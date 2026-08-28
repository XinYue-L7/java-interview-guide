package com.example.elasticjob;

import org.springframework.context.annotation.AnnotationConfigApplicationContext;

/**
 * 启动入口。
 *
 * 运行前提：
 *   1. 本地（或远程）已启动 Zookeeper，默认端口 2181
 *      快速启动：docker run -d --name zk -p 2181:2181 zookeeper:3.6
 *   2. 执行 mvn compile 编译
 *   3. 运行此类的 main 方法
 *
 * 观察控制台：
 *   - SimpleJob 每 5 秒触发一次，3 个分片并发执行
 *   - DataflowJob 每 10 秒触发一次，流式抓取并处理数据
 *
 * 高可用验证：
 *   启动两个实例（修改端口或在不同机器），当其中一个实例宕机时，
 *   它的分片会被自动转移（failover）到存活实例继续执行。
 */
public class Application {

    public static void main(String[] args) {
        System.out.println("=== Elastic-Job-Lite 示例启动中... ===");
        System.out.println("请确保 Zookeeper 已在 127.0.0.1:2181 启动");
        System.out.println();

        @SuppressWarnings("resource")
        AnnotationConfigApplicationContext context =
                new AnnotationConfigApplicationContext("com.example.elasticjob.config");

        context.registerShutdownHook();

        System.out.println("=== Elastic-Job-Lite 示例已启动 ===");
        System.out.println("SimpleJob   : 每 5 秒执行一次（3 分片）");
        System.out.println("DataflowJob : 每 10 秒执行一次（3 分片，流式处理）");
        System.out.println("按 Ctrl+C 退出...\n");

        // 主线程保持运行，作业由独立线程调度
        try {
            Thread.currentThread().join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
