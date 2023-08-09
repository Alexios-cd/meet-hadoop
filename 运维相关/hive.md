# 时间戳格式化
```sql
SELECT from_unixtime(cast(join_date/1000 AS bigint),'yyyy-MM-dd HH:mm:ss.SSS') AS join_date_str
FROM ods_tg_group_member
LIMIT 10
```
在hive执行的过程中会自动将string转成数值，进行计算
```sql
select '1684339161000'/1000 

-- 输出 ： 1684339161
```