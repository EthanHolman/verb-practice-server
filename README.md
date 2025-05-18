# verb-practice-server

This is a quick'n'dirty api server for my verb practice mobile app, allowing clients to store and retrieve verb records.

Built with python+flask, sqlite, and gunicorn (in production).

This was just a quick weekend project, and not intended to be well architected or scalable.

## Quickstart

`make install` - will download pip dependencies

`make dev` - starts flask dev server on port 5000

## Docker

Dockerfile and docker-compose is included to make running/deploying simple.

It is recommended to mount a volume for the sqlite database when running in production.
