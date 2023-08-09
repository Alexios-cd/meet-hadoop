# 配置空闲不断开
在某些默认的环境下，使用CRT连接服务器，如果一段时间内不操作连接会自动断开，需要进行设置  

Options->Session Options->Terminal->Anti-idle->勾选Send protocol NO-OP

![img.png](images/img.png)
# 当做sockets隧道使用