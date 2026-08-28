# Elastic-Job-Lite 分布式调度示例

## 项目结构

```
elastic-job-demo/
├── pom.xml
└── src/main/
    ├── java/com/example/elasticjob/
    │   ├── Application.java              # 启动入口（Spring 注解配置）
    │   ├── PureJavaMain.java             # 启动入口（纯 Java，无 Spring）
    │   ├── config/
    │   │   └── ElasticJobConfig.java     # Java 配置方式
    │   └── job/
    │       ├── MySimpleJob.java          # SimpleJob 示例
    │       └── MyDataflowJob.java        # DataflowJob 示例
    └── resources/
        └── applicationContext-job.xml    # XML 配置方式（可选）
```

## 前置条件

1. **JDK 1.8+**
2. **Maven 3.x**
3. **Zookeeper**（注册中心，必需）

   快速启动 Zookeeper：
   ```bash
   docker run -d --name zk -p 2181:2181 zookeeper:3.6
   ```

## 运行方式

### 方式一：Spring 注解配置（推荐）
运行 `Application.main()`，自动加载 `ElasticJobConfig` 配置。

### 方式二：纯 Java（无 Spring）
运行 `PureJavaMain.main()`，适合轻量场景。

### 方式三：Spring XML 配置
将 `applicationContext-job.xml` 加载到 Spring 容器中。

## 作业说明

### 1. SimpleJob（`MySimpleJob`）
- **类型**：最常用的简单作业
- **Cron**：`0/5 * * * * ?`（每 5 秒）
- **分片**：3 个分片，参数 `0=A,1=B,2=C`
- **特性**：失效转移、错过重执行
- **场景**：定时清理、数据同步、状态刷新

### 2. DataflowJob（`MyDataflowJob`）
- **类型**：数据流作业
- **Cron**：`0/10 * * * * ?`（每 10 秒）
- **分片**：3 个分片
- **流式处理**：`streamingProcess=true`，不停抓取直到无数据
- **场景**：大批量数据分批处理、消息补偿

## 核心概念

| 概念 | 说明 |
|------|------|
| **注册中心** | 基于 Zookeeper，负责选主、分片、失效转移 |
| **分片** | 将一个作业拆成多个分片，分配给不同实例并行执行 |
| **失效转移（Failover）** | 某节点宕机后，其分片自动转移到存活节点 |
| **错过任务重执行（Misfire）** | 错过的执行机会在恢复后补执行 |

## Cron 表达式说明

```
0/5 * * * * ?
│  │ │ │ │ │
│  │ │ │ │ └─ 年（可选）
│  │ │ │ └─── 周（? 表示不限制）
│  │ │ └───── 月
│  │ └─────── 日
│  └───────── 时
└──────────── 秒（0/5 表示从0秒开始每5秒）
```

## 验证高可用

1. 启动实例 A（运行 `Application.main`）
2. 修改端口后启动实例 B（或在不同机器上启动）
3. 观察：两个实例分担不同分片
4. 关闭实例 A → 实例 A 的分片自动转移给实例 B 继续执行
