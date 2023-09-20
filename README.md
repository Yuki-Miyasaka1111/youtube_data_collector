# Youtube Data Collector

Youtube Data APIを使用して指定したチャンネルの動画情報を取得する

## 起動方法

dockerコンテナの起動

```
docker compose build
docker compose up -d
```

フロントエンド

```
cd client
npm start
```

バックエンド

```
source venv/bin/activate
uvicorn main:app --reload --port 8001
```
