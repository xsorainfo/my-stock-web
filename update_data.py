import json
import yfinance as yf

# 1. 升级版自选股清单：直接写好行业和盈利特色
WATCHLIST = {
    "5817.T": {
        "name": "JMACS",
        "industry": "通信与电子设备",
        "feature": "主攻AI图像识别与工业自动化控制系统"
    },
    "3110.T": {
        "name": "日東紡績",
        "industry": "玻璃纤维与材料",
        "feature": "全球高频半导体基板用「超薄玻璃纤维布」垄断级巨头"
    },
    "5803.T": {
        "name": "フジクラ",
        "industry": "电线电缆与光纤",
        "feature": "AI数据中心核心部件「高密度光缆」关键供应商"
    }
}

def fetch_stock_data():
    updated_list = []
    
    for symbol, meta in WATCHLIST.items():
        try:
            print(f"正在抓取 {meta['name']} ({symbol})...")
            stock = yf.Ticker(symbol)
            info = stock.info
            
            # 价格与涨跌
            current_price = info.get('currentPrice') or info.get('regularMarketPrice')
            prev_close = info.get('previousClose')
            
            if current_price and prev_close:
                diff = current_price - prev_close
                percent = (diff / prev_close) * 100
                sign = "+" if diff > 0 else ""
                change_str = f"{sign}{diff:.2f} ({sign}{percent:.2f}%)"
                is_up = diff > 0
            else:
                change_str = "--"
                is_up = False
                
            # PER 标签逻辑
            per = info.get('forwardPE') or info.get('trailingPE') or "--"
            per_display = f"{per:.2f}" if isinstance(per, (int, float)) else str(per)
            if isinstance(per, (int, float)):
                if per < 0: per_display += " (亏损)"
                elif per < 15.0: per_display += " (低估)"
                elif per < 35.0: per_display += " (合理)"
                else: per_display += " (偏高)"
                
            # PBR 标签逻辑
            pbr = info.get('priceToBook') or "--"
            pbr_display = f"{pbr:.2f}" if isinstance(pbr, (int, float)) else str(pbr)
            if isinstance(pbr, (int, float)):
                if pbr < 1.0: pbr_display += " (低估)"
                elif pbr <= 3.0: pbr_display += " (合理)"
                else: pbr_display += " (偏高)"

            # 把行业和特色一起打包塞进 json
            updated_list.append({
                "code": symbol.split('.')[0],
                "name": meta['name'],
                "industry": meta['industry'],
                "feature": meta['feature'],
                "price": current_price,
                "change": change_str,
                "isUp": is_up,
                "per": per_display,
                "pbr": pbr_display
            })
        except Exception as e:
            print(f"{meta['name']} 抓取失败: {e}")
            
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(updated_list, f, ensure_ascii=False, indent=2)
    print("全部数据更新成功！")

if __name__ == "__main__":
    fetch_stock_data()
