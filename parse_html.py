import pandas as pd
import time
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

# --- 設定 ---
BASE_URL = "https://nanyo-city.jpn.org/prompt/{}.html"
START_ID = 100
END_ID = 700
OUTPUT_FILE = "nanyo_prompts.csv"

# カラム定義（URLを最初に追加）
COLUMNS = ["URL"] + [
    "目的・ねらい", "あなたの役割", "前提条件", "評価の基準", "明確化の要件", 
    "リソース", "実行指示", "出力形式", "問題の内容", 
    "希望する結末", "補足"
]

def fetch_page_content(browser, url):
    page = browser.new_page()
    try:
        # タイムアウトを30秒に設定
        response = page.goto(url, timeout=30000)
        if not response or response.status == 404:
            return None
        
        page.wait_for_load_state("networkidle")
        return page.content()
    except Exception as e:
        print(f"\n[Error] {url}: {e}")
        return None
    finally:
        page.close()



def parse_prompt_data(html, url):
    soup = BeautifulSoup(html, "html.parser")
    
    # URLを最初に入れて初期化
    data = {col: "" for col in COLUMNS}
    data["URL"] = url
    
    # 「目的・ねらい」を別途取得するためにカラムリストに追加して探す
    # ※もしCOLUMNSに「目的・ねらい」が入っていなければ追加してください
    target_keys = COLUMNS + ["目的・ねらい"]
    
    boxes = soup.find_all("div", class_="box-bun")
    found_any = False

    for box in boxes:
        h2 = box.find("h2")
        if not h2:
            continue
            
        key = h2.get_text(strip=True)
        
        if key in target_keys:
            # 1. まず textarea を探す
            textarea = box.find("textarea")
            if textarea:
                content = textarea.get_text(strip=True)
            else:
                # 2. textarea がない場合は、h2 以外のテキスト部分を取得
                # box全体から h2 のテキストを除去して残りを取得する
                content = box.get_text(separator="\n", strip=True).replace(key, "", 1).strip()
            
            # 抽出したデータを保存（COLUMNSに存在するキーのみ）
            if key in data:
                data[key] = content
                found_any = True
            # もし「目的・ねらい」を別のカラム（例: 補足など）に入れたい場合はここで調整
            elif key == "目的・ねらい":
                # 今回は「補足」などの既存カラムに入れるか、COLUMNSに項目を追加してください
                data["目的・ねらい"] = content 

    return data if found_any else None



def main():
    results = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        print(f"スクレイピングを開始します (1 to {END_ID})")
        
        for i in range(START_ID, END_ID + 1):
            url = BASE_URL.format(i)
            print(f"[{i}/{END_ID}] Checking: {url}...", end=" ", flush=True)
            
            html = fetch_page_content(browser, url)
            
            if html:
                prompt_data = parse_prompt_data(html, url)
                if prompt_data:
                    results.append(prompt_data)
                    print("Found!")
                else:
                    print("No target table.")
            else:
                print("Skip (404/Error).")
            
            # --- バックアップ処理: 10件ごとに保存 ---
            if len(results) > 0 and len(results) % 10 == 0:
                pd.DataFrame(results).to_csv(OUTPUT_FILE, index=False, encoding="utf-16", sep="\t")
            
            # サーバーに優しく（1秒待機）
            # time.sleep(1)
        
        browser.close()

    # --- 最終保存 ---
    if results:
        df = pd.DataFrame(results)
        # カラムの順番を固定して保存
        df = df.reindex(columns=COLUMNS)
        df.to_csv(OUTPUT_FILE, index=False, encoding="utf-16", sep="\t")
        print(f"\n完了！合計 {len(results)} 件のデータを {OUTPUT_FILE} に保存しました。")
    else:
        print("\nデータが1件も見つかりませんでした。")

if __name__ == "__main__":
    main()