// api/update_portfolio.js
// Vercel Serverless Function - 更新 portfolio_lists.py

export default async function handler(req, res) {
    // 1. 只允许 POST
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method not allowed' });
    }

    // 2. 验证 Token（复用 refresh.js 的验证方式）
    const authHeader = req.headers.authorization;
    const isAppend = req.body?.action === 'append';
    const expectedToken = isAppend ? process.env.PORTFOLIO_EDIT_PASSWORD : process.env.MY_REPO_TOKEN;
    
    if (!expectedToken) return res.status(503).json({ error: isAppend ? '请先在 Vercel 配置 PORTFOLIO_EDIT_PASSWORD' : 'MY_REPO_TOKEN is not configured' });

    if (!authHeader || authHeader !== `Bearer ${isAppend ? encodeURIComponent(expectedToken) : expectedToken}`) {
        return res.status(401).json({ error: 'Unauthorized' });
    }

    const { listName, symbols = [], action = 'add' } = req.body || {}; // action: 'add' | 'remove' | 'update'

    if (typeof listName !== 'string' || !/^[\p{L}\p{N}_ -]{1,80}$/u.test(listName) ||
        !['add', 'remove', 'update', 'append'].includes(action) || !Array.isArray(symbols) ||
        !symbols.every(s => typeof s === 'string' && /^[A-Za-z0-9.^=-]{1,40}$/.test(s))) {
        return res.status(400).json({ error: 'Invalid request: listName and symbols array required' });
    }

    try {
        // 3. 通过 GitHub API 读取并更新 portfolio_lists.py
        const githubToken = process.env.GITHUB_TOKEN || process.env.MY_REPO_TOKEN;
        if (!githubToken) return res.status(503).json({ error: 'GitHub write credentials are not configured' });

        const owner = process.env.GITHUB_REPO_OWNER || 'xsorainfo';
        const repo = process.env.GITHUB_REPO_NAME || 'my-stock-web';
        const path = 'scripts/portfolio_lists.py';

        let updatedSymbols = symbols;
        let changed = false;
        for (let attempt = 0; attempt < 3; attempt++) {
            const file = await githubRequest(owner, repo, `contents/${path}`, githubToken);
            const currentContent = Buffer.from(file.content, 'base64').toString('utf-8');
            const result = isAppend
                ? appendPortfolioSymbols(currentContent, listName, symbols)
                : { content: updatePythonDict(currentContent, listName, symbols, action), symbols };
            updatedSymbols = result.symbols;
            if (result.content === currentContent) break;
            try {
                await githubRequest(owner, repo, `contents/${path}`, githubToken, 'PUT', {
                    message: `Update portfolio list: ${listName}`,
                    content: Buffer.from(result.content, 'utf-8').toString('base64'),
                    sha: file.sha
                });
                changed = true;
                break;
            } catch (error) {
                if (error.status !== 409 || attempt === 2) throw error;
            }
        }

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
            updatedSymbols,
            changed 
        });

    } catch (error) {
        console.error('Error updating portfolio:', error);
        res.status(error.status === 409 ? 409 : error.status === 404 ? 404 : 500).json({ error: error.message || 'Internal server error' });
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


// Locate Python literals without treating braces inside strings/comments as syntax.
function closingDelimiter(source, start) {
    const pairs = { '{': '}', '[': ']' };
    const stack = [];
    let quote = null, escaped = false, comment = false;
    for (let i = start; i < source.length; i++) {
        const ch = source[i];
        if (comment) { if (ch === '\n') comment = false; continue; }
        if (quote) {
            if (escaped) escaped = false;
            else if (ch === '\\') escaped = true;
            else if (ch === quote) quote = null;
            continue;
        }
        if (ch === '#') { comment = true; continue; }
        if (ch === '"' || ch === "'") { quote = ch; continue; }
        if (pairs[ch]) stack.push(pairs[ch]);
        else if (ch === '}' || ch === ']') {
            if (stack.pop() !== ch) throw new Error('Unsupported portfolio format');
            if (!stack.length) return i;
        }
    }
    throw new Error('Unclosed portfolio literal');
}

function appendPortfolioSymbols(content, listName, symbols) {
    const entries = /^[ \t]*"([^"\n]+)"[ \t]*:[ \t]*\{/gm;
    let match, target;
    while ((match = entries.exec(content))) {
        const start = entries.lastIndex - 1;
        const end = closingDelimiter(content, start);
        if (match[1] === listName) { target = {start, end}; break; }
        entries.lastIndex = end + 1;
    }
    if (!target) {
        const error = new Error('组合不存在，请刷新页面后重试');
        error.status = 404; throw error;
    }
    const block = content.slice(target.start, target.end + 1);
    const field = /"symbols"\s*:\s*\[/.exec(block);
    if (!field) throw new Error('Missing symbols field');
    const start = target.start + field.index + field[0].length - 1;
    const end = closingDelimiter(content, start);
    // Symbols are a list of plain strings; reject executable Python expressions.
    const literal = content.slice(start + 1, end).replace(/#[^\n]*/g, '');
    const existing = [];
    let remainder = literal;
    const item = /^\s*(["'])([A-Za-z0-9.^=-]{1,40})\1\s*(,|$)/;
    while (remainder.trim()) {
        const value = item.exec(remainder);
        if (!value) throw new Error('Unsupported symbols format');
        existing.push(value[2]);
        remainder = remainder.slice(value[0].length);
    }
    const key = s => s.toUpperCase().replace(/\.SH$/, '.SS');
    const merged = [...existing];
    const seen = new Set(existing.map(key));
    for (const symbol of symbols) {
        const normalized = key(symbol);
        if (!seen.has(normalized)) { merged.push(normalized); seen.add(normalized); }
    }
    if (merged.length === existing.length) return {content, symbols: merged};
    const updated = content.slice(0, start) + JSON.stringify(merged, null, 4) + content.slice(end + 1);
    return {content: updated, symbols: merged};
}
