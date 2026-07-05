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
function renderTags(tags) {
    if (!tags || tags.length === 0) return '';
    return tags.map(tag => `
        <span class="stock-tag clickable-tag" data-tag="${encodeURIComponent(tag)}" onclick="navigateToTheme('${encodeURIComponent(tag)}')">
            ${tag} 
        </span>
    `).join('&nbsp;&nbsp;');
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
// 市场标签（带颜色）
// ============================================================
function getMarketBadgeWithColor(marketType) {
    const map = {
        '美股': { label: '🇺🇸 美股', color: '#3b82f6', bg: 'rgba(59, 130, 246, 0.10)' },
        '日股': { label: '🇯🇵 日股', color: '#ef4444', bg: 'rgba(239, 68, 68, 0.10)' },
        'A股': { label: '🇨🇳 A股', color: '#f59e0b', bg: 'rgba(245, 158, 11, 0.10)' },
        '港股': { label: '🇭🇰 港股', color: '#8b5cf6', bg: 'rgba(139, 92, 246, 0.10)' },
        '韩股': { label: '🇰🇷 韩股', color: '#14b8a6', bg: 'rgba(20, 184, 166, 0.10)' },
        '德股': { label: '🇩🇪 德股', color: '#f97316', bg: 'rgba(249, 115, 22, 0.10)' },
    };
    return map[marketType] || { label: '🌍', color: '#94a3b8', bg: 'rgba(148, 163, 184, 0.10)' };
}

// ============================================================
// 市场标签 HTML
// ============================================================
function renderMarketBadge(marketType) {
    const info = getMarketBadgeWithColor(marketType);
    return `<span class="market-badge" style="
        display: inline-block;
        font-size: 10px;
        font-weight: 600;
        padding: 1px 8px;
        border-radius: 10px;
        color: ${info.color};
        background: ${info.bg};
        border: 1px solid ${info.color}40;
        margin-left: 6px;
        line-height: 1.6;
    ">${info.label}</span>`;
}
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
