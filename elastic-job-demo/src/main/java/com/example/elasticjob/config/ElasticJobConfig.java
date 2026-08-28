package com.example.elasticjob.config;

import com.dangdang.ddframe.job.api.dataflow.DataflowJob;
import com.dangdang.ddframe.job.api.simple.SimpleJob;
import com.dangdang.ddframe.job.config.JobCoreConfiguration;
import com.dangdang.ddframe.job.config.JobRootConfiguration;
import com.dangdang.ddframe.job.config.dataflow.DataflowJobConfiguration;
import com.dangdang.ddframe.job.config.simple.SimpleJobConfiguration;
import com.dangdang.ddframe.job.lite.api.JobScheduler;
import com.dangdang.ddframe.job.lite.config.LiteJobConfiguration;
import com.dangdang.ddframe.job.lite.spring.api.SpringJobScheduler;
import com.dangdang.ddframe.job.reg.base.CoordinatorRegistryCenter;
import com.dangdang.ddframe.job.reg.zookeeper.ZookeeperConfiguration;
import com.dangdang.ddframe.job.reg.zookeeper.ZookeeperRegistryCenter;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * Elastic-Job Java 配置方式（不依赖 XML）。
 *
 * 需要先启动一个 Zookeeper 服务，例如本地 docker：
 *   docker run -d --name zk -p 2181:2181 zookeeper:3.6
 */
@Configuration
public class ElasticJobConfig {

    /** Zookeeper 连接地址 */
    private static final String ZK_SERVER_LIST = "127.0.0.1:2181";
    /** Zookeeper 命名空间（隔离不同应用的作业） */
    private static final String ZK_NAMESPACE = "elastic-job-demo";

    // ==================== 注册中心 ====================

    /**
     * 注册中心：基于 Zookeeper，负责作业的选主、分片、高可用等协调工作。
     */
    @Bean(initMethod = "init")
    public CoordinatorRegistryCenter registryCenter() {
        ZookeeperConfiguration zkConfig = new ZookeeperConfiguration(ZK_SERVER_LIST, ZK_NAMESPACE);
        zkConfig.setConnectionTimeoutMilliseconds(3000);
        zkConfig.setSessionTimeoutMilliseconds(5000);
        return new ZookeeperRegistryCenter(zkConfig);
    }

    // ==================== SimpleJob 配置 ====================

    @Bean
    public SimpleJob mySimpleJob() {
        return new com.example.elasticjob.job.MySimpleJob();
    }

    @Bean(initMethod = "init")
    public JobScheduler simpleJobScheduler(final SimpleJob mySimpleJob, final CoordinatorRegistryCenter registryCenter) {
        // 核心配置：cron 表达式、分片数、分片参数
        JobCoreConfiguration core = JobCoreConfiguration.newBuilder(
                "mySimpleJob",           // 作业名称（全局唯一）
                "0/5 * * * * ?",         // cron：每 5 秒执行一次
                3                         // 分片总数：3 个分片
        ).shardingItemParameters("0=A,1=B,2=C")  // 分片参数，可按分片区分逻辑
         .description("SimpleJob 示例")
         .failover(true)               // 开启失效转移
         .misfire(true)                // 开启错过任务重执行
         .build();

        // Simple 作业配置
        SimpleJobConfiguration simpleConfig = new SimpleJobConfiguration(core, mySimpleJob.getClass().getCanonicalName());

        // Lite 作业配置
        LiteJobConfiguration liteConfig = LiteJobConfiguration.newBuilder(simpleConfig)
                .overwrite(true)         // 本地配置覆盖 ZK 中的配置（开发期建议 true）
                .monitorExecution(false) // 不监控作业执行状态（true 会记录运行态，生产可开）
                .build();

        return new SpringJobScheduler(mySimpleJob, registryCenter, liteConfig);
    }

    // ==================== DataflowJob 配置 ====================

    @Bean
    public DataflowJob<String> myDataflowJob() {
        return new com.example.elasticjob.job.MyDataflowJob();
    }

    @Bean(initMethod = "init")
    public JobScheduler dataflowJobScheduler(final DataflowJob<String> myDataflowJob, final CoordinatorRegistryCenter registryCenter) {
        JobCoreConfiguration core = JobCoreConfiguration.newBuilder(
                "myDataflowJob",         // 作业名称
                "0/10 * * * * ?",        // cron：每 10 秒触发一次
                3                         // 分片总数
        ).shardingItemParameters("0=A,1=B,2=C")
         .description("DataflowJob 示例")
         .build();

        // Dataflow 作业配置：streamingProcess=true 表示流式处理（不停抓取直到无数据）
        DataflowJobConfiguration dataflowConfig = new DataflowJobConfiguration(
                core,
                myDataflowJob.getClass().getCanonicalName(),
                true   // streamingProcess
        );

        LiteJobConfiguration liteConfig = LiteJobConfiguration.newBuilder(dataflowConfig)
                .overwrite(true)
                .build();

        return new SpringJobScheduler(myDataflowJob, registryCenter, liteConfig);
    }
}
