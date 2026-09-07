// Shared stock data helpers used by dashboard and portfolio pages.
(function () {
  function getStockChangeValue(stock) {
    return parseFloat(String(stock?.change || '').match(/[-+]?\d+(?:\.\d+)?%/)?.[0] || 0);
  }
  function stockSearchText(stock) {
    return [stock?.code, stock?.symbol, stock?.name, ...(Array.isArray(stock?.display_tags) ? stock.display_tags : [])]
      .map(v => String(v || '').toLowerCase()).join(' ');
  }
  function filterStocks(stocks, { query = '', market = '', sort = '' } = {}) {
    const q = String(query).trim().toLowerCase();
    const result = (Array.isArray(stocks) ? stocks : []).filter(stock =>
      (!q || stockSearchText(stock).includes(q)) && (!market || stock.market_type === market)
    );
    if (sort === 'change-desc') result.sort((a,b) => getStockChangeValue(b)-getStockChangeValue(a));
    if (sort === 'change-asc') result.sort((a,b) => getStockChangeValue(a)-getStockChangeValue(b));
    if (sort === 'name') result.sort((a,b) => String(a?.name || '').localeCompare(String(b?.name || '')));
    return result;
  }
  window.getStockChangeValue = getStockChangeValue;
  window.filterStocks = filterStocks;
})();