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

# 参考文档：
1. [hadoop官方命令说明](https://hadoop.apache.org/docs/r3.1.1/hadoop-project-dist/hadoop-common/FileSystemShell.html#du)