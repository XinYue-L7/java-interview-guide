package com.example.elasticjob.job;

import com.dangdang.ddframe.job.api.ShardingContext;
import com.dangdang.ddframe.job.api.dataflow.DataflowJob;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * DataflowJob —— 数据流作业。
 *
 * 与 SimpleJob 不同，DataflowJob 分为两步：
 *   1. fetchData()：抓取数据
 *   2. processData()：处理数据
 *
 * 特点：当 fetchData 返回 null 或空集合时，作业停止继续抓取，等待下次调度。
 * 配合 streamingProcess=true 可实现"不停抓取直到无数据"的流式处理。
 *
 * 适用场景：大批量数据分批处理、消息补偿、订单状态轮询等。
 */
public class MyDataflowJob implements DataflowJob<String> {

    private static final Logger log = LoggerFactory.getLogger(MyDataflowJob.class);

    /** 模拟待处理数据源 */
    private final AtomicInteger counter = new AtomicInteger(0);

    /**
     * 抓取数据
     */
    @Override
    public List<String> fetchData(ShardingContext shardingContext) {
        int shard = shardingContext.getShardingItem();

        // 模拟从数据库/消息队列抓取数据
        List<String> data = new ArrayList<>();
        for (int i = 0; i < 5; i++) {
            int id = counter.getAndIncrement();
            if (id >= 30) {
                // 数据抓完了，返回空列表，作业将等待下次调度
                break;
            }
            // 简单分片：只抓取属于当前分片的数据
            if (id % shardingContext.getShardingTotalCount() == shard) {
                data.add("data-" + id);
            }
        }

        log.info("【DataflowJob-fetch】分片{} 抓取到 {} 条数据: {}", shard, data.size(), data);
        return data;
    }

    /**
     * 处理数据
     */
    @Override
    public void processData(ShardingContext shardingContext, List<String> data) {
        log.info("【DataflowJob-process】分片{} 正在处理 {} 条数据", shardingContext.getShardingItem(), data.size());

        for (String item : data) {
            log.info("  -> 处理完成: {}", item);
            // 这里写实际业务逻辑：更新数据库、发送消息、调用接口等
        }
    }
}
