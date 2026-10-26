# Apache Paimon C++ ：从阿里数据湖走向开源社区：PDF文本转写

> 仅转写原PDF文本层，页码为物理页序。图表、代码版面、未加载区域的限制见AI笔记与META；文本提取为空不表示原页为空白。

[原始PDF](RAW.pdf) · [AI学习笔记](<AI_Paimon C++湖表SDK.md>) · [来源与核验](META.json)

## PDF 第1页

[查看原页](RAW.pdf#page=1)

```text
Apache Paimon C++ ：从阿⾥数据湖⾛向开源社区
刘欣瑀 阿⾥技术 2026年9⽉9⽇ 03:18 浙江 2⼈
这是2026年的第 59 篇⽂章
（ 本⽂阅读时间：约 20 分钟 ）
前⾔
Apache Paimon C++ v0.3.0 最近发布了。这是 Paimon C++ 在 Apache 基⾦会下的第⼀个
正式版本，也意味着⼀个从阿⾥内部数据湖 需求⾥⻓出来的项⽬，开始以社区化的⽅式⾯向更
多引擎和开发者。
把时钟拨回 2024 年 1 ⽉。阿⾥巴巴集团决定统⼀采⽤ Apache Paimon 作为数据湖表格式。但
集团内部跑着的 ODPS、StarRocks 、Native Flink、Native Spark 等，⼤多是 C++ Native 引
擎。它们需要的不只是⼀个能够打开 Parquet 或 ORC ⽂件的 Reader，是⼀套不依赖 JVM、
能够完整理解 Paimon 表语义，并充分发挥 Native 引擎性能的读写库。
Paimon C++ 由此出现。项⽬由阿⾥巴巴智能引擎承担，团队⻓期为淘宝、⾼德、菜⻦、钉钉、
1688、闲⻥等内部搜推⼴业务提供⾼效稳定的⼯程能⼒。项⽬没有简单移植 Java 实现，系统性
调研了不同引擎的执⾏模型和真实 Workload，设计了⼀套以 Arrow 批式数据交换为基础、⽀持
深度插件化定制的 Native Paimon C++ SDK。
经过近两年⽣产验证，Paimon C++ 已在阿⾥数据湖上稳定⽀撑数 EB 数据。2025 年 12 ⽉在
GitHub Alibaba 开源后，项⽬很快吸引到蚂蚁、字节、云器 等团队参与共建。如今进⼊
Apache 社区，v0.3.0 成为新的起点。
```

## PDF 第2页

[查看原页](RAW.pdf#page=2)

```text
01
⼀套已经服务多类 Native Workload 的
Paimon SDK
在进⼊ Apache 社区之前，Paimon C++ 已经在不同类型的引擎、产品和业务中形成接⼊与⽣产
实践：
⼤规模⽣产使⽤：Native Spark（Gluten + Velox）、StarRocks、Native Flink 已在⽣产环
境⼤规模使⽤ Paimon C++ 读写能⼒；
开源社区接⼊：已形成 DuckDB 社区扩展、字节跳动 Bolt、Apache Doris 等社区⽣态接
⼊；
云上产品接⼊：StarRocks、Milvus、DuckDB、Spark 和 Hologres 等云上产品正在接⼊或
使⽤ Paimon C++；
内部业务使⽤：蚂蚁集团（Spark、OceanBase、Explorer）、字节跳动 TokaDB、云器等内
部业务已经开展使⽤和验证；
即将接⼊：下⼀步将启动 ClickHouse Native 接⼊，进⼀步覆盖⾼性能 OLAP 查询场景。
这些接⼊场景的执⾏框架、数据格式、⽂件系统、内存管理和查询模式并不相同。Paimon C++
的⽬标是让它们保留⾃⼰的性能优势，同时共享同⼀套 Paimon 表语义。
02
从阿⾥巴巴真实需求中诞⽣
集团统⼀采⽤ Paimon 后，Native 引擎⾯临的第⼀个问题是：如何正确、⾼效地访问 Paimon
表？
直接读取对象存储中的 Parquet 或 ORC ⽂件并不够。Paimon 表中的有效数据并⾮「⽬录下全
部⽂件」的简单集合，是由 Schema、Snapshot、Manifest、Partition、Bucket、索引以及表的
更新与合并规则共同确定。引擎还需要正确处理：
当前 Snapshot 对应哪些数据⽂件；
```

## PDF 第3页

[查看原页](RAW.pdf#page=3)

```text
Append 表和主键表各⾃的读取、更新与合并语义；
Merge-on-Read、Deletion Vector 和 Compaction 如何⽣成最终结果；
统计信息、⽂件索引和全局索引如何参与数据裁剪；
写⼊结果如何与 Paimon 的表版本及格式协议保持兼容。
如果每个引擎分别实现⼀套 Paimon Reader/Writer，不仅建设成本⾼，格式兼容性和⻓期维护
也会成为问题；如果所有数据都绕回 JVM 处理，⼜很难充分发挥 Native 引擎已有的向量化执⾏
和 I/O 优化能⼒。
因此，Paimon C++ 以“完整理解 Paimon 表语义”为⽬标：计算引擎继续负责分布式调度、算⼦
执⾏和数据交换，Paimon C++ 则负责 Scan、Read、Write、Commit、Compaction 以及相关
的格式和表语义。
03
C++ 引擎真正需要什么样的 Paimon SDK？
Paimon C++ 针对 Native 引擎的执⾏⽅式进⾏了专⻔设计，⽽⾮只是将 Java 实现迁移到
C++。经过对不同引擎使⽤场景的调研，⼀套适合 C++ ⽣态的湖表 SDK，需要同时满⾜以下四
类诉求。
直接适配向量化执⾏
分析型引擎普遍以列式 Batch 为单位完成计算。Paimon C++ 采⽤ Arrow C Data Interface 作
为主要数据交换边界，读取结果以 Arrow Batch 返回，写⼊侧也直接接收 Arrow Batch。
这种设计减少了逐⾏对象转换和不必要的数据复制，可以更⾃然地衔接向量化算⼦、批量调度和
并⾏执⾏。同时，Arrow C Data Interface 避免将 Paimon C++ 绑定到某个特定 Arrow C++
SDK 版本，降低引擎已有 Arrow 依赖之间的 ABI 冲突和集成成本。
保留引擎已有的性能能⼒
不同引擎通常已经在⽂件读取、缓存、内存管理和任务调度上投⼊多年优化；接⼊新的湖表
SDK，不应该意味着放弃这些积累。
Paimon C++ 因此设计了⾯向 Native 引擎的插件化扩展机制，允许引擎接⼊⾃定义的：
Format Reader/Writer：复⽤已有的 ORC、Parquet 或其他格式实现；
FileSystem：复⽤已有的对象存储访问、缓存和限流能⼒；
MemoryPool：接⼊引擎⾃⼰的内存统计、限额和回收体系；
Executor：复⽤引擎内部的线程池与任务调度能⼒。
Indexer：⽀持引擎按需定制索引实现。
例如，StarRocks 在接⼊过程中复⽤了内部带 Block Cache 的⽂件系统，使原有缓存与 I/O 优
化能够继续作⽤于 Paimon 读写链路，避免因为接⼊ SDK ⽽丢失已有性能能⼒。
```

## PDF 第4页

[查看原页](RAW.pdf#page=4)

```text
字节跳动 Bolt 则通过实现 Parquet 插件复⽤内部精⼼优化的 Parquet 读写能⼒，使其在接⼊
Paimon 表语义后，仍然能够延续原有的格式读取优势。
很多引擎还会注⼊⾃⼰的 MemoryPool，对 Paimon 读写链路的当前内存、峰值内存和分配⾏为
进⾏统⼀观测，并与引擎内部的资源管理和调度策略协同。
同时提供⾼效的默认实现
充分开放定制能⼒，并不意味着所有引擎都必须⾃⾏实现底层组件。Paimon C++ 同时提供⼀套
⾼效的默认实现，包括：
ORC、Parquet、Avro、Blob 等⽂件格式插件；
Local、Jindo、S3 等⽂件系统实现与统⼀⽂件系统抽象；
默认 MemoryPool 和 Executor；
Manifest Cache、Parquet Metadata Cache 等元数据缓存；
⽂件索引，以及⾯向标量、全⽂和向量检索的全局索引。
引擎可以开箱即⽤，也可以只替换⾃⼰最关注的组件。Paimon C++ 希望在通⽤性与专属性能之
间提供⾜够灵活的选择。
与 Apache Paimon 保持格式和协议兼容
Paimon C++ 原⽣实现 Paimon 表语义，同时保持与 Apache Paimon Java 格式及通信协议兼
容，包括 Manifest、Data Split、Commit Message 等关键数据结构。
不同语⾔和引擎因此可以共享同⼀张 Paimon 表，⽽不需要分别维护相互割裂的格式分⽀。
04
Paimon C++ 的五个设计重点
Paimon C++ ⽬前的核⼼能⼒可以归纳为五点。
将完整 Paimon 表语义带⼊ C++ ⽣态
Paimon C++ 是⼀套覆盖 Scan、Read、Write、Commit、Compaction 等操作的表级 SDK，⽀
持 Append 表和主键表，以及 Merge-on-Read、Deletion Vector 等关键语义。
设计基于 Arrow 的 Native 批式数据通路
通过 Arrow C Data Interface 在引擎与 SDK 之间交换列式 Batch，让 Paimon 数据可以直接进
⼊ Native 引擎的向量化执⾏链路，减少逐⾏转换、数据复制和跨语⾔交互。
建⽴可深度定制的插件化架构
```

## PDF 第5页

[查看原页](RAW.pdf#page=5)

```text
FileFormat、FileSystem、MemoryPool 和 Executor 均可由引擎定制。引擎可以复⽤经过⽣产
验证的基础设施和优化经验，同时由 Paimon C++ 统⼀维护表格式、协议、索引和⼀致性语义。
围绕 Native 读写链路进⾏系统优化
Paimon C++ 围绕 Native 读写链路进⾏了多项系统优化，本⽂后续会介绍其中⼏项：读取侧的
⽂件预取、Pipeline、多线程解码、异步 Row-to-Batch 和查询短路，以及主键写⼊侧通过分层
Spill Merge 减少临时⽂件重复读取和归并读放⼤。
从真实 Workload 出发扩展 Paimon 的能⼒边界
除了传统分析，Paimon C++ 还⽀持 Data Evolution、多模态数据和 Global Index，探索⾯向时
序、动态 JSON、Free-schema 和实时数据等 Workload 的存储与检索模式，并推动成熟能⼒进
⼊ Apache Paimon 标准演进。
05
完整读写链路如何⼯作
Scan 与 Read：让计划和执⾏⾃然分离
Paimon C++ 将读取拆分为 Scan 和 Read 两个阶段：
Scan: 读取 Snapshot 和 Manifest，根据 Partition、Bucket、统计信息和索引裁剪⽆关⽂
件，并⽣成可序列化的 Split；
Read: 在不同 Worker 上并⾏读取 Split，执⾏列裁剪、嵌套字段裁剪、谓词下推、Page
Filtering、预取和缓存，最终返回 Arrow Batch。
Coordinator 可以集中⽣成查询计划，Reader Task 则在不同节点并⾏执⾏。Split 可以跨进程和
语⾔传递，数据通过 Arrow 批式进⼊后续计算链路。
```

## PDF 第6页

[查看原页](RAW.pdf#page=6)

```text
Write 与 Commit：保留引擎的分布式执⾏模型
写⼊侧同样采⽤适合分布式引擎的两阶段模型：
Write: Worker 接收 Arrow Batch，完成数据组织与⽂件写⼊，并⽣成 Commit Message；
Commit: Coordinator 收集各 Worker 的 Commit Message，由 Paimon C++ 处理
Manifest、统计信息、冲突检查和 Snapshot 提交。
引擎仍然负责调度和数据交换，Paimon C++ 则保证表版本、⽂件格式和提交语义的正确性。
⽬前，Paimon C++ 已⽀持 Append 表和主键表的读写，包括 Merge-on-Read、Deletion
Vector 和 Compaction 等能⼒。
06
从传统分析⾛向 AI 与多模态检索
传统分析查询通常采⽤“列裁剪 + 谓词下推 + 批量扫描”的访问⽅式。AI Agent ⾯对的数据和查
询模式正在发⽣变化：⼀次检索可能同时包含向量相似度、全⽂关键词、权限与时间等标量过
滤，并最终返回⽂本、结构化字段、图⽚、⾳频或视频。
在 Data Evolution 表模式下，Paimon 为每⾏数据分配表级全局 Row ID，并通过 Row Tracking
保持稳定的⾏级定位能⼒。在此基础上，同⼀张 Paimon 表可以统⼀管理：
结构化数据；
⽂本与⽂档；
Embedding 向量；
图⽚、⾳频、视频等 Binary / Blob 多模态数据。
```

## PDF 第7页

[查看原页](RAW.pdf#page=7)

```text
查询模式也由传统扫描扩展为“全局索引召回 + Row ID 精准点查”：
1. Global Index 根据标量、⽂本或向量条件召回候选 Row ID 和可选 Score；
2. Paimon C++ 结合 Snapshot、Manifest 和⽂件范围⽣成 IndexedSplit；
3. Reader 根据 Row ID 精确读取所需字段或 Blob 数据。
Paimon C++ 当前提供：
基于 BTree 的标量查找与范围过滤；
基于 Lucene 和 Tantivy 的全⽂检索；
基于 Lumina 的向量相似度检索；
参与 Scan 和 Read 裁剪的各类⽂件索引。
这种模式让“⼀份数据⼊湖，全部数据可检索”成为可能。结构化数据、⽂本、向量和多模态
Payload 不再必须复制到多套专⽤系统中，可以减少数据复制带来的⼀致性、成本和运维问题。
07
Native 读写链路的性能优化
Paimon C++ 的性能价值不只是去掉 JVM 和跨语⾔转换。项⽬还围绕 I/O、解码、数据复制、
主键合并和框架数据转换进⾏了专⻔设计。
写⼊：降低 PK Spill Merge 的读写放⼤
主键表写⼊需要对记录进⾏排序和归并。当内存 Buffer 超限时，中间结果需要 Spill 到临时⽂
件。
传统平铺式 Spill List 在后续归并中，可能反复读取已经参与过归并的旧 Run，产⽣额外读放
⼤。Paimon C++ 使⽤分层 Spill Merge，只归并达到 Fan-in 阈值的当前层级，减少旧 Run 的
重复读取，并控制单次归并规模。这⼀优化不改变主键表语义，但能减少临时⽂件 I/O，并让归
并过程在数据规模增⼤时保持更加稳定。
读取链路的主要优化
```

## PDF 第8页

[查看原页](RAW.pdf#page=8)

```text
1. 并⾏⽂件预取：同⼀ ORC 或 Parquet ⽂件可按 Row Range 分配给多个 Reader，并⾏完成
I/O、解码和结果输出；每个 Reader 线程内部还通过 Pipeline 重叠数据读取与解码过程，进
⼀步降低查询延迟。
2. 异步 PK Row-to-Batch：Sort Merge ⽣产端与 Arrow Batch 转换消费端异步，通过有界
队列解耦。同时，消费端⽀持多线程进⾏ KeyValue 到 Arrow Batch 的转换。
3. COUNT(*) Short Circuit：对于 Append、PK + DV 和 PK MOR 场景，直接基于元数据或
合并结果完成计数，避免构造完整的 Value Batch，以及由此产⽣的不必要的框架间数据转换
开销。
此外，Scan 阶段会利⽤ Snapshot、Manifest、Partition、Bucket、统计信息和索引裁剪⽂件；
Read 阶段继续进⾏列裁剪、嵌套字段裁剪、Predicate Pushdown、Page Filtering、Prefetch
和 Cache，从源头减少真正需要读取的数据量。
08
端到端性能验证
以下数据来⾃ Alibaba 集团⽣产环境，对⽐了相关引擎切换⾄ Paimon C++ 前后的端到端性能，
反映了引擎完整查询链路的实际变化。实际效果会受到数据分布、⽂件数量、查询类型、硬件和
引擎配置等因素影响。
Native Spark：Gluten + Velox
测试对象为 PK Merge-on-Read 表，数据规模 119.32 GB，约 70 个⽂件存在主键重叠。
场景 Paimon C++ 切换前基线 提升
PK MOR 读取，8 轮 21～48 分钟 41～126 分钟 1.5～3.7 倍
StarRocks Native Reader
测试环境为单 BE、8 Core / 32 GB，对⽐ StarRocks 引擎切换 Paimon C++ 前后的端到端查
询性能。
场景 Paimon C++ 切换前基线 提升
Narrow Count 150 ms 220 ms 1.5 倍
PK Count，1000 列 403 ms 1251 ms 3.1 倍
```

## PDF 第9页

[查看原页](RAW.pdf#page=9)

```text
Narrow Aggregate 202 ms 451 ms 2.2 倍
PK Point / Filter 231～274 ms 376～403 ms 1.4～1.7 倍
Full-width Aggregate 18.5 秒 62.0 秒 3.4 倍
这些结果说明，Paimon C++ 的价值不仅在于消除 JVM 边界，还来⾃对 Paimon 表语义的完整
Native 实现，以及围绕⽂件读取、主键合并和 Arrow 批式转换所做的系统优化。随着数据规模
扩⼤，这些优化能够更充分地发挥作⽤，Paimon C++ 的性能收益也会更加明显。
09
从 Alibaba 到 Apache：持续演进与社区共建
从阿⾥内部数据湖业务到 Apache 社区，Paimon C++ 的核⼼⽬标没有变：让 Native 引擎在不
丢掉⾃身性能优势的前提下，完整、稳定地接⼊ Paimon ⽣态；变化的只是参与的⼈越来越多，
场景越来越⼴。
未来，社区会同步推进两条线：⼀条线紧跟 Apache Paimon 主线的格式和功能演进，完善
Native Scan、Read、Write、Commit、REST Catalog、Changelog 等能⼒；另⼀条线从真实
需求中持续探索 AI、多模态、时序、动态 JSON、Free-schema 和实时数据等场景，把成熟经
验沉淀为社区标准。
也欢迎来⾃查询引擎、数据湖、AI Infra、可观测和存储领域的开发者关注、试⽤、共建，⼀起完
善 Apache Paimon 的开放⽣态！
相关链接
Apache Paimon C++ 官⽅仓库：https://github.com/apache/paimon-cpp
GitHub Release Note：https://github.com/apache/paimon-cpp/releases/tag/v0.3.0
使⽤⽂档：https://paimon.apache.org/docs/cpp/
Apache Paimon 官⽅⽹站：https://paimon.apache.org
Apache Paimon GitHub：https://github.com/apache/paimon
Apache Paimon C++ 交流群
欢迎加⼊ Apache Paimon C++ 钉钉交流群，与社区开发者⼀起交流使⽤经验、讨论技术问题，
并参与社区共建。
```

## PDF 第10页

[查看原页](RAW.pdf#page=10)

```text
使⽤钉钉扫描⼆维码，即可加⼊群聊
欢迎留⾔⼀起参与讨论~
阅读 1429
```

## PDF 第11页

[查看原页](RAW.pdf#page=11)

```text
留⾔
写留⾔
还没有留⾔，来写⾸评
```

