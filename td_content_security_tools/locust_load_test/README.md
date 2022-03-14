### 压测工具locust
#### 安装locust环境
```shell
pip install locust==1.4.4
```

#### 准备测试图片
测试图片放置同目录下的test_image文件夹中

#### web模式
```shell
locust -f locustfile.py --host=http://10.57.31.15:8179
```
--host: 被压测服务的地址
##### 启动web界面，输入用户总数和并发数
`http://127.0.0.1:8089`

![web启动页面](images/welcome.png)
##### 监控压测情况

![压测图片](images/status.png)

##### qps和延时图表

![图表](images/graph.png)

#### no-web模式
```shell
locust -f locustfile.py --host=http://10.57.31.15:8179 --no-web -c 10 -r 10
```

#### 自动负载模式
```shell
locust -f locustfile_auto.py --host=http://10.57.31.15:8179
```

#### 常用参数
- -u 指定总的用户数
- -r 指定每秒产生的用户数（u/r 即多久开始按照指定的请求总数执行压测，相当于一个预热过程）
- -t: 执行压测的时间
