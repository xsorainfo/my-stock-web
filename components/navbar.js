// components/navbar.js
// 共通导航栏组件

// ============================================================
// ⭐ 网站统一配置（Logo + Favicon 集中管理）
// ============================================================
const SITE_CONFIG = {
    logo: '/assets/images/icon2.png',
    logoAlt: 'AI 硬科技',
    logoHeight: '32px',
    favicon: '/assets/images/StockLogo.jpg'
};

// ⭐ 添加这一行：获取网站根路径
const basePath = window.location.origin;

// ============================================================
// ⭐ 动态注入 Favicon（所有页面共用）
// ============================================================
function injectFavicon() {
    // 检查是否已存在 favicon 链接
    if (!document.querySelector('link[rel="icon"]')) {
        const link = document.createElement('link');
        link.rel = 'icon';
        link.type = 'image/jpeg';
        link.href = SITE_CONFIG.favicon;
        document.head.appendChild(link);
        console.log('✅ Favicon 已注入');
    }
    if (!document.querySelector('link[rel="apple-touch-icon"]')) {
        const link = document.createElement('link');
        link.rel = 'apple-touch-icon';
        link.href = SITE_CONFIG.favicon;
        document.head.appendChild(link);
    }
}

// ============================================================
// 加载导航栏
// ============================================================
function loadNavbar() {
    // ⭐ 注入 Favicon
    injectFavicon();

    const navbarHTML = `
        <nav class="top-navbar">
            <div class="nav-logo">
                <img src="${SITE_CONFIG.logo}" alt="${SITE_CONFIG.logoAlt}" style="height: ${SITE_CONFIG.logoHeight}; width: auto; border-radius: 4px;">
            </div>
            <div class="nav-links">
                <a href="${basePath}/pages/index.html" class="nav-item" data-page="index">首页</a>
                <a href="${basePath}/pages/sub_ai.html" class="nav-item" data-page="sub_ai" target="_blank">テーマ別</a>
                <a href="${basePath}/pages/settings.html" class="nav-item" data-page="settings">策略配置</a>
                <!-- ⭐ 下拉菜单：研究文档 -->
                <div class="dropdown">
                    <button class="dropbtn nav-item" data-page="docs">📚 研究文档 ▾</button>
                    <div class="dropdown-content">                        
                        <a href="${basePath}/docs/md.html?file=SEMICONDUCTOR_INDUSTRY" target="_blank">🧩 半导体产业链</a>
                        <a href="${basePath}/docs/md.html?file=AI_INDUSTRY_OVERVIEW" target="_blank">🧩 AI产业链全览</a>
                        <a href="${basePath}/pages/medical_devices.html" target="_blank">🏥 医疗器械产业</a>
                        <a href="${basePath}/pages/bond_transmission.html" target="_blank">💰 国债传导链</a>
                        <a href="${basePath}/docs/md.html?file=WATCHLIST_SUMMARY" target="_blank">📝 标的总结</a>
                    </div>
                </div>
                
                
            </div>
            <div class="nav-right">
                <button class="refresh-btn" id="cloudRefreshBtn">🔄 召唤云端强刷</button>
            </div>
        </nav>
    `;

    // 在页面中插入导航栏
    const placeholder = document.getElementById('navbar-placeholder');
    if (placeholder) {
        placeholder.innerHTML = navbarHTML;
    }

    // 高亮当前页面对应的导航项
    // components/navbar.js 中的高亮部分
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    const pageMap = {
        'index.html': 'index',
        'sub_ai.html': 'sub_ai',
        'settings.html': 'settings',
        'md.html': 'md'
    };
    const currentKey = pageMap[currentPage] || 'index';

    document.querySelectorAll('.nav-item[data-page]').forEach(item => {
        if (item.dataset.page === currentKey) {
            item.classList.add('active');
        }
    });

    // 绑定刷新按钮事件
    const refreshBtn = document.getElementById('cloudRefreshBtn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', async function() {
            const btn = this;
            if (btn.disabled) return;
            btn.disabled = true;
            btn.innerText = "正在发送指令...";
            try {
                const res = await fetch('/api/refresh', { method: 'POST' });
                if (res.ok) {
                    let s = 180;
                    btn.innerText = `🔄 等待 ${s}s 后刷新...`;
                    const t = setInterval(() => {
                        s--;
                        if (s > 0) btn.innerText = `🔄 等待 ${s}s 后刷新...`;
                        else { clearInterval(t); window.location.reload(); }
                    }, 1000);
                } else {
                    btn.disabled = false;
                    btn.innerText = '🔄 召唤云端强刷';
                    alert("刷新请求失败");
                }
            } catch (e) {
                btn.disabled = false;
                btn.innerText = '🔄 召唤云端强刷';
                alert("网络错误");
            }
        });
    }
}

// 确保 DOM 完全加载后再执行
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadNavbar);
} else {
    loadNavbar();
}
