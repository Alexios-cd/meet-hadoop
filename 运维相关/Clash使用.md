# 机场合并技术
clash提供了机场合并技术，相关背景和资料可以参考：[clash 分流规则终极使用方法](https://www.jamesdailylife.com/rule-proxy-provider)

具体参考样例文件 [Clash配置样例文件](clash/1691627412823.yml)

需要注意以下几点：
1. 直接导出的clash订阅链接配置进入使用时提示异常，需要在链接后面加上  &flag=clash 这个好像在高版本的clash中需要这么配置。
2. 如果使用openClash proxy-groups节点下面的 proxies: 要有 DIRECT 否则可能会报错，使用Clash for Windows可以不加
3. 在规则中 RULE-SET,规则集id,手动选择(优选) 一定要是 proxy-groups 配置的，经常手动切换节点的建议选择 类型为select的元素 。