// api/update_portfolio.js
// Vercel Serverless Function - 更新 portfolio_lists.py

export default async function handler(req, res) {
    // 1. 只允许 POST
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method not allowed' });
    }

    // 2. 验证 Token（复用 refresh.js 的验证方式）
    const authHeader = req.headers.authorization;
    const expectedToken = process.env.MY_REPO_TOKEN;
    
    if (!expectedToken) return res.status(503).json({ error: 'MY_REPO_TOKEN is not configured' });

    if (!authHeader || authHeader !== `Bearer ${expectedToken}`) {
        return res.status(401).json({ error: 'Unauthorized' });
    }

    const { listName, symbols = [], action = 'add' } = req.body || {}; // action: 'add' | 'remove' | 'update'

    if (typeof listName !== 'string' || !/^[\p{L}\p{N}_ -]{1,80}$/u.test(listName) ||
        !['add', 'remove', 'update'].includes(action) || !Array.isArray(symbols) ||
        !symbols.every(s => typeof s === 'string' && /^[A-Za-z0-9.^=-]{1,40}$/.test(s))) {
        return res.status(400).json({ error: 'Invalid request: listName and symbols array required' });
    }

    try {
        // 3. 通过 GitHub API 读取并更新 portfolio_lists.py
        const githubToken = process.env.GITHUB_TOKEN || expectedToken;

        const owner = process.env.GITHUB_REPO_OWNER || 'xsorainfo';
        const repo = process.env.GITHUB_REPO_NAME || 'my-stock-web';
        const path = 'scripts/portfolio_lists.py';

        // 读取当前文件
        let fileSha = null;
        let currentContent = '';
        try {
            const file = { data: await githubRequest(owner, repo, `contents/${path}`, githubToken) };
            fileSha = file.data.sha;
            currentContent = Buffer.from(file.data.content, 'base64').toString('utf-8');
        } catch (error) {
            if (error.status === 404) {
                // 文件不存在，创建默认内容
                currentContent = `# scripts/portfolio_lists.py\n# ポートフォリオ定義（銘柄リスト）\n\nPORTFOLIO_LISTS = {}\n`;
            } else {
                throw error;
            }
        }

        // 4. 更新 Python dict
        const updatedContent = updatePythonDict(currentContent, listName, symbols, action);

        // 5. 写回 GitHub
        await githubRequest(owner, repo, `contents/${path}`, githubToken, 'PUT', {
            message: `📊 Update portfolio list: ${listName}`,
            content: Buffer.from(updatedContent, 'utf-8').toString('base64'),
            sha: fileSha || undefined
        });

        // 保存与刷新分别报告，避免保存成功后因刷新失败而误报整体失败。
        let refreshTriggered = false;
        try {
            await githubRequest(owner, repo, 'dispatches', githubToken, 'POST', { event_type: 'web_refresh' });
            refreshTriggered = true;
        } catch (error) {
            console.error('Portfolio saved, but refresh failed:', error.message);
        }

        res.status(200).json({ 
            success: true,
            refreshTriggered, 
            message: `Portfolio list "${listName}" updated successfully`,
            updatedSymbols: symbols 
        });

    } catch (error) {
        console.error('Error updating portfolio:', error);
        res.status(500).json({ error: error.message || 'Internal server error' });
    }
}

async function githubRequest(owner, repo, path, token, method = 'GET', body) {
    const response = await fetch(`https://api.github.com/repos/${encodeURIComponent(owner)}/${encodeURIComponent(repo)}/${path}`, {
        method,
        headers: { Accept: 'application/vnd.github+json', Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
        ...(body === undefined ? {} : { body: JSON.stringify(body) })
    });
    if (!response.ok) {
        const error = new Error(`GitHub request failed (${response.status})`);
        error.status = response.status;
        throw error;
    }
    return response.status === 204 ? null : response.json();
}

// Python dict 更新函数
function updatePythonDict(content, listName, symbols, action = 'add') {
    // 解析现有的 PORTFOLIO_LISTS
    let dictContent = content;
    
    // 提取 PORTFOLIO_LISTS = {...} 部分
    const dictMatch = dictContent.match(/PORTFOLIO_LISTS\s*=\s*\{([\s\S]*?)\}\s*$/);
    let innerContent = '';
    let beforeDict = '';
    let afterDict = '';
    
    if (dictMatch) {
        beforeDict = dictContent.substring(0, dictContent.indexOf('PORTFOLIO_LISTS'));
        innerContent = dictMatch[1];
        afterDict = dictContent.substring(dictContent.lastIndexOf('}') + 1);
    } else {
        // 没有找到，在末尾追加
        throw new Error('Unsupported portfolio file format; no changes written');
    }

    // 解析现有的列表
    const lines = innerContent.split('\n');
    let listEntries = [];
    let currentList = null;
    let inList = false;
    let braceDepth = 0;

    // 简单的行解析（处理引号内的内容）
    for (let line of lines) {
        const trimmed = line.trim();
        
        // 检测列表名: "list_name": {
        const listMatch = trimmed.match(/^"([^"]+)"\s*:\s*\{/);
        if (listMatch) {
            if (currentList) {
                // 保存之前的列表
                listEntries.push(currentList);
            }
            currentList = {
                name: listMatch[1],
                content: line + '\n',
                braceDepth: 1,
                inList: true
            };
            continue;
        }

        if (currentList && currentList.inList) {
            currentList.content += line + '\n';
            // 计算括号深度
            const openBraces = (line.match(/\{/g) || []).length;
            const closeBraces = (line.match(/\}/g) || []).length;
            currentList.braceDepth += openBraces - closeBraces;
            
            if (currentList.braceDepth === 0) {
                // 列表结束
                currentList.inList = false;
                listEntries.push(currentList);
                currentList = null;
            }
            continue;
        }

        // 不在任何列表内
        if (trimmed && !trimmed.startsWith('//') && !trimmed.startsWith('#')) {
            // 可能是注释或空行
        }
    }

    // 查找或创建目标列表
    let targetList = listEntries.find(l => l.name === listName);
    
    if (action === 'remove') {
        // 移除列表
        listEntries = listEntries.filter(l => l.name !== listName);
    } else {
        // 添加或更新
        const symbolsStr = JSON.stringify(symbols, null, 8)
            .replace(/\n/g, '\n        ')
            .replace(/\[\s*/, '[')
            .replace(/\s*\]/, ']');
        
        const newListContent = `    "${listName}": {\n        "name": "${listName}",\n        "icon": "📌",\n        "description": "ユーザー追加リスト",\n        "symbols": ${symbolsStr}\n    }`;
        
        if (targetList) {
            // 更新现有列表
            if (!/"symbols"\s*:\s*\[[\s\S]*?\]/.test(targetList.content)) throw new Error('Missing symbols field');
            targetList.content = targetList.content.replace(/("symbols"\s*:\s*)\[[\s\S]*?\]/, (_, prefix) => prefix + symbolsStr);
        } else {
            // 添加新列表
            listEntries.push({
                name: listName,
                content: newListContent + ',\n',
                braceDepth: 0,
                inList: false
            });
        }
    }

    // 重新构建内嵌内容
    const newInnerContent = listEntries.map(l => l.content).join('\n');
    
    // 组合最终内容
    let result = beforeDict + 'PORTFOLIO_LISTS = {\n' + newInnerContent + '}\n' + afterDict;
    
    // 清理多余的逗号
    result = result.replace(/,\s*\n\s*\}/g, '\n}');
    result = result.replace(/,\s*\n\s*\}\)/g, '\n    }');
    
    return result;
}
