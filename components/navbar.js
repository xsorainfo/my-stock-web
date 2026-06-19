// components/navbar.js
// 共通导航栏组件

function loadNavbar() {
    const navbarHTML = `
        <nav class="top-navbar">
            <div class="nav-logo">🖥️</div>
            <div class="nav-links">
                <a href="index.html" class="nav-item" data-page="index">首页</a>
                <a href="sub_ai.html" class="nav-item" data-page="sub_ai" target="_blank">テーマ別</a>
                <a href="settings.html" class="nav-item" data-page="settings">策略配置</a>
                <a href="watchlist_summary.html" class="nav-item" data-page="summary" target="_blank">📊 标的总结</a>
                <a href="semiconductor_industry.html" class="nav-item" data-page="semiconductor" target="_blank">🏭 半导体产业链</a>
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
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    const pageMap = {
        'index.html': 'index',
        'sub_ai.html': 'sub_ai',
        'settings.html': 'settings',
        'watchlist_summary.html': 'summary',
        'semiconductor_industry.html': 'semiconductor'
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
                    let s = 45;
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
