cd /home/yjt/identify_express_via_waybillno/ && git pull && \
docker ps -a | grep identify_express_via_waybillno | awk '{print $1}' | xargs docker rm -f && \

sudo docker run --name identify_express_via_waybillno \
-v /home/yjt/identify_express_via_waybillno/:/identify_express_via_waybillno/  \
-v /root/.ssh/:/root/.ssh/ \
-p 8150:8150 \
-d --privileged=true \
--restart=always \
registry.cn-hangzhou.aliyuncs.com/docker-gnosis/identify_express_via_waybillno:v1.1 \
sh /identify_express_via_waybillno/startup.sh

sudo docker run --name identify_express_via_waybillno_1 \
-v /home/yjt/identify_express_via_waybillno/:/identify_express_via_waybillno/  \
-v /root/.ssh/:/root/.ssh/ \
-p 8151:8150 \
-d --privileged=true \
--restart=always \
registry.cn-hangzhou.aliyuncs.com/docker-gnosis/identify_express_via_waybillno:v1.1 \
sh /identify_express_via_waybillno/startup.sh

sudo docker run --name identify_express_via_waybillno_2 \
-v /home/yjt/identify_express_via_waybillno/:/identify_express_via_waybillno/  \
-v /root/.ssh/:/root/.ssh/ \
-p 8152:8150 \
-d --privileged=true \
--restart=always \
registry.cn-hangzhou.aliyuncs.com/docker-gnosis/identify_express_via_waybillno:v1.1 \
sh /identify_express_via_waybillno/startup.sh

sudo docker run --name identify_express_via_waybillno_3 \
-v /home/yjt/identify_express_via_waybillno/:/identify_express_via_waybillno/  \
-v /root/.ssh/:/root/.ssh/ \
-p 8153:8150 \
-d --privileged=true \
--restart=always \
registry.cn-hangzhou.aliyuncs.com/docker-gnosis/identify_express_via_waybillno:v1.1 \
sh /identify_express_via_waybillno/startup.sh