### 环境安装:

```shell
pip install -r requirements.txt
```

### 服务运行:

```shell
gunicorn -b 0.0.0.0:5000 -w 5 server:app --reload
```


### 核心目录/文件说明：
1. metrics: 存放相关模型指标，csv存储
2. template: 存放html 模板
3. server.py web服务主入口


### 集成步骤：
1. template 文件夹下，拷贝porn.html, 修改其中div id，同步修改getElementbyId的参数，修改setOption参数变量
2. index.html 中搜索include，并在其后引入<1> 中创建的html template
3. metrics 下存放模型相关指标
4. 在server.py 中创建函数获取模型指标数据生成图标。在index函数中调用创建的函数，并传递到render_template中，字典变量名与1中setOption中的参数名对应
5. 刷新页面，查看是否生效

