# realtime_sentiment
Meip experiment 2020 group 5

## Google Spreadsheet にアクセスするための認証手順
参考: https://qiita.com/connvoi_tyou/items/7cd7ffd5a98f61855f5c

### API credential 作成
1. 次のURLにブラウザからアクセス: https://developers.google.com/sheets/api/quickstart/python?hl=ja#step_1_turn_on_the
2. "Step 1: Turn on the Google Sheets API" セクションの "Enable Google Sheets API" をクリック
3. "Configure your OAuth client" は適当に選択して (Desktop app でいいと思う) "CREATE" をクリック
4. "DOWNLOAD CLIENT CONFIGURATION" をクリックして、 `credentials_sample.json` と同じディレクトリに `credentials.json` の名前で保存する

### config.yml 作成
1. `config_sample.yml` を複製して、ファイル名は `config.yml` とする。
2. 編集したいスプレッドシートのURLのIDを確認する。右の `{SHEET_ID}` の部分の文字列をコピー: `https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit#gid=0`
3. コピーした `SHEET_ID` を `config.yml` に追記する。（`sheet_id: ` のvalueに `SHEET_ID` を入れる）

### 認証する
1. `lib.auth.google_spreadsheet_auth` を呼び出すと、ブラウザが開いて認証画面に遷移する。
2. 認証を済ませるとローカルに認証情報が保存され、それが有効なうちは↑の作業をスキップして認証できる。

※ このステップで生成される `token.pickle` や `credentials.json` は誰にも渡らないように管理すること（認証したアカウントと同じ権限をもつので）。

※ `realtime_sentiment` 直下にこれらの名前で入っていれば、 `.gitignore` で弾いてくれるのでコミットに勝手に含まれることはない。

## cloneしてから実行するまでの手順
1. `pipenv install`を実行する。
2. 上記の手順で認証を済ませる(出力用スプレッドシートのテンプレートはドライブにある)。
3. ドライブにある`model.tar.gz`を`realtime_sentiment/models/serials/xxlarge-bin/model.tar.gz`に保存する。
4. スプレッドシートに入力する。
- グーグルフォームを使う場合：ドライブの入力用フォームのテンプレートを複製し、スプレッドシートと連携させる(参考: https://www.infact1.co.jp/staff_blog/webmarketing/43713/ )。さらに`spreadsheet_text_clumn.py`を実行し、出力用スプレッドシートの`text`の列に`spreadsheet_text_clumn.txt`をコピペする。ただし、`spreadsheet_text_clumn.py`の`シートID`の部分はフォームと連携しているスプレッドシートのシートIDに書き換えて使う。
- グーグルフォームを使わない場合：出力用スプレッドシートの`text`列に直接入力する。
5. `pipenv shell`を実行して仮想環境に入り、`python main.py`を実行する。ただしカレントディレクトリが`realtime_sentiment`の状態で実行する。
