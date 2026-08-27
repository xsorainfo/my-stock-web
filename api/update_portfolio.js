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
    
    if (!authHeader || authHeader !== `Bearer ${expectedToken}`) {
        return res.status(401).json({ error: 'Unauthorized' });
    }

    const { listName, symbols, action } = req.body; // action: 'add' | 'remove' | 'update'

    if (!listName || !symbols || !Array.isArray(symbols)) {
        return res.status(400).json({ error: 'Invalid request: listName and symbols array required' });
    }

    try {
        // 3. 通过 GitHub API 读取并更新 portfolio_lists.py
        const octokit = new (require('@octokit/rest')).Octokit({
            auth: process.env.GITHUB_TOKEN
        });

        const owner = process.env.GITHUB_REPO_OWNER || 'your-username';
        const repo = process.env.GITHUB_REPO_NAME || 'my-stock-web';
        const path = 'scripts/portfolio_lists.py';

        // 读取当前文件
        let fileSha = null;
        let currentContent = '';
        try {
            const file = await octokit.repos.getContent({
                owner,
                repo,
                path
            });
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
        await octokit.repos.createOrUpdateFileContents({
            owner,
            repo,
            path,
            message: `📊 Update portfolio list: ${listName}`,
            content: Buffer.from(updatedContent, 'utf-8').toString('base64'),
            sha: fileSha || undefined
        });

        // 6. 触发 data.json 重新生成（复用 refresh 机制）
        const refreshUrl = `${req.headers.origin || 'https://my-stock-web-ashen.vercel.app'}/api/refresh`;
        await fetch(refreshUrl, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${process.env.MY_REPO_TOKEN}`
            }
        });

        res.status(200).json({ 
            success: true, 
            message: `Portfolio list "${listName}" updated successfully`,
            updatedSymbols: symbols 
        });

    } catch (error) {
        console.error('Error updating portfolio:', error);
        res.status(500).json({ error: error.message || 'Internal server error' });
    }
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
        beforeDict = dictContent + '\n\nPORTFOLIO_LISTS = {';
        innerContent = '';
        afterDict = '}\n';
    }

    // 解析现有的列表
    const lines = innerContent.split('\n');
    const listEntries = [];
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
            targetList.content = newListContent + ',\n';
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
