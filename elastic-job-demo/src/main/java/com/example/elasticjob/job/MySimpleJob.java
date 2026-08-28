package com.example.elasticjob.job;

import com.dangdang.ddframe.job.api.ShardingContext;
import com.dangdang.ddframe.job.api.simple.SimpleJob;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.text.SimpleDateFormat;
import java.util.Date;

/**
 * SimpleJob —— 最常用的作业类型。
 * 每次调度触发时执行一次 execute 方法。
 *
 * 适用场景：定时清理、数据同步、状态刷新等无状态任务。
 */
public class MySimpleJob implements SimpleJob {

    private static final Logger log = LoggerFactory.getLogger(MySimpleJob.class);

    @Override
    public void execute(ShardingContext shardingContext) {
        String time = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(new Date());

        log.info("【SimpleJob】时间: {} | 作业名称: {} | 分片总数: {} | 当前分片项: {} | 分片参数: {}",
                time,
                shardingContext.getJobName(),
                shardingContext.getShardingTotalCount(),
                shardingContext.getShardingItem(),
                shardingContext.getShardingParameter());

        // 根据分片项处理不同的数据，实现分布式分片执行
        switch (shardingContext.getShardingItem()) {
            case 0:
                // 分片 0 处理：例如处理 ID % 3 == 0 的数据
                log.info("  -> 分片0 正在处理 ID 取模为 0 的数据...");
                break;
            case 1:
                // 分片 1 处理：例如处理 ID % 3 == 1 的数据
                log.info("  -> 分片1 正在处理 ID 取模为 1 的数据...");
                break;
            case 2:
                // 分片 2 处理：例如处理 ID % 3 == 2 的数据
                log.info("  -> 分片2 正在处理 ID 取模为 2 的数据...");
                break;
            default:
                log.info("  -> 未知分片: {}", shardingContext.getShardingItem());
        }
    }
}
