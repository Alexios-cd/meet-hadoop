# 目标

1. 梳理常见的表模型
2. 梳理常用的运维命令
3. 新建只读用户，配置Granfana表信息监控
4. 梳理分区，分桶相关操作
5. 梳理采集任务相关命令，查看，配置，取消等

# 表设计

参考链接: [表设计](https://docs.starrocks.io/zh-cn/2.5/table_design/StarRocks_table_design)

## 数据模型

StarRocks 支持四种数据模型，分别是明细模型 (Duplicate Key Model)、聚合模型 (Aggregate Key Model)、更新模型 (Unique Key Model) 和主键模型 (Primary Key Model)。这四种数据模型能够支持多种数据分析场景，例如日志分析、数据汇总分析、实时分析等。

数据导入至使用某个数据模型的表，会按照建表时指定的一列或多列排序后存储，这部分用于排序的列就称为排序键。排序键通常为查询时过滤条件频繁使用的一个或者多个列，用以加速查询。

| 模型     | 排序键              | 特点                           |
| -------- | ------------------- | ------------------------------ |
| 明细模型 | DUPLICATE KEY       | 排序键不需要满足唯一性约束     |
| 聚合模型 | AGGREGATE KEY       | 排序键需要满足唯一性约束       |
| 更新模型 | UNIQUE KEY REPLACE  | 排序键需要满足唯一性约束       |
| 主键模型 | PRIMARY KEY REPLACE | 排序键需要满足唯一性和非空约束 |

### 明细模型

#### 适用场景

- 分析原始数据，例如原始日志、原始操作记录等。
- 查询方式灵活，不需要局限于预聚合的分析方式。
- 导入日志数据或者时序数据，主要特点是旧数据不会更新，只会追加新的数据。

#### 建表语句

```sql
-- 例如，需要分析某时间范围的某一类事件的数据，则可以将事件时间（event_time）和事件类型（event_type）作为排序键。
CREATE TABLE IF NOT EXISTS detail (
    event_time DATETIME NOT NULL COMMENT "datetime of event",
    event_type INT NOT NULL COMMENT "type of event",
    user_id INT COMMENT "id of user",
    device_code INT COMMENT "device code",
    channel INT COMMENT ""
)
DUPLICATE KEY(event_time, event_type)
DISTRIBUTED BY HASH(user_id) BUCKETS 8
PROPERTIES (
"replication_num" = "3"
);
```

> 建表时必须使用 `DISTRIBUTED BY HASH` 子句指定分桶键。分桶键的更多说明，请参见[分桶](https://docs.starrocks.io/zh-cn/2.5/table_design/Data_distribution/#分桶)。

#### 使用说明

- 排序键的相关说明：

  - 在建表语句中，排序键必须定义在其他列之前。

  - 排序键可以通过 `DUPLICATE KEY` 显式定义。本示例中排序键为 `event_time` 和 `event_type`。

    > 如果未指定，则默认选择表的前三列作为排序键。

  - 明细模型中的排序键可以为部分或全部维度列。

- 建表时，支持为指标列创建 BITMAP、Bloom Filter 等索引。

### 聚合模型

#### 适用场景

适用于分析统计和汇总数据。比如:

- 通过分析网站或 APP 的访问流量，统计用户的访问总时长、访问总次数。
- 广告厂商为广告主提供的广告点击总量、展示总量、消费统计等。
- 通过分析电商的全年交易数据，获得指定季度或者月份中，各类消费人群的爆款商品。

在这些场景中，数据查询和导入，具有以下特点：

- 多为汇总类查询，比如 SUM、MAX、MIN等类型的查询。
- 不需要查询原始的明细数据。
- 旧数据更新不频繁，只会追加新的数据。

#### 建表语句

```sql
-- 例如需要分析某一段时间内，来自不同城市的用户，访问不同网页的总次数。
-- 则可以将网页地址 site_id、日期 date 和城市代码 city_code 作为排序键，将访问次数 pv 作为指标列，并为指标列 pv 指定聚合函数为 SUM。
CREATE TABLE IF NOT EXISTS example_db.aggregate_tbl (
    site_id LARGEINT NOT NULL COMMENT "id of site",
    date DATE NOT NULL COMMENT "time of event",
    city_code VARCHAR(20) COMMENT "city_code of user",
    pv BIGINT SUM DEFAULT "0" COMMENT "total page views"
)
AGGREGATE KEY(site_id, date, city_code)
DISTRIBUTED BY HASH(site_id) BUCKETS 8
PROPERTIES (
"replication_num" = "3"
);
```

> 建表时必须使用 `DISTRIBUTED BY HASH` 子句指定分桶键。分桶键的更多说明，请参见[分桶](https://docs.starrocks.io/zh-cn/2.5/table_design/Data_distribution/#分桶)。

#### 使用说明

- 排序键的相关说明：

  - 在建表语句中，**排序键必须定义在其他列之前**。

  - 排序键可以通过 `AGGREGATE KEY` 显式定义。

    > - 如果 `AGGREGATE KEY` 未包含全部维度列（除指标列之外的列），则建表会失败。
    > - 如果不通过 `AGGREGATE KEY` 显示定义排序键，则默认除指标列之外的列均为排序键。

  - 排序键必须满足唯一性约束，必须包含全部维度列，并且列的值不会更新。

- 指标列：通过在列名后指定聚合函数，定义该列为指标列。一般为需要汇总统计的数据。

- 聚合函数：指标列使用的聚合函数。聚合模型支持的聚合函数，请参见 [CREATE TABLE](https://docs.starrocks.io/zh-cn/2.5/sql-reference/sql-statements/data-definition/CREATE TABLE)。

- 查询时，排序键在多版聚合之前就能进行过滤，而指标列的过滤在多版本聚合之后。因此建议将频繁使用的过滤字段作为排序键，在聚合前就能过滤数据，从而提升查询性能。

- 建表时，不支持为指标列创建 BITMAP、Bloom Filter 等索引。

### 更新模型

#### 适用场景

实时和频繁更新的业务场景，例如分析电商订单。在电商场景中，订单的状态经常会发生变化，每天的订单更新量可突破上亿。

#### 建表语句

```sql
-- 在电商订单分析场景中，经常按照日期对订单状态进行统计分析
-- 则可以将经常使用的过滤字段订单创建时间 create_time、订单编号 order_id 作为主键，其余列订单状态 order_state 和订单总价 total_price 作为指标列。
-- 这样既能够满足实时更新订单状态的需求，又能够在查询中进行快速过滤。
CREATE TABLE IF NOT EXISTS orders (
    create_time DATE NOT NULL COMMENT "create time of an order",
    order_id BIGINT NOT NULL COMMENT "id of an order",
    order_state INT COMMENT "state of an order",
    total_price BIGINT COMMENT "price of an order"
)
UNIQUE KEY(create_time, order_id)
DISTRIBUTED BY HASH(order_id) BUCKETS 8
PROPERTIES (
"replication_num" = "3"
); 
```

> 建表时必须使用 `DISTRIBUTED BY HASH` 子句指定分桶键。分桶键的更多说明，请参见[分桶](https://docs.starrocks.io/zh-cn/2.5/table_design/Data_distribution/#分桶)。

#### 使用说明

- 主键的相关说明：
  - 在建表语句中，主键必须定义在其他列之前。
  - 主键通过 `UNIQUE KEY` 定义。
  - 主键必须满足唯一性约束，且列的值不会修改。
  - 设置合理的主键。
    - 查询时，主键在聚合之前就能进行过滤，而指标列的过滤通常在多版本聚合之后，因此建议将频繁使用的过滤字段作为主键，在聚合前就能过滤数据，从而提升查询性能。
    - 聚合过程中会比较所有主键，因此需要避免设置过多的主键，以免降低查询性能。如果某个列只是偶尔会作为查询中的过滤条件，则不建议放在主键中。
- 建表时，不支持为指标列创建 BITMAP、Bloom Filter 等索引。

### 主键模型

#### 适用场景

主键模型适用于实时和频繁更新的场景，例如：

- **实时对接事务型数据至 StarRocks**。事务型数据库中，除了插入数据外，一般还会涉及较多更新和删除数据的操作，因此事务型数据库的数据同步至 StarRocks 时，建议使用主键模型。[通过 Flink-CDC 等工具直接对接 TP 的 Binlog](https://docs.starrocks.io/zh-cn/2.5/loading/Flink_cdc_load)，实时同步增删改的数据至主键模型，可以简化数据同步流程，并且相对于 Merge-On-Read 策略的更新模型，查询性能能够提升 3~10 倍。
- **利用部分列更新轻松实现多流 JOIN**。在用户画像等分析场景中，一般会采用大宽表方式来提升多维分析的性能，同时简化数据分析师的使用模型。而这种场景中的上游数据，往往可能来自于多个不同业务（比如来自购物消费业务、快递业务、银行业务等）或系统（比如计算用户不同标签属性的机器学习系统），主键模型的部分列更新功能就很好地满足这种需求，不同业务直接各自按需更新与业务相关的列即可，并且继续享受主键模型的实时同步增删改数据及高效的查询性能。

#### 建表语句

```sql
-- 例如，需要按天实时分析订单，则可以将时间 dt、订单编号 order_id 作为主键，其余列为指标列。建表语句如下：
create table orders (
    dt date NOT NULL,
    order_id bigint NOT NULL,
    user_id int NOT NULL,
    merchant_id int NOT NULL,
    good_id int NOT NULL,
    good_name string NOT NULL,
    price int NOT NULL,
    cnt int NOT NULL,
    revenue int NOT NULL,
    state tinyint NOT NULL
) PRIMARY KEY (dt, order_id)
PARTITION BY RANGE(`dt`) (
    PARTITION p20210820 VALUES [('2021-08-20'), ('2021-08-21')),
    PARTITION p20210821 VALUES [('2021-08-21'), ('2021-08-22')),
    PARTITION p20210929 VALUES [('2021-09-29'), ('2021-09-30')),
    PARTITION p20210930 VALUES [('2021-09-30'), ('2021-10-01'))
) DISTRIBUTED BY HASH(order_id) BUCKETS 4
PROPERTIES (
    "replication_num" = "3",
    "enable_persistent_index" = "true"
);
```

> 建表时必须使用 `DISTRIBUTED BY HASH` 子句指定分桶键。分桶键的更多说明，请参见[分桶](https://docs.starrocks.io/zh-cn/2.5/table_design/Data_distribution/#分桶)。

```sql
-- 例如，需要实时分析用户情况，则可以将用户 ID user_id 作为主键，其余为指标列。建表语句如下：
create table users (
    user_id bigint NOT NULL,
    name string NOT NULL,
    email string NULL,
    address string NULL,
    age tinyint NULL,
    sex tinyint NULL,
    last_active datetime,
    property0 tinyint NOT NULL,
    property1 tinyint NOT NULL,
    property2 tinyint NOT NULL,
    property3 tinyint NOT NULL
) PRIMARY KEY (user_id)
DISTRIBUTED BY HASH(user_id) BUCKETS 4
PROPERTIES (
    "replication_num" = "3",
    "enable_persistent_index" = "true"
);
```

> 建表时必须使用 `DISTRIBUTED BY HASH` 子句指定分桶键。分桶键的更多说明，请参见[分桶](https://docs.starrocks.io/zh-cn/2.5/table_design/Data_distribution/#分桶)。

#### 使用说明

- 主键相关的说明：

  - 在建表语句中，主键必须定义在其他列之前。
  - 主键通过 `PRIMARY KEY` 定义。
  - 主键必须满足唯一性约束，且列的值不会修改。本示例中主键为 `dt`、`order_id`。
  - 主键支持以下数据类型：BOOLEAN、TINYINT、SMALLINT、INT、BIGINT、LARGEINT、DATE、DATETIME、VARCHAR/STRING。并且不允许为 NULL。
  - 分区列和分桶列必须在主键中。

- `enable_persistent_index`：是否持久化主键索引，同时使用磁盘和内存存储主键索引，避免主键索引占用过大内存空间。通常情况下，持久化主键索引后，主键索引所占内存为之前的 1/10。您可以在建表时，在`PROPERTIES`中配置该参数，取值范围为 `true` 或者 `false`（默认值）。

  > - 自 2.3.0 版本起，StarRocks 支持配置该参数。
  > - 如果磁盘为固态硬盘 SSD，则建议设置为 `true`。如果磁盘为机械硬盘 HDD，并且导入频率不高，则也可以设置为 `true`。
  > - 建表后，如果您需要修改该参数，请参见 ALTER TABLE [修改表的属性](https://docs.starrocks.io/zh-cn/2.5/sql-reference/sql-statements/data-definition/ALTER TABLE#修改-table-的属性) 。

- 如果未开启持久化索引，导入时主键索引存在内存中，可能会导致占用内存较多。因此建议您遵循如下建议：

  - 合理设置主键的列数和长度。建议主键为占用内存空间较少的数据类型，例如 INT、BIGINT 等，暂时不建议为 VARCHAR。
  - 在建表前根据主键的数据类型和表的行数来预估主键索引占用内存空间，以避免出现内存溢出。以下示例说明主键索引占用内存空间的计算方式：
    - 假设存在主键模型，主键为`dt`、`id`，数据类型为 DATE（4 个字节）、BIGINT（8 个字节）。则主键占 12 个字节。
    - 假设该表的热数据有 1000 万行，存储为三个副本。
    - 则内存占用的计算方式：`(12 + 9(每行固定开销) ) * 1000W * 3 * 1.5（哈希表平均额外开销) = 945 M`

# 运维手册

## 集群配置

**ADMIN SHOW CONFIG 命令**

参考链接: [官方集群管理命令](https://docs.starrocks.io/zh-cn/2.5/sql-reference/sql-statements/Administration/ADMIN%20SHOW%20CONFIG)

```sql
-- 查看所有FE配置
ADMIN SHOW FRONTEND CONFIG;
-- 查看指定配置
ADMIN SHOW FRONTEND CONFIG like 'max_scheduling_tablets'
-- 查看模糊指标的配置
ADMIN SHOW FRONTEND CONFIG like '%disable%';
```

所有配置参数说明: [官方文档配置参数](https://docs.starrocks.io/zh-cn/2.5/administration/Configuration#fe-%E9%85%8D%E7%BD%AE%E9%A1%B9)

## 系统变量

参考链接: [官方文档-系统变量](https://docs.starrocks.io/zh-cn/2.5/reference/System_variable)

**查看变量**

```sql
-- 查看系统中所有变量。
SHOW VARIABLES;

-- 查看符合匹配规则的变量。
SHOW VARIABLES LIKE '%time_zone%';
```

**当前会话生效**

```sql
-- 通过 SET <var_name> = xxx; 语句设置的变量仅在当前会话生效。如：
SET exec_mem_limit = 137438953472;

SET forward_to_master = true;

SET time_zone = "Asia/Shanghai";
```

**全局生效**

```sql
SET GLOBAL exec_mem_limit = 137438953472;
```

**单个查询生效**

```sql
SELECT /*+ SET_VAR(exec_mem_limit = 8589934592) */ name FROM people ORDER BY name;

SELECT /*+ SET_VAR(query_timeout = 1) */ sleep(3);
```

## 用户管理

参考文档: [官方文档用户管理](https://docs.starrocks.io/zh-cn/2.5/sql-reference/sql-statements/account-management/CREATE%20USER)

```sql
-- 建一个允许从 '192.168' 子网登录的用户
CREATE USER 'jack'@'192.168.%' IDENTIFIED BY '123456';

-- 查看所有用户的认证信息
SHOW ALL AUTHENTICATION;

-- 查看当前用户的认证信息。
SHOW AUTHENTICATION;

-- 查看指定用户的认证信息。
SHOW AUTHENTICATION FOR root;

-- 删除用户
DROP USER 'jack'@'192.%';

-- 查看所有用户权限信息
SHOW ALL GRANTS; 
-- 查看指定 user 的权限
SHOW GRANTS FOR jack@'%';
-- 查看当前用户的权限
SHOW GRANTS;

```

## Grafana配置

```sql
-- 新建用户
CREATE USER 'grafana'@'192.168.%' IDENTIFIED BY 'grafana';
-- 授权统计表的只读权限
GRANT SELECT_PRIV ON _statistics_.* TO 'grafana'@'192.168.%';

-- 查看用户
SHOW ALL AUTHENTICATION;
-- 查看权限
SHOW ALL GRANTS; 
```

# CBO统计信息

参考文档: [官方文档-查询加速-CBO统计信息](https://docs.starrocks.io/zh-cn/2.5/using_starrocks/Cost_based_optimizer)

| **采集类型** | **采集方式** | **采集方法**                                                 | **优缺点**                                                   |
| :----------- | :----------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| 全量采集     | 自动或手动   | 扫描全表，采集真实的统计信息值。按照分区（Partition）级别采集，基础统计信息的相应列会按照每个分区采集一条统计信息。如果对应分区无数据更新，则下次自动采集时，不再采集该分区的统计信息，减少资源占用。全量统计信息存储在 `_statistics_.column_statistics` 表中。 | 优点：统计信息准确，有利于优化器更准确地估算执行计划。缺点：消耗大量系统资源，速度较慢。从 2.4.5 版本开始支持用户配置自动采集的时间段，减少资源消耗。 |
| 抽样采集     | 自动或手动   | 从表的每个分区中均匀抽取 N 行数据，计算统计信息。抽样统计信息按照表级别采集，基础统计信息的每一列会存储一条统计信息。列的基数信息 (ndv) 是按照抽样样本估算的全局基数，和真实的基数信息会存在一定偏差。抽样统计信息存储在 `_statistics_.table_statistic_v1` 表中。 | 优点：消耗较少的系统资源，速度快。 缺点：统计信息存在一定误差，可能会影响优化器评估执行计划的准确性。 |

**查看采集配置**

```sql
-- 查看全量采集配置(为false时,系统停止自动的全量采集任务)
ADMIN SHOW FRONTEND CONFIG like 'enable_collect_full_statistic'
```

**自动全量采集时间段**

从 2.4.5 版本开始，支持用户配置自动全量采集的时间段，防止因集中采集而导致的集群性能抖动。采集时间段可通过 `statistic_auto_analyze_start_time` 和 `statistic_auto_analyze_end_time` 这两个 FE 配置项来配置。

```sql
ADMIN SHOW FRONTEND CONFIG like 'statistic_auto_analyze_%_time'
```

触发自动采集的判断条件：

- 上次统计信息采集之后，该表是否发生过数据变更。
- 分区数据是否发生过修改，未发生过修改的分区不做重新采集。
- 采集是否落在配置的自动采集时间段内（默认为全天采集，可进行修改）。
- 该表的统计信息健康度（`statistic_auto_collect_ratio`）是否低于配置阈值。

> 健康度计算公式：
>
> ​	当更新分区数量小于 10个 时：1 - MIN(上次统计信息采集后的更新行数/总行数)
>
> ​	当更新分区数量大于等于 10 个时： 1 - MIN(上次统计信息采集后的更新行数/总行数, 上次统计信息采集后的更新的分区数/总分区数)

```sql
-- 查看集群全部自定义采集任务。
SHOW ANALYZE JOB

-- 查看数据库test下的自定义采集任务。
SHOW ANALYZE JOB where `database` = 'test';
```

