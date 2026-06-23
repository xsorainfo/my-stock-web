// components/footer.js
// ============================================================
// Footer 共通组件 - 和导航栏一样的加载方式
// ============================================================

(function() {
    // 防止重复加载
    if (document.getElementById('footer-placeholder')?.dataset.loaded === 'true') {
        return;
    }

    function renderFooter() {
        const year = new Date().getFullYear();
        return `
            <footer class="simple-footer">
                <span class="brand">⚡ AI 半导体策略研究室</span>
                <span class="divider">|</span>
                <span>© ${year} 版权所有</span>
                <span class="divider">|</span>
                <span>📊 数据仅供参考，不构成投资建议</span>
            </footer>
        `;
    }

    function loadFooter() {
        const placeholder = document.getElementById('footer-placeholder');
        if (!placeholder) {
            console.warn('⚠️ 找不到 #footer-placeholder，跳过 Footer 渲染');
            return;
        }

        // 防止重复加载
        if (placeholder.dataset.loaded === 'true') return;
        placeholder.dataset.loaded = 'true';

        placeholder.innerHTML = renderFooter();
        console.log('📋 Footer 加载完成');
    }

    // DOM 加载完成后执行
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', loadFooter);
    } else {
        loadFooter();
    }
})();
