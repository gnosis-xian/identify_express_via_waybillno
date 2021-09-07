# 通过运单号识别所属快递公司（identify_express_via_waybillno）

## 通过运单号识别所属快递公司
基于TF-IDF

## 请求示例
```http request
http://waybill-identify.test.api.elrsp.com/identify/detail/waybillno?waybillno=YT2145335310152
```
响应：
```json
[
    {
        "express_code":"yuantong",
        "prob_percentage":0.40485092997550964
    }
]
```

## Quick startup with docker
```shell
sudo docker run --name identify_express_via_waybillno \
-v /home/yjt/identify_express_via_waybillno/:/identify_express_via_waybillno/  \
-v /root/.ssh/:/root/.ssh/ \
-p 8150:8150 \
-d --privileged=true \
--restart=always \
registry.cn-hangzhou.aliyuncs.com/docker-gnosis/identify_express_via_waybillno:v1.1 \
sh /identify_express_via_waybillno/startup.sh
```

## Quick start with python3.8

### 1. Create python3.8 environment.
### 2. Install with pip.
```shell
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```
### 3. startup with python.
```shell
python controller.py
```