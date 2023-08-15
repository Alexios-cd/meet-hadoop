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

# ForgeMC私服搭建

官网地址：https://files.minecraftforge.net/net/minecraftforge/forge/

下载后安装

```shell
# 命令行安装
java -jar forge-1.12.2-installer.jar nogui --installServer
```

# 推荐mod

## 小地图下载

Xaero's Minimap Download https://chocolateminecraft.com/minimapdownload.php

## 大地图下载

Xaero's World Map Download

https://chocolateminecraft.com/worldmapdownload.php

## 一键整理

Inventory Profiles Next

https://www.curseforge.com/minecraft/mc-mods/inventory-profiles-next/files

libIPN

https://www.curseforge.com/minecraft/mc-mods/libipn/files

fabric-language-[kotlin]()

https://www.curseforge.com/minecraft/mc-mods/fabric-language-kotlin

## 自动钓鱼

Autofish

https://www.curseforge.com/minecraft/mc-mods/autofish/files

AutoFish for Forge

https://www.curseforge.com/minecraft/mc-mods/autofish-for-forge/files

## 暮色深林

https://www.curseforge.com/minecraft/mc-mods/the-twilight-forest/files