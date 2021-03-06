﻿# APITEST

标签（空格分隔）： 接口文档

---
[TOC]
----
### 1.用户登陆

> **url: http://localhost:5000/api/login**
>
> **methods:GET**
>
> **Content-Type:application/json**

#### 入参
[//]:param
```json
{
  "user_name":"admin",
  "pwd":123
}
```
[//]:param

#### 回参
##### True:
[//]:True-response
```json
{
    "code": 200, 
    "data": {"code": 100, "token": "no-need-confirm"}, 
    "msg": "ok"
}
```
[//]:True-response

##### False:
[//]:False-response
```json
{
    "code": 400, 
    "data": {}, 
    "msg": "some-exception"
}
```
[//]:False-response

----

### 2.用户登陆

> **url: http://localhost:5000/api/login**
>
> **methods:POST**
>
> **Content-Type:application/json**

#### 入参
[//]: param
```json
{
  "user_name":"admin",
  "pwd":123
}
```
[//]: param


#### 回参
##### True:
[//]:True-response
```json
{
    "code": 200, 
    "data": {"code": 100, "token": "no-need-confirm"}, 
    "msg": "ok"
}
```
[//]:True-response

##### False:
[//]:False-response
```json
{
    "code": 400, 
    "data": {}, 
    "msg": "some-exception"
}
```
[//]:False-response

----
### 3.用户登陆GET

> **url: http://localhost:5000/api/login_get**
>
> **methods:GET**

#### 入参
[//]: param
```text
{
  "user_name":"admin",
  "pwd":123
}
```
[//]: param

#### 回参
##### True:
[//]:True-response
```json
{
    "code": 200, 
    "data": {"u_code": 100, "token": "no-need-confirm"}, 
    "msg": "ok"
}
```
[//]:True-response

##### False:
[//]:False-response
```json
{
    "code": 400, 
    "data": {}, 
    "msg": "user_name or pwd wrong"
}
```
[//]:False-response

----