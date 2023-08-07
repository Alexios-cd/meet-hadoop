# 综述

# PaperMC私服搭建
以下搭建基于centos
下载安装网址：
https://papermc.io/downloads
安装：

## 先执行命名
```shell
java -jar paper-xxx.jar nogui
```
```shell
# 如果以上命令下载命令慢，可以使用代理
java17 -Dhttp.proxyHost=192.168.50.99 \
-Dhttp.proxyPort=9999 \
-Dhttps.proxyHost=192.168.50.99 \
-Dhttps.proxyPort=9999 \
-jar paper-xxx.jar
```
然后等待经济和基础依赖jar下载完成
## 再次启动
```shell
java -jar paper-xxx.jar nogui
```

 修改协议文件eula.txt，同意协议

 按需修改server.properties文件，online-mode 修改为false(允许盗版登录)

## 最后启动
```shell
java -jar paper-xxx.jar nogui
```

## 备份脚本(非必须，需要回档的话可以使用)
```shell

#!/bin/bash
starttime=`date +'%Y-%m-%d %H:%M:%S'`
DATE=$(date +%Y-%m-%d_%H-%M-%S)
echo "开始时间：" $(date +"%Y-%m-%d %H:%M:%S")
zip -r /data/paper_mc_back/"$DATE.zip" /opt/paper_mc
echo "结束时间：" $(date +"%Y-%m-%d %H:%M:%S")
endtime=`date +'%Y-%m-%d %H:%M:%S'`
start_seconds=$(date --date="$starttime" +%s);
end_seconds=$(date --date="$endtime" +%s);
echo "本次备份耗时： "$((end_seconds-start_seconds))"秒"
```