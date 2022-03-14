## 数据备份工具
## 数据备份
通过tdbackup工具对模型数据资产进行定期自动备份。`tdbackup` 是公司运维团队提供的备份工具。[详细使用方法](http://wiki.tongdun.me/pages/viewpage.action?pageId=39580309)。由于我们训练数据主要为二进制的非结构化数据，所以类型为file。

## data_backup 脚本
该脚本是对`tdbackup`工具的python封装。

### 依赖
1. requests: 下载tdbackup工具
2. psutil: 查找到一个有效的网卡

### 使用方法
脚本共支持三个子命令：
- 基础配置：下载工具，配置server
- 一键备份：输入策略名及备份路径即可一下完成备份设置；策每周日凌晨3点备份；每月1号凌晨三点备份
- 自定义备份

```shell
python data_backup.py --help
```
如下输出：
```
usage: 
    backup your data by tdbackup tools. 
    1. configure tdbackup tool
    2. fast backup use default policy
    3. add your custom backup policy
    
       [-h] {config,fast-backup,add} ...

positional arguments:
  {config,fast-backup,add}
    config              prepare tdbackup tools
    fast-backup         one shot backup for dl training data
    add                 add extra backup policy.

optional arguments:
  -h, --help            show this help message and exit
```
### 使用流程
1. 下载相关工具，配置server
```shell
python data_backup.py config  
```
2. 快速一键配置数据备份，输入策略名和要备份的数据地址
```shell
python data_backup.py fast-backup --name porn_data --data_path /disk/yubin.wang/porn_data 
```
3. 【可选】如有特殊需求备份需求，可新增策略
```shell
python data_backup.py add --name porn_data --data_path /disk/yubin.wang/porn_data
```

#### 备份周期参考crontab
[cron 配置策略](https://www.runoob.com/linux/linux-comm-crontab.html)

```
*    *    *    *    *
-    -    -    -    -
|    |    |    |    |
|    |    |    |    +----- 星期中星期几 (0 - 6) (星期天 为0)
|    |    |    +---------- 月份 (1 - 12) 
|    |    +--------------- 一个月中的第几天 (1 - 31)
|    +-------------------- 小时 (0 - 23)
+------------------------- 分钟 (0 - 59)
```

### tdbackup 常用命名：
#### 查询备份情况：
```shell
./tdbackup ls tdbackup_server/tdbackup-ai-vision/<有效期>/<备份机器ip>/file/<name>/<备份策略id>/<data_path>
```

#### 查看备份策略：
```shell
./tdbackup bp ls tdbackup_server  -i eno1 --json
```

#### 删除备份策略：
```shell
./tdbackup bp del file --id 1633674949082411976 -i eno1 tdbackup_server
```

### FAQ
1. 未知域名：
  - 不能配置代理，no_proxy='minio-tdbackup-offline.te.td'
  - 若仍不能访问到，配置hosts，映射ip
```shell
# 在 /etc/hosts 中添加
10.57.27.6      minio-tdbackup-offline.te.td
sudo /etc/init.d/network restart
```