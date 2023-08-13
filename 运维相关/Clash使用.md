# 机场合并技术
clash提供了机场合并技术，相关背景和资料可以参考：[clash 分流规则终极使用方法](https://www.jamesdailylife.com/rule-proxy-provider)

具体参考样例文件 [Clash配置样例文件](clash/1691627412823.yml)

需要注意以下几点：
1. 直接导出的clash订阅链接配置进入使用时提示异常，需要在链接后面加上  &flag=clash 这个好像在高版本的clash中需要这么配置。
2. 如果使用openClash proxy-groups节点下面的 proxies: 要有 DIRECT 否则可能会报错，使用Clash for Windows可以不加
3. 在规则中 RULE-SET,规则集id,手动选择(优选) 一定要是 proxy-groups 配置的，经常手动切换节点的建议选择 类型为select的元素 。

# V2rayA 
## 介绍
一个易用而强大的，跨平台的 V2Ray 客户端。你可通过本节对用户文档的内容进行快速预览。  
官方文档：[https://v2raya.org/docs/prologue/introduction/](https://v2raya.org/docs/prologue/introduction/)
## V2rayA在 Ubuntu 安装
以下内容全程参考：[V2rayA/安装/DebianUbuntu安装](https://v2raya.org/docs/prologue/installation/debian/)
### 第一步：安装 V2Ray 内核
v2rayA 的功能依赖于 V2Ray 内核，因此需要安装 V2Ray 内核。    
建议使用V2Ray官方内核： [v2fly/fhs-install-v2ray](https://github.com/v2fly/fhs-install-v2ray)  
官方简体中文参考链接：[fhs-install-v2ray/blob/master/README.zh-Hans-CN.md](https://github.com/v2fly/fhs-install-v2ray/blob/master/README.zh-Hans-CN.md)
```shell
// 请注意：以下链接需要访问github才可以安装成功，请确保网络。
// 安装可执行文件和 .dat 数据文件
# bash <(curl -L https://raw.githubusercontent.com/v2fly/fhs-install-v2ray/master/install-release.sh)
```
安装后可以关掉服务，因为 v2rayA 不依赖于该 systemd 服务,只是使用v2ray内核执行文件。
```shell
sudo systemctl disable v2ray --now
```

### 第二步：安装V2rayA

以下命令运行就好，深究无用

```shell
# 添加公钥
wget -qO - https://apt.v2raya.org/key/public-key.asc | sudo tee /etc/apt/trusted.gpg.d/v2raya.asc
# 添加V2rayA软件源
echo "deb https://apt.v2raya.org/ v2raya main" | sudo tee /etc/apt/sources.list.d/v2raya.list
sudo apt update
# 安装V2RayA
sudo apt install v2raya
```

### 第三步：启动 v2rayA / 设置 v2rayA 自动启动

```shell
# 启动 v2rayA
sudo systemctl start v2raya.service
# 设置开机自动启动
sudo systemctl enable v2raya.service

```



