# proxy-chat-api

各種LLMへのアクセスを中継するサーバーの実装です。
OpenAIのAPI形式を採用しています。
https://platform.openai.com/docs/api-reference/introduction

## TODO:
- [x] support openai
- [x] support fireworks.ai
- [x] /v1/models
- [x] /v1/chat/completions
- [ ] /v1/completions

## 使用方法
.envに各種パラメータを設定します。
```
$ cp env.example .env
$ vim .env
```

docker composeで立ち上げるとポート番号8080でアクセスできます。
```
$ docker compose up -d
$ curl https://localhost:8080/v1/models -H "Content-Type: application/json" -H "Authorization: Bearer <SECRET_TOKEN>"
```

サーバーを停止する場合は下記コマンドで停止できます。
```
$ docker compose down
```

ドメインを利用する場合は.envにAPI_HOSTを設定後、traefikを立ち上げてください。
```
$ docker compose -f traefik.yml up -d
```

traefikを停止する場合は下記コマンドで停止できます。
```
$ docker compose -f traefik.yml down
```
