# Playwright環境構築ガイド (Windows)

このガイドでは、Windows環境でPythonの仮想環境を構築し、Playwrightをインストールして使用するまでの手順を説明します。

## 1. Pythonのインストール

まだPythonがインストールされていない場合は、まずPythonをインストールする必要があります。

1.  **Python公式サイトにアクセス:**
    [Python公式ダウンロードページ](https://www.python.org/downloads/windows/)
2.  **インストーラーのダウンロード:**
    最新の安定版Python 3.xの「Windows installer (64-bit)」をダウンロードします。
3.  **インストーラーの実行:**
    ダウンロードした`.exe`ファイルを実行します。
    *   **重要:** インストール開始時に「**Add Python X.Y to PATH**」のチェックボックスを**必ずオン**にしてください。これにより、コマンドプロンプトからPythonが簡単に使えるようになります。
    *   「Install Now」をクリックしてインストールを完了させます。

4.  **インストール確認:**
    コマンドプロンプトを開き、以下のコマンドを実行してPythonが正しくインストールされたか確認します。
    ```bash
    python --version
    pip --version
    ```
    Pythonとpipのバージョンが表示されれば成功です。

## 2. Python仮想環境の構築

プロジェクトごとに独立した環境を構築するために、仮想環境を使用することを強く推奨します。

1.  **プロジェクトディレクトリの作成:**
    任意の場所にプロジェクト用のフォルダを作成し、そのフォルダに移動します。
    例:
    ```bash
    mkdir my_playwright_project
    cd my_playwright_project
    ```

2.  **仮想環境の作成:**
    以下のコマンドを実行して仮想環境を作成します。`venv`は仮想環境の名前です（任意ですが、`venv`が一般的です）。
    ```bash
    python -m venv .venv
    ```

3.  **仮想環境のアクティベート:**
    作成した仮想環境をアクティベートします。これにより、この環境内でインストールされるパッケージは、システム全体のPython環境とは分離されます。
    ```bash
    .\.venv\Scripts\Activate.ps1
    ```
    コマンドプロンプトの表示が `(venv) C:\Users\your_user\my_playwright_project>` のように変われば、アクティベート成功です。

## 3. Playwrightのインストール

仮想環境がアクティベートされた状態で、Playwrightをインストールします。

1.  **Playwrightのインストール:**
    ```bash
    pip install playwright
    ```

2.  **Playwrightブラウザのインストール:**
    Playwrightがサポートするブラウザ（Chromium, Firefox, WebKit）をダウンロードしてインストールします。
    ```bash
    playwright install
    ```
    これにより、必要なブラウザバイナリが自動的にダウンロードされます。

3.  **インストール確認:**
    以下のPythonコードを`test_playwright.py`などのファイルに保存し、実行してPlaywrightが動作するか確認します。

    `test_playwright.py`:
    ```python
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://www.google.com")
        print(page.title())
        browser.close()
    ```

    実行コマンド:
    ```bash
    python test_playwright.py
    ```
    Googleのタイトル（例: "Google"）が表示されれば成功です。

## 4. 仮想環境のディアクティベート

作業が完了したら、以下のコマンドで仮想環境をディアクティベートできます。

```bash
deactivate
```
