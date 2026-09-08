function getSharedIntradaySignal(stock) {
  if (stock.intraday_signal && stock.intraday_signal.label) return stock.intraday_signal;
  const match = String(stock.change || "").match(/\(([-+]?\d+(?:\.\d+)?)%\)/);
  const percent = match ? Number(match[1]) : 0;
  const trend = stock.trend || "";
  if (percent >= 2 && trend === "牛市多头") return {label:"日内偏强", class:"signal-up", reason:"涨幅明显且站上20日均线"};
  if (percent <= -2 && trend === "熊市空头") return {label:"日内偏弱", class:"signal-down", reason:"跌幅明显且低于20日均线"};
  if (percent > 0.8 && trend === "牛市多头") return {label:"偏强观察", class:"signal-up", reason:"涨幅为正且趋势偏多"};
  if (percent < -0.8 && trend === "熊市空头") return {label:"偏弱观察", class:"signal-down", reason:"跌幅为负且趋势偏空"};
  return {label:"震荡观察", class:"signal-flat", reason:"涨跌幅与均线趋势未形成一致信号"};
}
function renderSharedSignalBadges(stock) {
  const signal = getSharedIntradaySignal(stock);
  const flow = stock.flow_proxy;
  const divergence = flow && ((signal.class === "signal-up" && flow.class === "signal-down") || (signal.class === "signal-down" && flow.class === "signal-up"));
  return '<div class="signal-badges">' +
    '<div class="intraday-signal ' + signal.class + '" title="根据指标计算">📈 策略：' + signal.label + ' · ' + signal.reason + '</div>' +
    (signal.plan ? '<div class="signal-plan">🧭 ' + signal.plan + '</div>' : '') +
    (flow && flow.label ? '<div class="intraday-signal ' + flow.class + '" title="根据价格与成交量估算，不代表真实机构订单">💰 资金：' + flow.label + ' · ' + flow.reason + ' · 量比 ' + flow.volume_ratio + 'x</div>' : '') +
    (divergence ? '<div class="signal-divergence">⚠️ 信号分歧：趋势与资金方向不一致</div>' : '') +
    '</div>';
}

function getHoldingCost(symbol) {
  const value = Number(localStorage.getItem("holding_cost_" + symbol));
  return Number.isFinite(value) && value > 0 ? value : "";
}
function updateHoldingCost(symbol, value) {
  const cost = Number(value);
  if (Number.isFinite(cost) && cost > 0) localStorage.setItem("holding_cost_" + symbol, cost);
  else localStorage.removeItem("holding_cost_" + symbol);
  const result = document.querySelector('[data-holding-result="' + symbol + '"]');
  if (result) result.textContent = formatHoldingResult(symbol, cost);
}
function formatHoldingResult(symbol, cost) {
  const card = document.querySelector('[data-stock-symbol="' + symbol + '"]');
  const current = card ? Number(card.dataset.currentPrice) : NaN;
  if (!Number.isFinite(cost) || cost <= 0 || !Number.isFinite(current)) return "填写成本价后显示盈亏";
  const pnl = current - cost;
  const pct = cost ? pnl / cost * 100 : 0;
  return (pnl >= 0 ? "当前浮盈 " : "当前浮亏 ") + Math.abs(pnl).toFixed(2) + "（" + (pnl >= 0 ? "+" : "") + pct.toFixed(2) + "%）";
}
function renderHoldingCost(stock) {
  const symbol = stock.symbol || stock.code || "";
  const cost = getHoldingCost(symbol);
  return '<div class="holding-cost" data-stock-symbol="' + symbol + '" data-current-price="' + (Number(stock.price) || 0) + '">' +
    '<label>💼 持仓成本</label><input type="number" min="0" step="0.01" placeholder="输入成本价" value="' + cost + '" onchange="updateHoldingCost(\'' + symbol + '\', this.value)">' +
    '<span class="holding-result" data-holding-result="' + symbol + '">' + formatHoldingResult(symbol, cost) + '</span></div>';
}
