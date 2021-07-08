# Traffic Light

## Introduction

此專案目的為提供一套後台系統，用於控制紅綠燈並監控營運狀態，可分為以下功能模組，也可參考[架構](https://hackmd.io/@kuochuwon/SJm_rVfo_)

* 裝置管理 (Device)

* 裝置群組管理 (Device group)

* 用戶管理 (Account)

* 用戶群組管理 (Account group)

* 認證管理 (Auth)

## 自行設定.env

```python
# In development environment
FLASK_CONFIG=development

# Database configuration for production environment
DATABASE_URL=postgresql+psycopg2://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>

# Database configuration for development environment
DEV_DATABASE_URL=postgresql+psycopg2://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>

# Database configuration for unittest
TEST_DATABASE_URL=postgresql+psycopg2://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>

# Web/JWT key
WEB_SECRET_KEY=<your_secret_key>
JWT_SECRET_KEY=<your_secret_key>

# access token expired in X minutes
JWT_ACCESS_TOKEN_EXPIRES = <expire minutes>
# refresh token expired in X days
JWT_REFRESH_TOKEN_EXPIRES = <expire days>

# log directory must be created first
LOG_FILE=log/lighting.log

# MQTT setting for publish module, mainly offer for command api.
MQTT_CLIENT_ID = <client_id>
MQTT_ALIVE = <alive seconds>
MQTT_SERVER = <server_host>
MQTT_PORT = <port_number>

# If publish topic of command change, gateway command need change too.
MQTT_PUBLISH_TOPIC = main_path/sub_path1/subpath2/...
MQTT_QOS = 0
```

## Build

```python
python -m venv venv

# windows
.\venv\Scripts\activate

# mac/linux
source venv/bin/activate
```

```python
python -m pip install pip --upgrade
python -m pip install setuptools --upgrade
pip install flake8
pip install autopep8
pip install rope
```



## Run

```python
python manage.py run
```

## Run test

```python
python manage.py test
```

## Initial database configuration

```python
python manage.py db init
```

## 確認目前使用中的資料庫版本(專案/資料庫)
## 同步專案與資料庫的版本資訊(以專案為優先)

```python
python manage.py db current
python manage.py db heads
python manage.py db stamp heads
```

## Prepare database migration

```python
python manage.py db migrate -m "<comment>"
```

## Do database migration

```python
python manage.py db upgrade
```

## Undo database migration

 ```python
python manage.py db downgrade
```

## Publish initial data

```python
python manage.py seed
```

## check_access_authority的運作原理
* 先取得user的資訊，根據user id找出user所屬的user group
* 根據user group找出該gruop所屬的role，以及該role可訪問的routes，例如: getall, getdetail... etc
* 若該user所打的API route在可訪問的routes中，就開放使用

## convert_null_emptystr的運作原理
由於先前專案曾遇到一個困難，在前後端的協作情境，有時會遇到需處理NULL的情況，當後端不希望接收到NULL以免產生預期以外的錯誤，，但又不得不處理NULL時(例如前端呼叫API，API沒有找到相應結果，而回傳NULL)，此時我們將回傳的NULL進行處理，將NULL轉換為空字串。
* 為了降低函式複雜度，用遞迴實現
* 接收到回傳的JSON物件時，透過for loop檢查每一層的內容是否含有NULL
* 若含有NULL就替換為空字串，若JSON的key底下還有一層JSON，遞迴呼叫原函式處理
* 若已經抵達最底層，就結束

## aaa_verify的運作原理
* 解碼應用JWT技術產生的Token
* 還原Token中夾帶的cust_id, vendor_id等使用者資訊
* query db中的customer table，比對夾帶的cust_id是否在customer table中
* 若不在table中，就拋出一個例外並結束程式
