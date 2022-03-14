### 简介
通过自动化回归测试脚本，批量测试历史模型版本，监控模型迭代情况。测试结果写入到mysql中，最终通过superset进行可视化。
[superset地址](http://10.57.33.22:8089/superset/welcome/)

#### 自动化回归测试架构图
![架构图](./images/architecture.png)

### 依赖:
1. docker: docker python sdk
2. requests: ai api requests
3. sqlalchemy: communicate with database
4. loguru: logging
5. skearn: classification_report (可选)

#### 安装
```shell
pip install -r requirements.txt
```

### 文件/目录介绍
1. metrics: 存放各个场景指标对应的数据库字段
2. tools: 导入csv样例程序
3. images: 项目配图，自动回归测试架构图
4. database_util.py: 数据库连接操作相关工具

### 回归测试示例：
1. model_regression_example.py: 回归测试demo
2. config_example.yaml: 回归测试配置文件

### 模型指标表设计
    - 每个场景一个张表，具体字段可以自己设计
    - 必须字段：test_id, date(测试时间），model_version(模型版本)

#### 举例
![数据库标示例](images/table-example.png)