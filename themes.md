# Темы 

Возможные темы для будущего обзора:

1. Классы-итераторы и генераторы в Python
2. API rest клиенты
3. Руководство по использованию интернета для пожилых людей

## Local Clickhouse Server

```shell
# server
docker run \
    -v "$PWD/clickhouse/data:/var/lib/clickhouse/" \
    -v "$PWD/clickhouse/logs:/var/log/clickhouse-server/" \
    -p 18123:8123 -p 19000:9000 \
    -e CLICKHOUSE_PASSWORD=123 \
    --name some-clickhouse-server --ulimit nofile=262144:262144 clickhouse/clickhouse-server
    
# client
docker exec -it some-clickhouse-server clickhouse-client
```