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
function renderTags(tags, stockTagThemes, displayTags) {
    // ⭐ 防御性检查：确保 displayTags 是数组
    let displayList = [];
    
    // 优先使用 displayTags
    if (displayTags && Array.isArray(displayTags)) {
        displayList = displayTags;
    } else if (tags && Array.isArray(tags)) {
        displayList = tags;
    } else {
        return '';
    }
    
    if (!Array.isArray(displayList) || displayList.length === 0) {
        return '';
    }
    
    const tagThemes = Array.isArray(stockTagThemes) ? stockTagThemes : [];
    
    const result = [];
    displayList.forEach((displayTag) => {
        if (typeof displayTag !== 'string') return;
        
        let foundPath = null;
        for (const t of tagThemes) {
            if (t && t.tag === displayTag && t.theme_path && Array.isArray(t.theme_path) && t.theme_path.length > 0) {
                foundPath = t.theme_path;
                break;
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
    
    if (unique.length === 0) return '';
    
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

// ============================================================
// 16. 备忘录（メモ）功能
// ============================================================

// ⭐ 获取备忘录存储 key
function getMemoKey(symbol) {
    return `stock_memo_${symbol}`;
}

// ⭐ 保存备忘录
function saveMemo(symbol, text) {
    try {
        localStorage.setItem(getMemoKey(symbol), text);
        return true;
    } catch (e) {
        console.error('保存备忘录失败:', e);
        return false;
    }
}

// ⭐ 读取备忘录
function loadMemo(symbol) {
    try {
        return localStorage.getItem(getMemoKey(symbol)) || '';
    } catch (e) {
        console.error('读取备忘录失败:', e);
        return '';
    }
}

// ⭐ 检查是否有备忘录
function hasMemo(symbol) {
    const memo = loadMemo(symbol);
    return memo && memo.trim().length > 0;
}

// ⭐ 删除备忘录
function deleteMemo(symbol) {
    try {
        localStorage.removeItem(getMemoKey(symbol));
        return true;
    } catch (e) {
        console.error('删除备忘录失败:', e);
        return false;
    }
}

// ⭐ 获取备忘录字符数
function getMemoCharCount(text) {
    return text ? text.length : 0;
}

// ⭐ 生成备忘录 HTML（在卡片底部使用）
function renderMemoHTML(stock) {
    const symbol = stock.code;
    const memoText = loadMemo(symbol);
    const hasMemoText = memoText && memoText.trim().length > 0;
    const charCount = getMemoCharCount(memoText);
    // ⭐ 空の場合はデフォルトテキストを表示
    const displayText = hasMemoText ? memoText : '🌺\n9️⃣\n🇩';
    const displayHasMemo = hasMemoText || true;  // 空でも表示する
    
    // デフォルトテキストの場合はインジケーターを表示しない
    const indicatorClass = hasMemoText ? 'has-memo' : '';
    
    // ⭐ 空でない場合は展開（デフォルトテキストも展開）
    //const isOpen = 'open';
    //const arrowClass = 'open';
    
    // ⭐ 如果有备忘录内容，默认展开
    const isOpen = hasMemoText ? 'open' : '';
    const arrowClass = hasMemoText ? 'open' : '';
    
    // ⭐ 行数に応じて初期高さを計算（1行あたり約20px + パディング）
    const lineCount = (displayText.match(/\n/g) || []).length + 1;
    const initialHeight = Math.max(56, lineCount * 20 + 16);
    
    return `
        <div class="stock-memo-section">
            <div class="stock-memo-toggle" onclick="toggleMemo('${symbol}')">
                <span class="memo-icon">📝</span>
                <span>メモ</span>
                <span class="memo-indicator ${indicatorClass}"></span>
                <span class="memo-arrow ${arrowClass}" id="memoArrow_${symbol}">▶</span>
            </div>
            <div class="stock-memo-body ${isOpen}" id="memoBody_${symbol}">
                <textarea 
                    class="stock-memo-textarea" 
                    id="memoTextarea_${symbol}"
                    placeholder="ここにメモを入力..."
                    maxlength="500"
                    style="min-height:56px;height:${initialHeight}px;overflow-y:hidden;"
                    oninput="autoResizeMemo('${symbol}')"
                >${displayText.replace(/"/g, '&quot;')}</textarea>
                <div class="stock-memo-actions">
                    <span class="stock-memo-char-count" id="memoCount_${symbol}">${getMemoCharCount(displayText)}/500</span>
                    <button class="stock-memo-save-btn" id="memoSaveBtn_${symbol}" onclick="saveMemoHandler('${symbol}')">
                        💾 保存
                    </button>
                </div>
            </div>
        </div>
    `;
}
// ⭐ 切换备忘录展开/收起
function toggleMemo(symbol) {
    const body = document.getElementById(`memoBody_${symbol}`);
    const arrow = document.getElementById(`memoArrow_${symbol}`);
    if (body) {
        body.classList.toggle('open');
        if (arrow) {
            arrow.classList.toggle('open');
        }
        if (body.classList.contains('open')) {
            const textarea = document.getElementById(`memoTextarea_${symbol}`);
            if (textarea && !textarea.value.trim()) {
                setTimeout(() => textarea.focus(), 100);
            }
        }
    }
}

// ⭐ 备忘录输入事件
function onMemoInput(symbol) {
    const textarea = document.getElementById(`memoTextarea_${symbol}`);
    const countEl = document.getElementById(`memoCount_${symbol}`);
    if (textarea && countEl) {
        const len = textarea.value.length;
        countEl.textContent = `${len}/500`;
        countEl.className = 'stock-memo-char-count' + (len > 450 ? ' warning' : '') + (len > 480 ? ' danger' : '');
    }
}

// ⭐ 保存备忘录处理
function saveMemoHandler(symbol) {
    const textarea = document.getElementById(`memoTextarea_${symbol}`);
    const btn = document.getElementById(`memoSaveBtn_${symbol}`);
    if (!textarea) return;
    
    const text = textarea.value;
    const success = saveMemo(symbol, text);
    
    if (success) {
        btn.textContent = '✅ 保存完了';
        btn.classList.add('saved');
        
        // 如果开启自动备份，保存时自动下载备份
        if (autoBackupEnabled) {
            setTimeout(() => {
                exportAllMemosSilent();
            }, 100);
        }
        
        setTimeout(() => {
            btn.textContent = '💾 保存';
            btn.classList.remove('saved');
        }, 2000);
        
        // 更新指示器
        const section = btn.closest('.stock-memo-section');
        if (section) {
            const indicator = section.querySelector('.memo-indicator');
            if (indicator) {
                if (text && text.trim().length > 0) {
                    indicator.classList.add('has-memo');
                } else {
                    indicator.classList.remove('has-memo');
                }
            }
        }
    } else {
        btn.textContent = '❌ 保存失敗';
        setTimeout(() => {
            btn.textContent = '💾 保存';
        }, 2000);
    }
}

// ⭐ 删除备忘录处理
function deleteMemoHandler(symbol) {
    if (confirm('メモを削除しますか？')) {
        const textarea = document.getElementById(`memoTextarea_${symbol}`);
        if (textarea) {
            textarea.value = '';
            saveMemo(symbol, '');
            const countEl = document.getElementById(`memoCount_${symbol}`);
            if (countEl) countEl.textContent = '0/500';
            const section = textarea.closest('.stock-memo-section');
            if (section) {
                const indicator = section.querySelector('.memo-indicator');
                if (indicator) indicator.classList.remove('has-memo');
            }
            const btn = document.getElementById(`memoSaveBtn_${symbol}`);
            if (btn) {
                btn.textContent = '✅ 削除完了';
                btn.classList.add('saved');
                setTimeout(() => {
                    btn.textContent = '💾 保存';
                    btn.classList.remove('saved');
                }, 2000);
            }
        }
    }
}

// ============================================================
// 17. 备忘录备份功能
// ============================================================

// ⭐ 导出所有备忘录为 JSON 文件
function exportAllMemos() {
    const allMemos = {};
    let count = 0;
    
    for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        if (key && key.startsWith('stock_memo_')) {
            const symbol = key.replace('stock_memo_', '');
            const memo = localStorage.getItem(key);
            if (memo && memo.trim().length > 0) {
                allMemos[symbol] = memo;
                count++;
            }
        }
    }
    
    if (count === 0) {
        alert('📭 保存されたメモがありません。');
        return;
    }
    
    const backupData = {
        exportedAt: new Date().toISOString(),
        version: '1.0',
        totalMemos: count,
        memos: allMemos
    };
    
    const blob = new Blob([JSON.stringify(backupData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `memos_backup_${new Date().toISOString().slice(0,10)}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    console.log(`✅ ${count}件のメモをエクスポートしました`);
}

// ⭐ 导入备忘录备份文件
function importAllMemos(file) {
    if (!file) return;
    
    const reader = new FileReader();
    reader.onload = function(e) {
        try {
            const data = JSON.parse(e.target.result);
            
            if (!data.memos || typeof data.memos !== 'object') {
                alert('❌ 無効なバックアップファイルです。');
                return;
            }
            
            const memos = data.memos;
            let count = 0;
            let overwritten = 0;
            
            for (const [symbol, memo] of Object.entries(memos)) {
                if (memo && memo.trim().length > 0) {
                    const existing = localStorage.getItem(`stock_memo_${symbol}`);
                    if (existing && existing.trim().length > 0) {
                        overwritten++;
                    }
                    localStorage.setItem(`stock_memo_${symbol}`, memo);
                    count++;
                }
            }
            
            const msg = `✅ ${count}件のメモをインポートしました。\n${overwritten > 0 ? `⚠️ ${overwritten}件は上書きされました。` : ''}`;
            alert(msg);
            console.log(msg);
            
            if (confirm('🔄 ページをリフレッシュして表示を更新しますか？')) {
                location.reload();
            }
        } catch (error) {
            alert('❌ インポートに失敗しました。ファイル形式を確認してください。');
            console.error('导入失败:', error);
        }
    };
    reader.readAsText(file);
}

// ⭐ 静默导出（不弹窗）
function exportAllMemosSilent() {
    const allMemos = {};
    let count = 0;
    
    for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        if (key && key.startsWith('stock_memo_')) {
            const symbol = key.replace('stock_memo_', '');
            const memo = localStorage.getItem(key);
            if (memo && memo.trim().length > 0) {
                allMemos[symbol] = memo;
                count++;
            }
        }
    }
    
    if (count === 0) return;
    
    const backupData = {
        exportedAt: new Date().toISOString(),
        version: '1.0',
        totalMemos: count,
        memos: allMemos
    };
    
    const blob = new Blob([JSON.stringify(backupData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `memos_auto_${new Date().toISOString().slice(0,10)}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// ⭐ 自动备份开关
let autoBackupEnabled = false;

function toggleAutoBackup() {
    autoBackupEnabled = !autoBackupEnabled;
    localStorage.setItem('auto_backup_enabled', autoBackupEnabled ? 'true' : 'false');
    
    const btn = document.getElementById('autoBackupBtn');
    if (btn) {
        btn.textContent = `🔄 自動バックアップ: ${autoBackupEnabled ? 'ON' : 'OFF'}`;
        btn.style.background = autoBackupEnabled ? '#d1fae5' : '#f1f5f9';
        btn.style.color = autoBackupEnabled ? '#065f46' : '#1e293b';
    }
    
    console.log(`📦 自動バックアップ: ${autoBackupEnabled ? 'ON' : 'OFF'}`);
}

// ⭐ 初始化自动备份设置
function initAutoBackup() {
    const saved = localStorage.getItem('auto_backup_enabled');
    autoBackupEnabled = saved === 'true';
    return autoBackupEnabled;
}

// ============================================================
// 18. 将函数暴露到全局
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

// 备忘录函数
window.saveMemo = saveMemo;
window.loadMemo = loadMemo;
window.hasMemo = hasMemo;
window.deleteMemo = deleteMemo;
window.renderMemoHTML = renderMemoHTML;
window.toggleMemo = toggleMemo;
window.onMemoInput = onMemoInput;
window.saveMemoHandler = saveMemoHandler;
window.deleteMemoHandler = deleteMemoHandler;
window.exportAllMemos = exportAllMemos;
window.importAllMemos = importAllMemos;
window.toggleAutoBackup = toggleAutoBackup;
window.initAutoBackup = initAutoBackup;


// ============================================================
// 19. 空卖链接（直接跳转）
// ============================================================

function renderShortBadge(symbol) {
    if (!symbol) return '';
    
    // 提取纯数字代码
    let cleanCode = symbol;
    if (symbol.includes('.')) {
        cleanCode = symbol.split('.')[0];
    }
    cleanCode = cleanCode.replace(/\D/g, '');
    if (!cleanCode) return '';
    
    const irbankUrl = `https://irbank.net/short/search?q=${cleanCode}`;
    
    return `
        <a href="${irbankUrl}" target="_blank" rel="noopener noreferrer" 
           class="short-badge" style="text-decoration: none; display: inline-flex; align-items: center; gap: 3px; margin-left: 6px; font-size: 10px; font-weight: 700; color: #ef4444; background: #fee2e2; padding: 1px 8px; border-radius: 10px; border: 1px solid #fca5a5; transition: all 0.2s;">
            <span style="font-size: 11px;">📉</span>
            空売り
        </a>
    `;
}

// 导出到全局
window.renderShortBadge = renderShortBadge;

// ============================================================
// 20. 判断是否为大幅波动（涨跌幅 ≥ 6%）
// ============================================================

function getChangePercent(changeStr) {
    if (!changeStr) return 0;
    const match = changeStr.match(/\(([^)]+)%\)/);
    if (match) {
        return parseFloat(match[1]);
    }
    return 0;
}

function getBigMoveMark(changeStr) {
    const percent = getChangePercent(changeStr);
    const absPercent = Math.abs(percent);
    
    if (absPercent < 5) return '';  // 涨跌幅 < 5%，不显示
    
    // 涨幅 ≥ 6%
    if (percent > 0) {
        return '<span class="big-move-mark big-up">🔥大涨</span>';
    }
    // 跌幅 ≥ 6%
    if (percent < 0) {
        return '<span class="big-move-mark big-down">⚠️大跌</span>';
    }
    return '';
}
// ============================================================
// 21. 返回顶部功能（共通）
// ============================================================

function initBackToTop() {
    // 既存のボタンを削除（重複防止）
    const existingBtn = document.getElementById('backToTop');
    if (existingBtn) {
        existingBtn.remove();
    }
    
    // ボタンを作成
    const btn = document.createElement('button');
    btn.id = 'backToTop';
    btn.className = 'back-to-top';
    btn.innerHTML = '⬆';
    btn.setAttribute('title', '先頭に戻る');
    document.body.appendChild(btn);
    
    let isScrolling = false;
    let scrollTimer = null;
    
    // スクロール検知
    window.addEventListener('scroll', function() {
        if (window.scrollY > 300) {
            btn.classList.add('visible');
        } else {
            btn.classList.remove('visible');
        }
        
        isScrolling = true;
        clearTimeout(scrollTimer);
        scrollTimer = setTimeout(function() {
            isScrolling = false;
        }, 150);
    }, { passive: true });
    
    // クリックでトップへ
    btn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    console.log('⬆ 返回顶部ボタンが初期化されました');
}

// ページ読み込み完了時に自動初期化
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initBackToTop);
} else {
    initBackToTop();
}

// グローバルに公開（必要に応じて手動呼び出しも可能）
window.initBackToTop = initBackToTop;
// 导出到全局
window.getChangePercent = getChangePercent;
window.getBigMoveMark = getBigMoveMark;
