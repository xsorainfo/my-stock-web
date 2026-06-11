import json
import yfinance as yf

# 1. 定义你想监控的自选股清单（可以随时在这里加减）
# 格式为: {"股票代码": "你想在网页上显示的中文名字"}
# 注意：日股加 .T，港股加 .HK，美股直接写代号（如 AAPL）
WATCHLIST = {
    "5817.T": "JMACS",
    "3110.T": "日東紡績",
    "5803.T": "フジクラ"
}

def fetch_stock_data():
    updated_list = []
    
    for symbol, name in WATCHLIST.items():
        try:
            print(f"正在抓取 {name} ({symbol})...")
            stock = yf.Ticker(symbol)
            info = stock.info
            
            # 拿最新价
            current_price = info.get('currentPrice') or info.get('regularMarketPrice')
            # 拿昨收价算涨跌
            prev_close = info.get('previousClose')
            
            if current_price and prev_close:
                diff = current_price - prev_close
                percent = (diff / prev_close) * 100
                # 拼装涨跌幅文字
                sign = "+" if diff > 0 else ""
                change_str = f"{sign}{diff:.2f} ({sign}{percent:.2f}%)"
                is_up = diff > 0
            else:
                change_str = "--"
                is_up = False
                
            # 提取 PER 并根据数值打上不同的状态标签
            per = info.get('forwardPE') or info.get('trailingPE') or "--"
            per_display = f"{per:.2f}" if isinstance(per, (int, float)) else str(per)
            
            if isinstance(per, (int, float)):
                if per < 0:
                    per_display += " (亏损)"
                elif per < 15.0:
                    per_display += " (低估)"
                elif 15.0 <= per <= 35.0:
                    per_display += " (合理)"
                else:
                    per_display += " (偏高)"

            # 提取 PBR 并根据数值打上不同的状态标签
            pbr = info.get('priceToBook') or "--"
            pbr_display = f"{pbr:.2f}" if isinstance(pbr, (int, float)) else str(pbr)
            
            if isinstance(pbr, (int, float)):
                if pbr < 1.0:
                    pbr_display += " (低估)"
                elif 1.0 <= pbr <= 3.0:
                    pbr_display += " (合理)"
                else:
                    pbr_display += " (偏高)"
            
                    
            # 组装成网页需要的格式
            updated_list.append({
                "code": symbol.split('.')[0], # 去掉尾巴，只要数字代码
                "name": name,
                "price": current_price,
                "change": change_str,
                "isUp": is_up,
                "per": per_display,
                "pbr": pbr_display
            })
        except Exception as e:
            print(f"{name} 抓取失败: {e}")
            
    # 2. 把结果写入 data.json 文件
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(updated_list, f, ensure_ascii=False, indent=2)
    print("全部数据更新成功！")

if __name__ == "__main__":
    fetch_stock_data()
