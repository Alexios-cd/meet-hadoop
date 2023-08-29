# 获取hdfs目录大小

```shell
# 获取每个目录的大小
hadoop fs -du -h /
# 对比Linux原生命令
du -h -d 1 /
```
输出如下：
```shell
#第一列为单个文件实际大小，第二列为备份大小，第三列为详情目录
实际大小  备份大小    详情目录
182.7 G  366.4 G  /checkpoint
133.8 K  267.5 K  /data
14.3 G   43.9 G   /hbase
0        0        /home
511.2 G  1.0 T    /indata
577.3 G  1.1 T    /sparkdata
50.4 G   101.6 G  /busdata
155.6 M  311.3 M  /tmp
7.4 T    22.3 T   /user
```
---
# 获取当前目录总容量

```shell
# 获取当前目录总容量
#-s 统计父目录
hadoop fs -du -h -s  /
```
输出如下：
```shell
#第一列为单个文件实际大小，第二列为备份大小，第三列为详情目录
实际大小  备份大小    详情目录
8.7 T  25.0 T  /
```
---
```shell
# 获取HDFS整体使用
[root@quickstart ~]# hdfs dfs -df -h /
Filesystem                         Size     Used  Available  Use%
hdfs://quickstart.cloudera:8020  54.5 G  832.6 M     31.5 G    1% 
```
注意：
1. 可以使用排序相关命令 eg：hadoop fs -du -h / |sort -rh ，但是因为 前面加入了参数 -h 导致排序只能根据数据来做，不太实用
   1. 如果确实要根据文件夹大小排序可以使用 hdfs dfs -du / | sort -n -r 忽略-h 指令（这样显示的是bytes）
1. 关于第二列的数字跟第一列数字不一致，有说法为第二列为备份大小，有说法为限额大小，依据实际情况来看，偏向于备份大小。

---
# 获取当前目录的文件数量

```shell
hadoop fs -count -q -v /

QUOTA       REM_QUOTA     SPACE_QUOTA REM_SPACE_QUOTA    DIR_COUNT   FILE_COUNT       CONTENT_SIZE PATHNAME
none            inf            none             inf         145         1404          9088242399 /

-count: 指定要执行文件和目录计数操作。
-q 或 --quiet: 在输出结果中，只显示计数信息，不显示其他冗余信息。
-h 或 --human-readable: 以可读的格式显示文件和目录的大小。例如，使用 B、KB、MB 等单位显示文件大小。
-v 或 --verbose: 显示详细的计数信息，包括每个子目录的计数结果。
/path/to/your/directory: 这是您想要统计文件数量的目标文件夹的路径。
```

```
hadoop fs -count -q -v -h /
QUOTA       REM_QUOTA     SPACE_QUOTA REM_SPACE_QUOTA    DIR_COUNT   FILE_COUNT       CONTENT_SIZE PATHNAME
none             inf            none             inf        7.2 K       24.4 M            547.4 G /

"1K" 可以表示 1,000 个文件
"1M" 可以表示 1,000,000 个文件
"1G" 可以表示 1,000,000,000 个文件
```



# 删除历史日期文件

删除hdfs之前日期之前创建的文件

```shell
#!/bin/bash
 
# 定义要操作的目录路径变量
target_directory="/user/hdfs/.flink"
 
# 定义删除前的天数阈值
days_threshold=7
 
# 获取当前时间的时间戳
current_time=$(date +%s)
 
# 计算阈值天数前的时间戳
threshold_time=$((current_time - days_threshold * 24 * 3600))
 
# 进行kerberos认证
# kinit -kt /etc/kerberos/hdfs.keytab hdfs@HADOOP.COM
 
# 列出指定目录下的所有文件夹
hdfs dfs -ls "$target_directory" | awk '{print $6, $7, $8}' | while read -r modification_time_day modification_time_time folder_path; do
    # 构建完整的修改时间
    modification_time="${modification_time_day} ${modification_time_time}"
     
    # 转换修改时间为时间戳
    modification_timestamp=$(date -d "$modification_time" +%s)
     
    # 判断文件夹是否满足删除条件
    if [[ "$folder_path" != "/" && "$modification_timestamp" -lt "$threshold_time" ]]; then
        days_diff=$(( (current_time - modification_timestamp) / 86400 ))
        echo "文件夹创建时间为 $modification_time， 于 $days_diff 天以前创建: $folder_path 将会被删除"
        # 删除符合条件的文件夹
        hdfs dfs -rm -r "$folder_path"
    fi
done
echo "删除完成！！！！！"
```

# 参考文档：
1. [hadoop官方命令说明](https://hadoop.apache.org/docs/r3.1.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#du)