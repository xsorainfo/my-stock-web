// components/common.js
// ============================================================
// 共同工具函数和逻辑
// ============================================================

// ============================================================
// 1. 全局变量 - sectorMapping 缓存
// ============================================================
let sectorMappingGlobal = [];

// ============================================================
// 2. 估值判断
// ============================================================
function judgeValuation(val, type) {
    if (!val || val === '--' || isNaN(parseFloat(val))) {
        return '<span class="val-badge val-normal">--</span>';
    }
    const num = parseFloat(val);
    if (type === 'PER' || type === 'forward_per') {
        if (num > 50) return `<span class="val-badge val-high">${num.toFixed(1)} 高估值</span>`;
        if (num < 25) return `<span class="val-badge val-low">${num.toFixed(1)} 具性价比</span>`;
        return `<span class="val-badge val-normal">${num.toFixed(1)} 合理</span>`;
    } else if (type === 'PBR') {
        if (num > 15) return `<span class="val-badge val-high">${num.toFixed(1)} 高溢价</span>`;
        if (num < 3) return `<span class="val-badge val-low">${num.toFixed(1)} 净资产防守</span>`;
        return `<span class="val-badge val-normal">${num.toFixed(1)} 正常</span>`;
    }
    return `<span class="val-badge val-normal">${num}</span>`;
}

// ============================================================
// 3. ROE 判断函数（4档：优秀/良好/一般/不佳）
// ============================================================
function judgeROE(roe) {
    if (!roe || roe === '--' || isNaN(parseFloat(roe))) {
        return '<span class="val-badge val-normal">--</span>';
    }
    const num = parseFloat(roe);
    if (num >= 15) return `<span class="val-badge val-high" style="background:#d1fae5;color:#065f46;">${roe} 優秀</span>`;
    if (num >= 10) return `<span class="val-badge val-normal" style="background:#dbeafe;color:#1d4ed8;">${roe} 良好</span>`;
    if (num >= 5) return `<span class="val-badge val-normal" style="background:#fef3c7;color:#92400e;">${roe} 一般</span>`;
    return `<span class="val-badge val-low" style="background:#fee2e2;color:#b91c1c;">${roe} 不佳</span>`;
}

// ============================================================
// 4. 市场标签
// ============================================================
function getMarketBadge(type) {
    const map = {
        '美股': '🇺🇸',
        '日股': '🇯🇵',
        'A股': '🇨🇳',
        '韩股': '🇰🇷',
        '德股': '🇩🇪'
    };
    return map[type] || '🌍';
}

// ============================================================
// 5. 雅虎财经链接
// ============================================================
function getYahooUrl(stock) {
    if (stock.market_type === '日股') {
        return `https://finance.yahoo.co.jp/quote/${stock.code}`;
    }
    if (stock.market_type === 'A股') {
        const prefix = (stock.code.startsWith('6')) ? 'sh' : 'sz';
        return `https://finance.sina.com.cn/realstock/company/${prefix}${stock.code}/nc.shtml`;
    }
    return `https://finance.yahoo.co.jp/quote/${stock.code}`;
}

// ============================================================
// 6. TradingView 链接
// ============================================================
function getTradingViewUrl(stock) {
    if (stock.market_type === '日股') {
        const cleanCode = stock.code.split('.')[0];
        return `https://jp.tradingview.com/symbols/TSE-${cleanCode}/`;
    } else if (stock.market_type === 'A股') {
        const prefix = stock.code.startsWith('6') ? "SHSE" : "SZSE";
        return `https://www.tradingview.com/symbols/${prefix}-${stock.code}/`;
    }
    return `https://www.tradingview.com/symbols/${stock.code}/`;
}

// ============================================================
// 7. 打开 kabuyoho 目标股价页面
// ============================================================
function openTargetPrice(symbol) {
    let cleanCode = symbol;
    if (symbol.includes('.')) {
        cleanCode = symbol.split('.')[0];
    }
    const url = `https://kabuyoho.jp/sp/reportTarget?bcode=${cleanCode}`;
    window.open(url, 'kabuyoho', 'width=1200,height=800,scrollbars=yes,resizable=yes');
}

// ============================================================
// 8. 复制到剪贴板
// ============================================================
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        console.log('已复制: ' + text);
    }).catch(err => {
        console.error('复制失败: ', err);
    });
}

// ============================================================
// 9. 渲染标签 HTML
// ============================================================
function renderTagsOld(tags) {
    if (!tags || tags.length === 0) return '';
    return tags.map(tag => `
        <span class="stock-tag clickable-tag" data-tag="${encodeURIComponent(tag)}" onclick="navigateToTheme('${encodeURIComponent(tag)}')">
            ${tag} 
        </span>
    `).join('&nbsp;&nbsp;');
}

// ============================================================
// 9. 渲染标签 HTML - 直接使用 display_tags（已映射完成）
// ============================================================
function renderTags(stock) {
    // ⭐ 防御性检查
    if (!stock || typeof stock !== 'object') {
        console.warn('renderTags: stock 参数无效', stock);
        return '';
    }
    
    // ⭐ 直接使用 display_tags（数据源已完成映射）
    const displayList = Array.isArray(stock.display_tags) ? stock.display_tags : [];
    if (displayList.length === 0) return '';
    
    // ⭐ 获取 tag_themes（已包含匹配好的路径）
    const tagThemes = Array.isArray(stock.tag_themes) ? stock.tag_themes : [];
    
    const result = [];
    displayList.forEach((displayTag) => {
        if (typeof displayTag !== 'string') return;
        
        // ⭐ 在 tag_themes 中查找匹配（直接用 displayTag 匹配）
        let foundPath = null;
        for (const t of tagThemes) {
            if (t.tag === displayTag && t.theme_path && t.theme_path.length > 0) {
                foundPath = t.theme_path;
                break;
            }
        }
        
        let displayText = displayTag;
        let hasPath = false;
        
        if (foundPath && foundPath.length >= 3) {
            // 显示完整的三级路径：一级 › 二级 › 三级
            displayText = `${foundPath[0]} › ${foundPath[1]} › ${displayTag}`;
            hasPath = true;
        } else if (foundPath && foundPath.length >= 2) {
            // 兼容只有两级的情况：一级 › 二级
            displayText = `${foundPath[0]} › ${displayTag}`;
            hasPath = true;
        }
        
        result.push({
            displayTag: displayTag,
            displayText: displayText,
            hasPath: hasPath
        });
    });
    
    // 去重
    const unique = [];
    const seen = new Set();
    result.forEach(item => {
        if (!seen.has(item.displayTag)) {
            seen.add(item.displayTag);
            unique.push(item);
        }
    });
    
    return unique.map(item => {
        const tagClass = item.hasPath ? 'stock-tag clickable-tag theme-tag' : 'stock-tag clickable-tag';
        const jumpTag = encodeURIComponent(item.displayTag);
        return `
            <span class="${tagClass}" data-tag="${jumpTag}" onclick="navigateToTheme('${jumpTag}')" title="${item.displayText}">
                ${item.displayText}
            </span>
        `;
    }).join('&nbsp;&nbsp;');
}
// ============================================================
// 9. 渲染标签 HTML（带层级路径 + 可点击跳转）
// ============================================================
function renderTags(tags, stockTagThemes) {
    if (!tags || tags.length === 0) return '';
    
    const result = [];
    tags.forEach(tag => {
        let foundPath = null;
        if (stockTagThemes) {
            for (const t of stockTagThemes) {
                if (t.tag === tag && t.theme_path && t.theme_path.length > 0) {
                    foundPath = t.theme_path;
                    break;
                }
            }
        }
        
        let displayText = tag;
        let hasPath = false;
        
        if (foundPath && foundPath.length >= 2) {
            displayText = `${foundPath[0]} › ${tag}`;
            hasPath = true;
        }
        
        result.push({
            tag: tag,
            displayText: displayText,
            hasPath: hasPath
        });
    });
    
    // 去重
    const unique = [];
    const seen = new Set();
    result.forEach(item => {
        if (!seen.has(item.tag)) {
            seen.add(item.tag);
            unique.push(item);
        }
    });
    
    return unique.map(item => {
        const tagClass = item.hasPath ? 'stock-tag clickable-tag theme-tag' : 'stock-tag clickable-tag';
        return `
            <span class="${tagClass}" data-tag="${encodeURIComponent(item.tag)}" onclick="navigateToTheme('${encodeURIComponent(item.tag)}')" title="${item.displayText}">
                ${item.displayText}
            </span>
        `;
    }).join('&nbsp;&nbsp;');
}

// ============================================================
// 修改后的 renderTags 函数 - 使用 display_tags 匹配主题
// ============================================================
function renderTags(tags, stockTagThemes, displayTags) {
    if (!tags || tags.length === 0) return '';
    
    // 如果没有 displayTags，使用原始 tags
    const displayList = displayTags || tags;
    
    const result = [];
    displayList.forEach((displayTag, index) => {
        // 使用原始 tag 去匹配 theme_path
        const rawTag = tags[index] || displayTag;
        let foundPath = null;
        
        if (stockTagThemes) {
            for (const t of stockTagThemes) {
                // ⭐ 关键：用原始 tag 匹配，但显示用 displayTag
                if (t.tag === rawTag && t.theme_path && t.theme_path.length > 0) {
                    foundPath = t.theme_path;
                    break;
                }
            }
        }
        
        let displayText = displayTag;
        let hasPath = false;
        
        if (foundPath && foundPath.length >= 3) {
            displayText = `${foundPath[0]} › ${foundPath[1]} › ${displayTag}`;
            hasPath = true;
        } else if (foundPath && foundPath.length >= 2) {
            displayText = `${foundPath[0]} › ${displayTag}`;
            hasPath = true;
        }
        
        result.push({
            tag: rawTag,           // 用于跳转时使用原始 tag
            displayText: displayText,
            hasPath: hasPath,
            displayTag: displayTag // 映射后的标签
        });
    });
    
    // 去重（基于 displayTag）
    const unique = [];
    const seen = new Set();
    result.forEach(item => {
        if (!seen.has(item.displayTag)) {
            seen.add(item.displayTag);
            unique.push(item);
        }
    });
    
    return unique.map(item => {
        const tagClass = item.hasPath ? 'stock-tag clickable-tag theme-tag' : 'stock-tag clickable-tag';
        // ⭐ 跳转时使用 displayTag（映射后的统一名称）
        const jumpTag = encodeURIComponent(item.displayTag);
        return `
            <span class="${tagClass}" data-tag="${jumpTag}" onclick="navigateToTheme('${jumpTag}')" title="${item.displayText}">
                ${item.displayText}
            </span>
        `;
    }).join('&nbsp;&nbsp;');
}
// ============================================================
// 10. 跳转到主题页面
// ============================================================
function navigateToTheme(tag) {
    const decodedTag = decodeURIComponent(tag);
    window.open(`/pages/sub_ai.html?tag=${encodeURIComponent(decodedTag)}`, '_blank');
}

// ============================================================
// 11. 加载 sector_mapping（返回 Promise）
// ============================================================
async function loadSectorMapping() {
    try {
        const response = await fetch('/data/sector_mapping.json?v=' + new Date().getTime());
        if (response.ok) {
            const data = await response.json();
            sectorMappingGlobal = data.sector_mapping || [];
            console.log('📊 sector_mapping 已加载，共', sectorMappingGlobal.length, '个板块');
            return sectorMappingGlobal;
        } else {
            console.warn('sector_mapping.json 加载失败');
            sectorMappingGlobal = [];
            return [];
        }
    } catch (e) {
        console.warn('sector_mapping.json 读取失败:', e);
        sectorMappingGlobal = [];
        return [];
    }
}

// ============================================================
// 12. 获取 sector_name
// ============================================================
function getSectorName(sectorId) {
    if (!sectorMappingGlobal || !Array.isArray(sectorMappingGlobal) || sectorMappingGlobal.length === 0) return sectorId;
    const found = sectorMappingGlobal.find(item => item.sector_id === sectorId);
    return found ? found.sector_name : sectorId;
}

// ============================================================
// 13. 获取 sector_comment
// ============================================================
function getSectorComment(sectorId) {
    if (!sectorMappingGlobal || !Array.isArray(sectorMappingGlobal) || sectorMappingGlobal.length === 0) return '';
    const found = sectorMappingGlobal.find(item => item.sector_id === sectorId);
    return found ? found.sector_comment : '';
}

// ============================================================
// 14. 获取 industry_name
// ============================================================
function getIndustryName(sectorId, industryId) {
    if (!sectorMappingGlobal || !Array.isArray(sectorMappingGlobal) || sectorMappingGlobal.length === 0) return industryId;
    const sector = sectorMappingGlobal.find(item => item.sector_id === sectorId);
    if (!sector) return industryId;
    const industry = sector.industries.find(item => item.industry_id === industryId);
    return industry ? industry.industry_name : industryId;
}

// ============================================================
// 15. 获取 industry_comment
// ============================================================
function getIndustryComment(sectorId, industryId) {
    if (!sectorMappingGlobal || !Array.isArray(sectorMappingGlobal) || sectorMappingGlobal.length === 0) return '';
    const sector = sectorMappingGlobal.find(item => item.sector_id === sectorId);
    if (!sector) return '';
    const industry = sector.industries.find(item => item.industry_id === industryId);
    return industry ? industry.industry_comment : '';
}
// components/common.js


// ============================================================
// 16. 将函数暴露到全局
// ============================================================
window.judgeValuation = judgeValuation;
window.judgeROE = judgeROE;
window.getMarketBadge = getMarketBadge;
window.getYahooUrl = getYahooUrl;
window.getTradingViewUrl = getTradingViewUrl;
window.openTargetPrice = openTargetPrice;
window.copyToClipboard = copyToClipboard;
window.renderTags = renderTags;
window.navigateToTheme = navigateToTheme;
window.loadSectorMapping = loadSectorMapping;
window.getSectorName = getSectorName;
window.getSectorComment = getSectorComment;
window.getIndustryName = getIndustryName;
window.getIndustryComment = getIndustryComment;
