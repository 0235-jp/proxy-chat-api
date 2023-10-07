# proxy-chat-api
[README_JP](https://github.com/KoheiYamashita/proxy-chat-api/blob/main/README_JP.md)

This is an implementation of a server that relays access to various LLMs.
It uses OpenAI API format.
https://platform.openai.com/docs/api-reference/introduction

## TODO:
- [x] support openai
- [x] support fireworks.ai
- [x] /v1/models
- [x] /v1/chat/completions
- [ ] /v1/completions

## Usage
Set various parameters in .env.
```
$ cp env.example .env
$ vim .env
```

If you start up with docker compose, you can access it on port 8080.
```
$ docker compose up -d
$ curl https://localhost:8080/v1/models -H "Content-Type: application/json" -H "Authorization: Bearer <SECRET_TOKEN>"
```

If you want to stop the server, you can use the following command.
```
$ docker compose down
```

If you want to use a domain, set API_HOST in .env and start up traefik.
```
$ docker compose -f traefik.yml up -d
```

If you want to stop traefik, you can use the following command.
```
$ docker compose -f traefik.yml down
```
