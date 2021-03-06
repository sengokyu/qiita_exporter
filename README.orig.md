# はじめに  
国内のエンジニアのほぼ100%が云々とか雑なことを言ったり、コンプライアンス的にやばそうなことをやってお気持ちの問題で済ませるサービスに依存するのは、リスクだと思うので現在の記事をGitHubに移行する方法を検討します。  
  
なお、私の記事は以下のようになりました。  
https://github.com/mima3/note  
  
  
# 動作環境  
Python 3.7.4  
Windows10  
  
# 事前準備  
Qiitaのアクセストークンを取得します。  
  
(1)設定画面のアプリケーションタブから「新しいトークンを発行する」を押下します。  
  
![image.png](https://qiita-image-store.s3.amazonaws.com/0/47856/1027591c-3943-b695-c493-615457408997.png)  
  
(2)読み取り権限を付けて「発行」を押下します  
![image.png](https://qiita-image-store.s3.amazonaws.com/0/47856/cc957b75-91f7-9f5e-7fd8-2be56c38061f.png)  
  
(3)アクセストークンをメモしておきます  
![image.png](https://qiita-image-store.s3.amazonaws.com/0/47856/d28c2a4f-19a6-6255-7e30-3d1bbfaf2d42.png)  
  
# 使用方法  
(1)以下のリポジトリからスクリプトを取得する  
https://github.com/mima3/qiita_exporter  
  
(2)下記の形式でスクリプトを実行する。  
  
```
python qiita_to_github.py [userid] [accesstoken] [保存先フォルダ] [GitHubのブロブのルートURL ex.https://github.com/mima3/note/blob/master]  
```  
  
(3)保存先フォルダをGitHubに登録します。  
  
# やっていること  
・画像をローカルにダウロードして、リンクを書き換えます。  
・コードブロック以外の行にて、改行コードの前にスペース2ついれて改行を行います。  
・「#タイトル」という記述があったら「# タイトル」に直します。  
・コードブロックのタイトル（例：「```python:test.py」）が表示されないので対応します。  
・自分の記事へのURLを修正する  
  
  
# 課題  
・タグとかの表現をどうするか。  
・コメントとかの取り扱いをどうするか。  
・既存の記事に移行先を入れる方法とか。  
  
