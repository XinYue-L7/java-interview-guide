package com.example.elasticjob;

import com.dangdang.ddframe.job.config.JobCoreConfiguration;
import com.dangdang.ddframe.job.config.simple.SimpleJobConfiguration;
import com.dangdang.ddframe.job.lite.api.JobScheduler;
import com.dangdang.ddframe.job.lite.config.LiteJobConfiguration;
import com.dangdang.ddframe.job.reg.base.CoordinatorRegistryCenter;
import com.dangdang.ddframe.job.reg.zookeeper.ZookeeperConfiguration;
import com.dangdang.ddframe.job.reg.zookeeper.ZookeeperRegistryCenter;
import com.example.elasticjob.job.MySimpleJob;

/**
 * 方式三：纯 Java 配置（不依赖 Spring）。
 *
 * 适合不想引入 Spring 框架的场景。
 */
public class PureJavaMain {

    public static void main(String[] args) {
        System.out.println("=== 纯 Java 方式启动 Elastic-Job ===");

        // 1. 创建注册中心
        ZookeeperConfiguration zkConfig = new ZookeeperConfiguration("127.0.0.1:2181", "elastic-job-demo");
        CoordinatorRegistryCenter registryCenter = new ZookeeperRegistryCenter(zkConfig);
        registryCenter.init();

        // 2. 构建作业配置
        JobCoreConfiguration core = JobCoreConfiguration.newBuilder(
                "mySimpleJob",
                "0/5 * * * * ?",
                3
        ).shardingItemParameters("0=A,1=B,2=C")
         .failover(true)
         .build();

        SimpleJobConfiguration simpleConfig = new SimpleJobConfiguration(core, MySimpleJob.class.getCanonicalName());

        LiteJobConfiguration liteConfig = LiteJobConfiguration.newBuilder(simpleConfig)
                .overwrite(true)
                .build();

        // 3. 启动调度器（纯 Java 方式不需要传入 Job 实例，
        //    Job 类通过 SimpleJobConfiguration 中的 class 全名由反射创建）
        JobScheduler scheduler = new JobScheduler(registryCenter, liteConfig);
        scheduler.init();

        System.out.println("=== 启动完成，按 Ctrl+C 退出 ===");

        // 主线程保持
        try {
            Thread.currentThread().join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
