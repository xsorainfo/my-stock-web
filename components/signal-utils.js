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
  return '<div class="signal-badges">' +
    '<div class="intraday-signal ' + signal.class + '" title="根据指标计算">📈 策略：' + signal.label + ' · ' + signal.reason + '</div>' +
    (flow && flow.label ? '<div class="intraday-signal ' + flow.class + '" title="根据价格与成交量估算，不代表真实机构订单">💰 资金：' + flow.label + ' · ' + flow.reason + ' · 量比 ' + flow.volume_ratio + 'x</div>' : '') +
    '</div>';
}
