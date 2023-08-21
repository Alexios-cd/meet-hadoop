# 简介
CDH（Cloudera Distribution including Apache Hadoop）是一个由Cloudera公司开发和维护的Hadoop生态系统的发行版。CDH集群是一个由多台服务器组成的集群，用于存储、处理和分析大规模数据。

CDH集群包含了以下核心组件：
1. Hadoop HDFS：分布式文件系统，用于存储大规模数据。
2. Hadoop YARN：资源管理系统，用于分配和管理集群中的计算资源。
3. Hadoop MapReduce：分布式计算框架，用于并行处理大规模数据。
4. Hadoop Hive：数据仓库基础架构，用于提供SQL查询和数据聚合功能。
5. Hadoop HBase：分布式数据库，用于存储和访问非结构化数据。
6. Hadoop Spark：快速通用的大数据处理引擎，用于实时数据处理和机器学习。
7. Hadoop Impala：高性能的SQL查询引擎，用于实时查询大规模数据。
8. Hadoop Flume：可靠、可扩展的分布式日志收集和聚合系统。
9. Hadoop Kafka：高吞吐量的分布式消息队列系统，用于实时数据流处理。
10. Hadoop ZooKeeper：分布式协调服务，用于管理和协调集群中的各个组件。

CDH集群提供了一套完整的工具和服务，用于管理、监控和维护集群。它还支持与其他开源工具和技术的集成，如Apache Spark、Apache Kafka等，以满足不同的数据处理和分析需求。

总之，CDH集群是一个强大而灵活的大数据处理平台，可以帮助企业快速搭建和管理大规模数据处理环境，并提供丰富的数据分析和挖掘功能。

# 官方地址
中文版：https://www.clouderacn.cn/  
原版：https://www.cloudera.com/

## 安装地址
在官方网站首页已经很难找到 开源的CDH 安装下载入口，根据官方的描述：
参考链接：[How to download Cloudera Express version 6.3.2](https://community.cloudera.com/t5/Support-Questions/How-to-download-Cloudera-Express-version-6-3-2/m-p/314198)
```shell
Hello 
Cloudera used to offer Express edition for Cloudera Data Hub, aka CDH, e.g. CDH 5.x, 6.x

It is part of the platform binaries, so only if you upload a valid license, you will activate the enterprise features, else you can continue using the Express edition free of charge

Details: https://www.cloudera.com/content/dam/www/marketing/resources/datasheets/cloudera-enterprise-datashee...

Since end of Jan 2021, to download all platform binaries, including CDH 5.x, CDH 6.x, HDP and CDP, you need an active Cloudera subscription, details: https://www.cloudera.com/downloads/paywall-expansion.html

So to answer your question
1. you need an active Cloudera subscription to download
2. if you already have the binaries, i.e. CDH 6.3.2, you can continue using the Express edition free of charge 

你好
Cloudera过去为Cloudera数据中心 (又名CDH) 提供快速版，例如CDH 5.x，6.X

它是平台二进制文件的一部分，因此只有当您上传有效的许可证时，您才会激活企业功能，否则您可以继续免费使用Express edition

详细信息: https://www.cloudera.com/content/dam/www/marketing/resources/datasheets/cloudera-企业-datashee...

自2021年1月结束以来，要下载所有平台二进制文件，包括CDH 5.x, CDH 6.x, HDP和CDP，您需要一个活跃的Cloudera订阅，详细信息: https://www.cloudera.com/downloads/paywall-expansion.html


所以回答你的问题
1.您需要一个活跃的Cloudera订阅才能下载

2.如果您已经拥有二进制文件，即CDH 6.3.2，则可以继续免费使用Express edition
```
需要注册订阅后才能获取相关的安装资料，并且目前开源的仅限于 6.3.x的版本。

如果有二进制可以直接安装。

各种下载链接 [CDH 6 Download Information](https://docs.cloudera.com/documentation/enterprise/6/release-notes/topics/rg_cdh_6_download.html)
## 各种关键入口
1. [CDH6.3.x版本官方下载渠道](https://docs.cloudera.com/documentation/enterprise/6/release-notes/topics/rg_cdh_6_download.html) 
2. [官方安装指南](https://docs.cloudera.com/documentation/enterprise/6/6.3/topics/installation.html)
3. [CDH默认端口](https://docs.cloudera.com/documentation/enterprise/6/6.3/topics/cdh_ports.html)
4. [服务依赖关系](https://docs.cloudera.com/documentation/enterprise/6/6.3/topics/cm_ig_service_dependencies.html)
5. [CDH里面各个组件版本](https://docs.cloudera.com/documentation/enterprise/6/release-notes/topics/rg_cdh_63_packaging.html)


