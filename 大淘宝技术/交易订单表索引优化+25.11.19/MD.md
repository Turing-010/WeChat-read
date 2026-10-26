# 交易订单表如何做索引优化：PDF文本转写

> 这是原始PDF文本层转写，不是学习摘要。页码为PDF物理页序；图表、代码版面和图片文字不能完整表达在此文本层。已查看图像的内容和质量问题见AI学习笔记及META.json。

[原文PDF](RAW.pdf) · [AI学习笔记](AI_交易订单表索引优化.md) · [处理与质量记录](META.json)

## PDF 第1页

[查看原页](RAW.pdf#page=1)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
交易订单
原创
表如何做索引优化
营销&交易技术 2025年11月19日 01:15 浙江
大淘宝技术 509人
本文首先以淘天电商交易订单
表线上一条非典型慢 SQL 的
深
系
统地分析与排查慢 SQL；接着详尽归纳了索引分类、B
+
+
Tree 高度估算方法、EXPLAIN 与 Query Profile 等诊断
入剖析为切入点，示范如何
Tree 与 B‑Tree 的结构差
异、B
引下推与排序的执
工具的使用，以及索
行
流程等索引优化理论；最后结合日常实
践经验，提出了适用于大规
模线上集群的索引变更 SOP，并总结了常见的慢 SQL 成因与相应的解决策略。
前言
交易订单
表（tcorder）用于存储集团电商的在线订单记录，该表近60个字段，单个分表近千
万
行
左右（受历史订单迁移影响会上下浮动），平
行
长5.4KB，是名副其实的大
表，该表的
读写性能直接影响上游创
单、逆向退款、订单列表等一系列跟订单
有关
的业务功能，对该表的
任何变更都是非常谨慎，需要多方一起综
合评估。受业务需求推动，近两年我非常“有
作了一次订单
表索引优化，这里总结下mysql索引优化相关
的知
识
幸”各操
、SOP、之前遇到的慢SQL
问题及其对应的优化方法。
均
一个非典型的慢SQL
7月份做订单
表的慢SQL梳理，发现分页查询类的请求比
较多，典型的SQL如下：
1
2
3
4
select order
id from tcorder where is
_
_
main = 1
and buyer
id=2********5
_
***************
order by create
_
time desc,order
_
id asc limit 0,10
该类慢SQL执
行
的统计信息如下：
```

## PDF 第2页

[查看原页](RAW.pdf#page=2)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
字段 结果 说明
sql_id 71d14de3
SQL Parttern ID ， 基 于 原始 SQL
文本通过BKDR的HASH算法生成
execute_count 3106 慢SQL总次数
cost 2017平
均执
行
耗时，单位ms
send_row_count 10 平
均返回
行数
examined_row_count 8705平
均扫描
行数
logical_read 40023
平
逻辑读，即SQL处理过程中读
取的数据页和索引页的数量，包含
从Innodb Buffer Pool和磁盘读取
两
部分的，数据页和索引页的大小
都是16kb
均
physical_sync_read 5174
平
均同步物理读，即SQL处理过程
中从磁盘读取的数据页和索引页的
数量
该慢SQL的执
计划如下：
行
据 此 该SQL 实 际 执
行
过 程中 是 命中 索 引 `ind_***_buyerid` ， 其中 buyer_id走 索 引 过 滤
（key_len等于8），is_main等大部分字段都在索引里面，通过索引下推过滤（Using index
conditions），只有两个字段不在索引中通过回表查过滤（Using where）。这两个字段正常
满足条件的比例不超过1%，因此即使回表查扫描
行数也不会大幅上涨。出现问题的可能原因就
是这里的Using filesort，这种方式下需要把所有
满足条件的记录都过滤出来再排序，排序完成
再取前10条，导致扫描
行数和逻辑读异常。
上述猜想可以通过mysql的show profile执
行
过程来验证，如下：
```

## PDF 第3页

[查看原页](RAW.pdf#page=3)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
Creating sort index 的 耗 时 和 CPU 损 耗 远大 于 其 他几 步 ， 确 认 是 filesort 导 致 。 为 啥 出 现
filesort呢？因为排序条件create_time desc,order_id asc无法利用索引。create_time在索
引ind_***_buyerid里面，order_id是主键索引，但是这两个是不同的索引，多字段排序时无
法利用索引排序。同样可以通过show profile来验证，如下：
同一 个 SQL， 对比
create_time desc排 序 （ q
uery 3） 和 create_time desc,order_id asc排
序（q
uery 2），可以发现前者利用索引排序（Sorting result），耗时很低0.000019，后者
走文件堆排（Creating sort index），耗时很高0.094799。
去掉order_id排序
为了解决上述慢SQL，最简单
的办法就是把order_id排序去掉，不过在此之前先回顾下增加
order_id排序的背景。24年做订单列表后置过滤治理时，tm2在订单列表查询条件中新增了一
个m_tid字段，该字段用于过滤掉不在手淘上展示的订单，从而实现在DB侧前置过滤掉不在手
淘上展示的订单，不用后置到tm2内存过滤。不过m_tid字段没有
索引，为保证压测通过，新增
了 索 引 `idx_***_mtid`
(`buyer_id`,`is_main`,**************,`create_time`,*************) 。因 为 create_time
是排序条件，不是查询条件，所以新索引把create_time字段放到索引中倒数第三的位置上。
```

## PDF 第4页

[查看原页](RAW.pdf#page=4)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
基于新索引，DB单实例压测和全链路压测
都没问题，但是tm2在放量结束后的第二天上午突然
出现了
大量订单找不到或者订单重复的舆情，典型的case如下：
在dms上通过force index指定索引的方式复现了上述问题，发现走老索引没问题，走新索引有
问题，二者的explain差异如下：
```

## PDF 第5页

[查看原页](RAW.pdf#page=5)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
跟DBA沟通确认，走老索引ind_***_buyerid时，因为create_time字段在索引中第二个字段，
create_time desc排序可以直接利用索引排序，返回的订单ID是按照
索引里面固定的顺序返
回 。走 新 索 引 idx_****_mtid时 ，因 为 create_time是 索 引中 倒 数 第 三 个 字段 ， create_time
desc排序只能走文件堆排，而第一页订单请求和第二页订单请求的文件堆排的排序结果可能不
同，即A1-A6的顺序是不确定的，一旦
两次排序顺序不同，计算分页时获取的订单就可能出现
重复或者订单
缺失的问题，比
如第一页订单请求时排序是A1,A2,A3,A5,A4,A6,取前面4条，第
二页订单请求时排序是A1,A2,A3,A4,A5,A6，取后面2条，即出现A4缺失，A5重复的问题。因
为 索 引二 次变 更 没有足 够 的 时 间 窗口， 当 时决策 采用风险 相对 较小 的方
案 ， 把排 序 条 件 从
create_time desc改成create_time desc,order_id asc排序，通过order_id asc来保证创
时 间一 致 的 情 形 下 返 回 的 订单列表 的 稳 定 。因 为二级
索 引 的 叶子 节点里面 本 身 是 包 含有
order_id字段的，所以不会新增回表查，对DB的影响主要是新增order_id排序本身的损耗，通
过DB单实例压测验证这部分损耗对整体CPU水位的影响不明显，后续也通过了双11考验。
单
明确增加order_id排序的原因后，就制定了一种风险相对较小的优化方式，把非tm2订单列表
即不 带m_tid 字段 的 分页 查 询 请 求 中 的 order_id排 序 去 掉 ， 预 期 这 类 SQL 应 该走老 索 引
ind_***_buyerid，从而保证返回的订单列表的稳定。放量完成后
发现不带m_tid字段的分页查
询请求也会走到新索引 idx_****_mtid，如下：
查询条件中带有
create_time的范围查询，理论来说走老索引ind_***_buyerid更优，可以走索
引 过 滤而 不 是 索 引 下 推 过 滤 。 实 际 测 试 发 现 当 查 询 时 间 是 2025-08-01 会走老 索 引
ind_***_buyerid，如下：
```

## PDF 第6页

[查看原页](RAW.pdf#page=6)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
该用户下创
单最早的订单
都是大于2025-01-01，初步怀疑create_time大于2025-01-01的查
询条件被索引选
择器直接忽略。如果把查询时间去掉，也是走新索引 idx_****_mtid，相比老
索引可以有更多的字段走索引过滤，符合预期。
可以通过INFO
数：
R
MATION_SCHEMA.INDEX_STATISTICS表 来查看走各个索引查询返回的记录
```

## PDF 第7页

[查看原页](RAW.pdf#page=7)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
基于上述统计结果可知，实际查询中有很多case依然走新索引idx_****_mtid。为了彻底解决
新索引带来的排序问题，同时解决业务要求的新的查询字段加索引问题，决策再次调整订单
表
的索引。
索引知
识回顾
磨刀不误砍柴工，先系
统回顾总结下相关
的知
识点，打好理论基础。
▐ 索引分类
▐ B+Tree数据结构
找了一圈资料，发现只有下面这张图是比
较清晰和准确的，下面基于这个图来做补充。
```

## PDF 第8页

[查看原页](RAW.pdf#page=8)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
B
+
Tree是一个多
叉树，即子节点的数量可以大于2，与之相对的红黑树最多只有2个子节点。
B
+
Tree中一个节点的子节点数目的最大值就是B
+
Tree的阶，比
如8阶B
+
Tree最多有8个子节
点。B
+
Tree通过增加子节点的数量可以大幅增加单层B
+
Tree的节点数（比
如3层8阶的B
+
Tree
第三层的节点数等于8*8*8=252，3层的红黑树第三层的节点数等于2*2*2=8），从而大幅降
低整体的树高度，减少查询过程中的磁盘访问，提升读写效率，比
如图中树的高度是3，从根
节点到叶子节点只需要3次磁盘访问即可返回。
B
+
Tree中
单个节点实际对应一个16kb
的物理Page，Page的Fil Header中会维护两个链表指
针，指向相邻的两个Page，通过这两个指针，每一层的Page都会组成一个横向的Page双向链
表，从而支持双向遍历，提升列表查询效率。每个Page中会包含多条索引记录Record，各个
Record在逻辑上基于索引列值升序排列并组成一个单向链表，这些称为User Records。Page
内预留了两个固定位置固定值的System Records，在链表头
的Infim
u
m记录以及在链表尾的
Su
prem
u
m记录，Infim
u
m指向索引值最小的Record，Su
prem
u
m通常为null。Page内部还会
维护一组Directory slot，每个Directory slot指向一个Record记录，两个Directory slot对应
的Record记录中间会相隔4到8个Record记录，实际在Page内部查找满足条件的Record记录
时先根据Directory slot做二分查找找到相邻的两个slot记录，再顺序遍历这两个slot中间的
Record记录，从而提升查找效率。
```

## PDF 第9页

[查看原页](RAW.pdf#page=9)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
B
+
Tree中的节点分为三种，根节点、叶子节点和中间的非叶子节点，其中主键索引根节点对应
PageNo默认是3，可以根据PageNo和PageSize计算出文件偏移量，再根据偏移量从idb文件
中读取对应PageSize的字节数据，再按照约定的数据存储格式即可解析出来存储的原始数据。
三种节点包含的Record的Header部分基本一致，主要区别是Data部分。其中根节点和非叶子
节点记录的Data是索引字段的值和指向下层子节点的PageNo，如果是主键索引则只有一个索
引字段，如果是二级
索引则可能存在多个索引字段，注意索引字段的值是下层子节点中所有
Record中最小的且每个Record都对应一个下层节点，比
如图中Page4 Record为0的记录指向
Page6，包含0和1两条记录，Record为2的记录指向Page7，包含2和3两条记录。对于叶子节
点包含的Record，如果是主键索引则Data是索引字段的值以及其他的非索引字段的值，这两
者加起来构成完成的一
行数据，比
如图中的A,B,C,D,E,F,G,H就是非索引字段的取值；如果是
二级
索引则Data是二级
索引各个字段的值加上主键索引字段的值，如下图：
对应的原始数据如下：
order_id create_time is_main status type
1 1752595200 0 0 10000
2 1752595200 0 0 200
3 1752595200 1 0 200
4 1752595201 1 0 5000
5 1752595202 1 1 200
6 1752595203 0 0 10000
```

## PDF 第10页

[查看原页](RAW.pdf#page=10)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
7 1752595203 1 0 200
8 1752595203 1 0 261
二级
索引顺序是按照多个索引字段的顺序从左往右依次比
较，跟比
较两个字符串的顺序的规则
基 本一 致 ，比
如上面 的 case ， 先比
is_main，is_main一致的情况下再比
较 create_time ， create_time一 致 的 情 况 下 再比
较
较status，这样设计会导致二级
索引只有第一个字段是
有
索引前面的字段的值是确定的，则后面的第
序的，其他的字段实际存储都是无序的；如果二级
一个字段的存储也是
有序的。
二级
INFO
索引的Root Page的PageNo是通过索引的元数据表
R
MATION_SCHEMA.INNODB_SYS_INDEXES 维护的，如下：
▐ B+Tree的高度测算
单个Page包含的Record记录数取
决于
单个Record的大小，以tcorder为例分析，主键索引是
order_id，BIGINT类型，占8个字节，非叶子节点的Record的大小约为8
+
5（Header）
+
4(子
节点 PageNo 指 针 )=13 ，单个 Page 包 含 的 最大 的Record 数 量为 （ 16*1024-200
（Header））/13=952。叶子节点的大小为单
的
长5.4kb
行
行
+
20（Header）=5.5kb，单个
Page包含的最大的Record数量是2。据此不同高度的B
+
Tree支持的最大记录数如下：
高度非叶子节点数量 叶子节点数量 最大记录数
1 0 1 2
2 1 952 952*2=1904
```

## PDF 第11页

[查看原页](RAW.pdf#page=11)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
3 1
952=953 952*952=906304
+
952*952*2=18126
08
4
1
952
+
+
952*952=
907257
952*952*952=86
2801408
952*952*952*2=1
725602816
索 引 `ind_***_buyerid` 的长 度 是 58，非 叶子 节点 的Record的长 度 约 是 58
5
4=67，单个
+
+
Page 包 含 的 最大 的Record 数 量为 （ 16*1024-200 （ Header ） ） /67=241 。 叶子 节点 的
Record的长度是67
8（主键索引）
+
+
20（Header）=95，单个Page包含的最大的Record数
量是（16*1024-200（Header））/95=170个。据此不同高度的B
+
Tree支持的最大记录数如
下：
高度非叶子节点数量 叶子节点数量 最大记录数
1 0 1 170
2 1 241 241*170=1904
3 1
+
241=242
241*241=58081
241*241*170=987
3770
4 1
241
+
+
8323
241*241=5
241*241*241=139
97521
241*241*241*170=
2379578570
通过上述测算可知：
1. tcorder单
表的量级在800w左右，按照上面的测算，主键索引B
+
Tree的高度是4，二级
索
引B
+
Tree的高度是3。
2. 在存储同等量级
的数据的前提下，
行
长和索引长度增加会导致单个Page包含的Record数量
减少，导致B
+
Tree的高度增加，导致读写效率下降，所以需要限制
表的字段数量和索引
的字段数量。
3. 对于二级
索引，索引长度不超过50，单
表控制在1000w
以内，B
行
+
Tree的高度不超过3。
4. 对于主键索引，
长
不超过1.5kb，单
表控制在1000w
以内，B
行
行
+
Tree的高度不超过3。
单
▐ B-Tree的数据结构
```

## PDF 第12页

[查看原页](RAW.pdf#page=12)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
B
+
Tree是从B-Tree改进而来，两者的区别如下：
m阶B-Tree m阶B
+
Tree
子节点数量 m+
1 m
非叶子节点是否包含非索引
字段数据
是 ，任 何 索 引 记 录 只 存 在 于
一个节点中
否 ，非 叶子 节点 只 存储 索 引
字段 ， 只用 于二 分 查 找 ，因
此 同一 个 索 引 记 录 可 能 出 现
在 多 个非 叶子 节点中 ， 只有
叶子 节点 保 存 了 完 整 的 索 引
数据
同一层的节点是否有双向指
否 是
针
优势
没有 数 据 冗 余 ， 数 据 规模 较
小 时 ，因 为 命中 了某 个非 叶
子 节点 即 可 返 回 ， 点 查 场 景
下查询效率更高
在大 规模 数 据 下 因 为非 叶子
节点 包 含 的 索 引 记 录 更 多 ，
从而降
低 整 体 B
+
Tree 的高
度，提升查找效率。
每 次查 询 必 须走 到 叶子 节
点 ， 从而 保 证 查 询RT 的 稳
定。
同一 层 的 节点有 双 向指 针 ，
提高列表查询的效率。
缺点
每 次查 询 命中 的 节点 的 树高
度可能不一致导致查询RT不
稳定
同一 层 的 节点 没有 双 向指
针，不利于列表查询。
有数据冗余
同样的数据，B-Tree的数据结构如下：
```

## PDF 第13页

[查看原页](RAW.pdf#page=13)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
▐ explain说明
```

## PDF 第14页

[查看原页](RAW.pdf#page=14)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text

```

## PDF 第15页

[查看原页](RAW.pdf#page=15)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
explain 的
输 出 默 认 是 表 格模 式的 ，还
有一 个 json 格式，输 出 的 信 息 更 详 尽 ， 通 过 explain
format=json SQL的方式获取，以这个SQL为例：
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
select
********
from
(
select
order
id
_
from
`tcorder
`
where
is
main = 1
_
and buyer
id = 1*******1
_
**************
order by
create
_
time desc,
`
order
id`
_
limit
0, 10
) t2,
`tcorder
` t1
where
t2.order
id = t1.order
_
_
id
asc
对应的表格
输出如下，输出的表的顺序并不是实际的执
顺序，而是先外层表再内层表。
行
对应的json输出如下：
1
2
3
4
5
6
{
"query_
block": {--最外层的SQL的执
"select
_
id": 1,
"cost
info": {
_
"query_
cost": "17.25"
},
成本
行
--预估的成本值，不是预估耗时，只能用作
横向比
较
```

## PDF 第16页

[查看原页](RAW.pdf#page=16)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
"nested
_
loop": [--
按照执
行
顺序列出来多个内层SQL预估的执
行
成本
{
"table": {
"table
name": "t2"
_
,
"access
_
type": "ALL"
,
"rows
examined
_
_per
_
scan": 5,
--预估的扫描
行数
"rows
_produced
_per
_join": 5,
--预估的返回上层的
行数
"filtered": "100.00"
,
"cost
info": {
_
"read
cost": "10.25"
_
,
--预估的
单次读取数据的成本
"eval
cost": "1.00"
_
,
--预估的将单次读取的数据按照
where条件过滤一遍
"prefix
cost": "11.25"
_
,
--整体的查询成本
"data
read
_
_per
_join": "80"
--预估读取的数据量，单位字节
},
"used
columns": [
_
"order
id"
_
],
"materialized
from
_
_
subquery": {--表示t2是物化子查询产生的
"using_
temporary_
table": true,
--使用了临时表保存结果
"dependent": false,
--表示子查询的where条件跟外层SQL无关，在外层执
"cacheable": true,
--表示子查询的结果可以缓存
"query_
block": {
"select
_
id": 2,
"cost
info": {
_
"query_
cost": "20928.00"
},
"ordering_
operation": {--表示需要排序
"using_
filesort": true,
--表示走文件堆排排序
"table": {
"table
name": "tcorder"
_
,
"access
_
type": "ref"
,
"possible
_
keys": [
"ind
***
_
_
buyerid"
,
"idx
***
_
_gmtcreate"
],
"key": "idx
***
_
_gmtcreate"
,
"used
_
key_parts": [--表示实际生效的索引列
"buyer
id"
_
],
"key_
length": "8"
,
"ref": [
"const"
],
"rows
examined
_
_per
_
scan": 17440,
"rows
_produced
_per
_join": 5,
"filtered": "0.03"
,
```

## PDF 第17页

[查看原页](RAW.pdf#page=17)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
--index
condition表示通过索引下推过滤的查询条件
_
"index
condition": "
_
****************
((`tcorder
`
.
`buyer
id`
<=> 117075031) and (``tcorde
_
***************
"
,
"cost
info": {
_
"read
cost": "17440.00"
_
,
"eval
cost": "1.18"
_
,
"prefix
cost": "20928.00"
_
,
"data
read
_
_per
_join": "236K"
},
"used
columns": [
_
"order
id"
_
,
"buyer
id"
_
,
*************
],
--attached
_
condition表示通过mysql服务器层过滤的where条件
"attached
condition": "((ifnull(`tcorder
`
`
.
attribute
_
}
}
}
}
}
},
{
"table": {
"table
name": "t1"
_
,
"access
_
type": "eq_
ref"
,
"possible
_
keys": [
"PRIMARY"
],
"key": "PRIMARY"
,
"used
_
key_parts": [
"order
id"
_
],
"key_
length": "8"
,
"ref": [
"t2.order
id"
_
],
"rows
examined
_
_per
_
scan": 1,
"rows
_produced
_per
_join": 5,
"filtered": "100.00"
,
"cost
info": {
_
"read
cost": "5.00"
_
,
"eval
cost": "1.00"
_
,
```

## PDF 第18页

[查看原页](RAW.pdf#page=18)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
99
100
101
102
103
104
105
106
107
108
109
110
"prefix
cost": "17.25"
_
,
"data
read
_
_per
_join": "200K"
},
"used
columns": [
_
"order
id"
_
,
****************
]
}
}
]
}
}
综
合上面json的
输出可知上述SQL的实际执
行
过程大致如下：
1. 先执
行
子查询（select_id=2），扫描 tcorder 的索引 idx_***_gmtcreate（约 17440 条
候 选 ） ， 应用 index_condition （ ICP ） 以 减 少 要 回表 的
行 数 ； 仍 需 对
attached_condition 做服务器端判断；对结果做排序（using_filesort），把结果物化到
临 时表 （using_temporary_table=true） 。 物 化 后临 时表 （ t2） 约有 5
行
（非 常小 且
cacheable，因为 dependent=false）。
2. 外层扫描临时表 t2（ALL，5
行
），对每个 t2.order_id 用主键在 t1 上做 eq_ref 点查
（一次找到一
行
），最终组合出 5 条输出
。
行
▐ Query Profiler
MySQL 的 Query Profiler 是一个使用非常方便的 Query 诊断分析工具，通过该工具可以获
取一条Query 在整个执
过程中
行
不同阶段多种资源的消耗情况，如耗时、CPU，IO，IPC，
SWAP 等 ， 以 及
发生 的 PAGE FAULTS， CONTEXT SWITCHE次数 等 等 ， 同 时还 能 得 到 该
Query 执
行
过程中 MySQL 所调用的各个函数在源文件中的位置，其具体用法如下：
命令 说明 示例
show variables like 'profil
ing'
查看 是 否 开启
默认关
闭
profile功 能 ，
set profiling = 1
开启 Query Profiler 功 能 ，
开启
后 执
行
任 何 SQL
都会 被
采集Profiler信息
```

## PDF 第19页

[查看原页](RAW.pdf#page=19)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
show profiles
-查看当前保留的采集了pro
file信息的SQL列表，默认是
最多保存15个，通过参数pr
ofiling_history_size控制
SHOW PR
OFILE [type] [F
O
R QUERY n] [LIMIT row
_count [OFFSET offset]]
查看 具 体 的 profile信 息 ， ty
pe取 值 可 以 是 ALL\BLOCK
IO等，多个type之间用逗号
间隔。FO
R QUERY n中的n
是 SHOW PR
OFILES中 的 编
号 ， 可 以 查看 指 定 缓 存 的 Pr
ofiling 信 息 。LIMIT OFFSE
T控制
的是一条查询的Profili
ng信息中
输出哪部分
（阶
行
段）的信息。直接执
行SHO
W PR
OFILE展示的是最新一
条被缓存的Profiling信息
type的取值如下：
取值说明
ALL 显示所有
的开销信息
BLOCK IO 显示块IO相关开销
CONTEXT SWITCHES 显示上下文切换相关开销
CPU 显示CPU相关开销信息
IPC 显示发送和接收相关开销信息
MEM
O
RY 显示内存相关开销信息，5.7版本未实现
PAGE FAULTS 显示页面错误相关开销信息
SOU
RCE
显 示 和 Source_function， Source_file， Source_lin
e相关
的开销信息
```

## PDF 第20页

[查看原页](RAW.pdf#page=20)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
SWAPS 显示交换次数相关开销的信息
Profiler采集的信息最终保存在INFO
R
MATION_SCHEMA.PR
OFILING表中，相关字段说明如
下：
取值说明
QUERY_ID 查询语句的ID
STATE 具体的状态，对应输出结果的status列
Duration 状态总持续时间，单位秒
CPU_user用户CPU时间，单位秒
CPU_system系
统CPU时间，单位秒
Context_voluntary 上下文主动切换次数
Context_involuntary 上下文被动切换次数
Block_ops_in 磁盘阻塞写入次数
Block_ops_out 磁盘阻塞读取次数
Messages_sent 发送的消息量
Messages_received接收的消息量
Page_faults_major 主要页面错误的数量
Page_faults_minor 次要页面错误的数量
Swaps 交换次数
Source_function 原函数（调用源码中的函数）
Source_file 源文件（MySQL源码中对应的.cc文件）
```

## PDF 第21页

[查看原页](RAW.pdf#page=21)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
Source_line 源代码行
（对应源码文件中的代码行数）
status的取值如下：
取值说明
starting
checking permissions（ 或 checking per
missions on table）
Waiting for q
uery cache lock
MySQL 为 执
流程）。
该语 句 做 初 始 准备 （启 动 执
行
行
检 查用 户 权 限 ， 确 认 是 否有 访 问表 / 列的 权
限。
等待查询缓存的锁（如果启用了 q
uery_cac
he），常见于并发环境
Opening tables
打 开 表 （ 打 开文 件 /表 句 柄、
这是执
前的准备。
行
表 定义 等 ） ，
After opening tables / After opening ta
bles
System lock
表 示 已完 成 打 开 表 的 步 骤 （有 时 重 复出
现）。
获取
全 局 / 系
统
级 锁 （ 各 种 内 部 同 步 ） ， 旧
存储引擎或元数据操作时可见。
Waiting for table metadata lock/Waitin
g for metadata lock / Waiting for table
lock
等待元数据锁（MDL），例如其他会话正在
做 ALTER/LOCK TABLE 等。
init
optimizing / optimizing (or optimise)
statistics
初 始 化 执
行
环 境 （ 分配 内 存、 初 始 化 变 量
等）。
优 化器 进
行 重 写 / 选
索 引 并生 成 访 问计
择
划。
收集统计信息（表
、索引基数、列分布等）
以估算成本（优化器用这些信息）。
preparing 为执
做最后准备（例如为执
行
部分生成临时结构）。
计划的某些
行
```

## PDF 第22页

[查看原页](RAW.pdf#page=22)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
Sending data
通 常表 示 把 结 果
行
从 存储 引 擎 / 服 务器 发 送
到客户端、或是执
行
过程中从存储引擎读取
并向上层传递
。
行
executing
表示运
语句的服务器端逻辑（包括存储过
行
程/函数/触发器
存储引擎的执
的代码、
表
达式求值、调用
逻辑等），这是一个比
较通
行
用的执
阶段标识。
行
Copying to tmp table
将 结 果 复制 到临 时表 （当 需 要 Y、 DISTINCT、
某 些 O
物化时）。这是将数据写入
GR
OUP B
RDER BY、子 查 询
临时表的阶段。
创建临时表结构（内存或磁盘）以便后续使
Creating tmp table
Sorting for grou
Sorting result
p / Sorting for order /
Creating sort index / Repair by sorting
用。
对数据做排序（filesort），可能用于 GR
O
UP BY、 O
RDER BY 。 filesort 多 时开 销
大。
与 索 引 重 建 或修 复相关 （不 常见于 普 通 查
询，常见于 REPAIR 操作）。
Waiting for table level lock / Waiting fo
r table flush
等待表
级锁或表刷新相关
Sorting for grou
p
为 GR
OUP BY 排序或准备聚合（可能和 lo
ose index scan 相关）
end / q
uery end 查询逻辑结束，进入收尾阶段。
closing tables关
闭已打开的表/文件句柄。
freeing items 释放表
达式/缓存所占资源（清除内存）。
cleaning u
p 最终清理，回收分配
、释放临时表等。
各个阶段的准确含义可以根据打日志对应的源码位置翻阅源码确认。根据各个阶段的耗时情况
可以分析某个慢SQL的问题根因，比
如排序耗时占比过高则需要优化排序逻辑或者给排序字段
```

## PDF 第23页

[查看原页](RAW.pdf#page=23)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
加 索 引 。 注 意 Query Profiler 在 mysql EXPLAIN ANALYZE功能来分析单个SQL的实际执
8.0 以 上 版本 已经 废 弃 ， 可 以 使用 功 能 更 强大 的
过程。
行
▐ 索引下推
先看看没有
索引下推的情形，如下SQL：
1
2
3
4
5
6
7
explain select
*
from
`tcorder
`
where
`
parent
id`
= 37*******0834
_
and `from
`
_group
= 3;
输出结果：
据此可知，上述SQL
完全命中的索引ind_***_parentid(parent_id,from_grou
p)且通过const
常量方式查询索引，最多命中一
行
记录，此时是存储引擎根据索引找到符合条件的记录后再回
表获取
完整的记录
行
。因为是const常量访问，此时Extra为NULL，没有显示Using Index。
调整查询条件from_grou
p为大于，如下：
1
2
3
4
5
6
7
explain select
*
from
`tcorder
`
where
`
parent
id`
= 37*******0834
_
and `from
`
_group
> 3;
输出结果：
```

## PDF 第24页

[查看原页](RAW.pdf#page=24)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
json格式的结果如下：
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
{
"query_
block": {
"select
_
id": 1,
"cost
info": {
_
"query_
cost": "1.42"
},
"table": {
"table
name": "tcorder"
_
,
"access
_
type": "range"
,
"possible
_
keys": [
"ind
***
_
_parentid"
],
"key": "ind
***
_
_parentid"
"used
_
key_parts": [
"parent
id"
_
,
"from
_group"
,
],
"key_
length": "12"
,
"rows
examined
_
_per
_
scan": 1,
"rows
_produced
_per
_join": 0,
"filtered": "100.00"
,
"index
condition": "((`tcorder
`
`
.
_
parent
id`
_
"cost
info": {
_
"read
cost": "1.18"
_
,
"eval
cost": "0.08"
_
,
"prefix
cost": "1.42"
_
,
"data
read
_
_per
_join": "15K"
= 37*******0834) and
},
"used
columns": [
_
"order
id"
_
,
***************
]
}
}
}
```

## PDF 第25页

[查看原页](RAW.pdf#page=25)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
Using index condition表 示 使用 了 索 引 下 推 （ index condition p
ushdown ， 简 称 ICP ） ，
json输出中index_condition表明parent_id和from_grou
p两个条件都通过索引下推来做过滤
了。
假设满足
parent_id条件的
有10条，同时满足两个条件的只有1条，不
过程如下：
1. 存储引擎读取满足
parent_id条件的10条索引记录。
2. 存储引擎根据索引记录中的主键ID读取10
行
完整的
行
记录。
3. 存储引擎返回给mysql server层，由server层完成剩余的from_grou
客户端。
开启ICP时，整体的查询
p条件的过滤并返回给
开启ICP时，整体的查询过程如下：
1. 存储引擎读取满足
值来做from_grou
parent_id条件的10条索引记录，利用索引中记录的from_grou
p条件的过滤，并最终返回1条索引记录。
2. 存储引擎根据索引记录中的主键ID读取1
行
完整的
行
记录。
3. server层直接把存储引擎返回的1
行
记录返回给客户端。
p字段的
整个查询过程中回表的次数就从10次降
低为1次，从而提升整体的效率。ICP是默认开启
的（通
过参数index_condition_p
ushdown控制），为了充分发挥ICP的优化效果，需要把区分度大
的字段尽可能加入到二级
索引中，从而大幅降
低回表查的次数。
查询的字段在二级
索引中，命中下列情形时也可能不使用ICP:
1. 如果索引已覆盖所需返回列，无需回表，Extra显示Using index。
2. 为了满足
O
RDER BY/LIMIT，优化器可能选
择
3. 查询条件中包含非确定性/有副作用函数，比
按
索引顺序扫描或 filesort。
如now()/RAND()等，必须在server层执
行
滤。
4. 优化器
估算的候选条目很少导致下推收益小，优化器可能选
择
在服务器层过滤。
过
比
如下面的SQL：
1
2
3
4
5
6
7
8
9
select
order
id
_
from
`tcorder
`
where
is
main = 1
_
and buyer
id = 117075031
_
***************
-- and (
```

## PDF 第26页

[查看原页](RAW.pdf#page=26)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
10
11
12
13
14
15
16
17
-- ifnull(attribute4, 0) <> 1
and ifnull(attribute4, 0) <> 2
-- -- )
***************
order by
create
time desc
_
limit
0, 10;
注掉attribute4条件，所有
的查询字段和返回字段都在索引里面有，不需要回表，explain结果
如下：
执
过程：通过mysql server层来完成索引记录的过滤，从索引记录中读取order_id后直接返
行
回，不回表。
恢复attribute4条件，因为attribute4不在索引里，需要回表查，所以不显示Using index，如
下：
执
行
过程：server层完成索引记录的过滤后回表查完整的记录
行
，再执
行
attribute4的过滤。
去掉order by条件，显示Using index condition，如下：
执
行
过 程： 除 attribute4 外 在 存储 引 擎 层 过 滤 ， 过 滤完 成 后 回表 查 ， 在 server 层完 成
attribute4字段的过滤。
▐ 排序优化
mysql处理order by时先判断能否使用索引来做排序，判断标准是排序条件必须跟索引B
+
Tree
叶子节点的排序完全一致。因为索引B
+
Tree叶子节点中的数据本身就是排序好的，基于索引顺
序 或者 倒 序 读取 出 来 的 记 录 可 以 直 接 返 回 给 上 层 ，不 需 要 额 外 的 排 序 操 作 。 以 索 引
ind_***_parentid(parent_id,from_grou
p)为例说明，如下情形可以利用索引排序：
```

## PDF 第27页

[查看原页](RAW.pdf#page=27)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
1
2
3
4
5
6
select * from tcorder order by parent
_
id;
select * from tcorder order by parent
_
id,from
_group;
select * from tcorder where parent
_
id=1234 order by from
_group;
select * from tcorder where parent
_
id>1234 order by parent
_
id;
select * from tcorder where parent
id=1234 and from
_
_group>1 order by fr
select * from tcorder order by parent
_
id desc,from
_group desc;
如下情形不能走索引排序：
1
2
3
4
5
select * from tcorder order by from
_group;
select * from tcorder order by abs(parent
_
id);
select * from tcorder where parent
_
id>1234 order by from
_group;
select * from tcorder where from
_group=1 order by parent
_
id;
select * from tcorder order by parent
_
id desc,from
_group asc;
不能使用索引排序时，explain就会显示Using filesort，这里的filesort是一个统称，如果排序
的数据量小则在内存通过快速排序算法排序，这块内存叫sort buffer，通过sort_buffer_size
控制
大小，默认为2m，基于DB链接维度分配；如果数据量大则借助磁盘临时文件通过多路归
并算法排序，因为磁盘的读写效率远低于内存，所以要避免使用磁盘临时文件排序。另外如果
order by后面跟着limit m,n的话，则会优化成基于内存的优先级队列的方式排序，但是如果
m+
n条数据超过了排序内存的容量还是会退化到借助磁盘临时文件排序的方式，所以要避免
非
必要的
深翻查询，容易导致慢SQL。
两
种排序方式都是基于排序key来做排序，排序key前面是参与排序的字段值，如果有字符串类
的字段参与排序，则最大只允许max_sort_length字节（默认是1024）的数据参与排序。排序
key后面的部分默认是其他的需要返回的字段，称为全字段排序；如果排序key的总长度超过
max_length_for_sort_data（默认是1024），则排序key后面的部分变成主键ID，称为rowId
排序，从而减少排序key的长度，避免使用磁盘临时文件排序，等整体排序完成后再根据这个
主键ID回表获取需要返回的各个字段。filesort整体的流程如下：
```

## PDF 第28页

[查看原页](RAW.pdf#page=28)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
实际的排序过程中是否触发
了优先级排序或者临时文件排序，可以通过optimizer_trace日志来
做 确 认 ， 该日 志 主 要用 来 跟 踪 优 化器
的 执
过 程 ， 默 认关
行
闭 ， 通 过 set
optimizer_trace="enabled=on";开启，另外为了保证trace日志能被完整保留，需要调整缓存
大小set optimizer_trace_max_mem_size=1638400；注意这两个变量修改只能DBA黑屏操
作。如下：
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
{
"filesort
{
_
information": [--
排序的字段和顺序
"direction": "desc"
,
"table": "`tcorder
`"
,
"field": "create
_
time"
},
{
"direction": "asc"
"table": "`tcorder
"field": "order
_
,
`"
id"
,
}
],
"filesort
_priority_queue
_
optimization": {
"limit": 10,
--查询SQL中带了limit 10
"rows
_
estimate": 285372816,
--预估的参与排序的总
"row
_
size": 67,
--预估的排序key的大小
行数
```

## PDF 第29页

[查看原页](RAW.pdf#page=29)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
18
19
20
21
22
23
24
25
26
27
28
29
30
"memory_
available": 2097152,
--sort buffer的大小
"chosen": true--
说明使用了优先级队列排序
},
"filesort
execution": [
_
],
"filesort
_
summary": {
"rows": 11,
--最终返回给上层的
行数
"examined
_
rows": 10597,
--
实际处理的
行数
"number
of
_
_
tmp_
files": 0,
--使用的临时文件的数量，为0表示未生成
"sort
buffer
_
_
size": 832,
--
实际使用的sort buffer的大小
"sort
mode": "<sort
_
_
key, additional
_
fields>"
--
排序key的构成
}
}
注意mysql排序使用的三种算法快速排序、优先级队列排序和多路归并排序 都存在键值相同的
记录排序顺序不
相等时保持输
稳定的问题，这并不是mysql的bug而是SQL规范并不要求在 O
RDER BY 键值
入顺序不变，mysql的文档也明确说明了该问题：
为了保证排序结果的稳定，只能基于索引排序或者把主键ID加入到排序字段中。
索引变更SOP
▐ 分析慢SQL类型和根因
1. 基于dbTrace的离线日志分析捞
主要的调用来源应用。
取最近一周慢SQL量级前20的慢SQL的SQL Parttern ID和
2. 根据SQL Parttern ID和调用来源应用名到dbTrace在线日志中查询最新的慢SQL日志，从
日志中拿到带有
参数的慢SQL和最新的traceId。
3. 通过explain命令分析带有
监控中查询该慢SQL的执
行
参数的慢SQL，同时根据SQL Parttern ID去dbservice的慢SQL
统计信息初步确认慢SQL原因。
4. 第三步排查下来发现并非索引问题，需要进一步排查产生慢SQL时DB的CPU/活跃链接数/
磁盘读写/网络带宽等以及应用机器
的GC/网络丢包等是否有
异常，如果存在异常需要先排
查异常的根因。
```

## PDF 第30页

[查看原页](RAW.pdf#page=30)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
5. 拿着最新的traceId找来源应用的owner了解上游业务场景，跟业务沟通确认能否调整查询
条件或者切换查询接口，优先考虑业务调整的方式来解决慢SQL。
6. 明确只能通过索引变更的方式来解决的慢SQL的类型和量级，这些也是索引变更完成后用
来评价新索引是否符合优化预期的重要依据。
▐ 分析全量查询SQL构成
1. 从dbTrace离线
表
捞
文本和对应的量级
的占比
。
2. 从SQL文本中解析出来查询字段，结合对应SQL的查询量级
占比
。
3. 明确各个查询字段的具体含义
取待优化表的最近一周排名前100的SQL Parttern ID、带问号的SQL
算出来不同字段的查询量级和
、在实际业务中的用法，据此推算出该字段的区分度。
▐ 确认索引字段顺序
联系DBA、SRE、应用owner、leader一起讨论，结合前面2步的分析结果确认二级
字段的顺序，参考以下原则：
索引中多个
1. 分库分表的字段排在第一位，比
如buyer_id/seller_id，这个字段是区分度最大的。
2. 参与排序的字段排在第二位，比
如create_time，避免通过filesort排序。
3. 查询频率高且区分度高且的字段排在中间。
4. 查询频率高但区分度低的字段排在最后。
5. 查询频率低的字段参考实际的慢SQL情况，可以考虑不放在索引中，比
比
可以引导上游业务切换查询字段。如果慢SQL
较多且上游强依
如gmt_modified，
的，则将其放在最后。
赖
▐ 提交结构设计工单
索引字段顺序确认完成后就需要在dms上提结构设计工单来完成索引变更，先在日常库执
行
走完审批流后再在生产库上执
行
。注意一下几点：
，
1. 日 常库 执
行
只 能 验 证 索 引 变 更 的 SQL本 身 是 否 正确 ，无 法 直 接 在日 常库 验 证 新 索 引 的 效
果，比
如日常库加完索引后执
行explain发现还是走老索引，此时并不能说明新索引比老索
引差，至少日常库的数据量级和特征分布无法跟线上库对齐，需要以线上库的验证结果为
准。
2. DRC同步时不会过滤alter table这类语句，因此存在多集群的情况下，只需要对中心集群
的逻辑库提变更工单即可。另外，因为alter table语句也是binlog日志的一部分且一个DB
实 例 只有一 个 有
效binlog文 件 ， DRC同 步 在 其 他 集 群 执
该DDL语 句 时 以 及 备 库 同 步 该
行
DDL语句时都会阻塞掉其他正常的数据变更，导致单元间DRC同步延迟，执
行变更期间需
```

## PDF 第31页

[查看原页](RAW.pdf#page=31)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
要监控DRC同步延迟是否超出预期，如果同步延迟大幅上涨，需要联系DBA调大执
索引
行
变更各分表间的时间间隔，比
如从10s调整到1m，DRC可以利用这1m来追平延迟的
变更。
延迟过高时一旦主库挂掉，发生主备切换，因为备库需要先回放未同步完的binlog日志，
导致备库有
较长的时间不可写入。
3. 当前RDS支持异步DDL，即执
DDL语句时不用等待其执
行
行
持用于磁盘碎片整理的optimize table语句生效，且只支持对备库生效。
完成即可返回，但是当前只支
4. 线上执
行
时需要选
起始执
择
行
时间，所有DDL类变更必须在凌晨业务低峰期执
行
，第二天
早上7点前停
止，从而降
低出现问题时的影响面。结构设计工单只能指定执
的起始时间，
行
无法设置任务停
止时间，只能人工暂停或者依
DB维度的
赖
变更窗口期暂停，一般核心DB会
配置变更窗口期，建议联系DBA确认。
5. 压测验证都是针对影子表，需要同时给线上表和影子表
创建结构设计工单，避免遗漏导致
压测失真。
▐ 线上灰度
1. 结构设计工单
线上执
行
较少建议选
分库维度，否则选
择
为支持继续自动执
的时候支持按照分表
、分库和实例三个维度来做灰度，如果实例数
择实例维度，原则是第一批灰度1%左右的查询流量。灰度
后续任务和暂停任务等待人工干预两
种，自动执
风险不可控，必
行
行
行
须选
择第二种。注意第一次执
行
时是由dms平台随机选
指定，等第一次执
完成后才能由工单执
行
行
人来手动选
一个分库或者
择
实例来执
行
，无法
执
的分库或者
择
行
实例。
2. dms按照分库或者
例只能有一个分表执
实例维度来执
DDL工单时，是按照分库加分表维度串
执
行
行
行
，一个实
行变更，先变更完某个分库下所有分表才会变更下一个分库，可以在
工单执
行详情中查看已经变更完成的和正在变更的分表。这样设计会拉长整体的灰度观察
时间，大幅降
低
变更风险，方便基于分库或者分表维度来排查问题，在变更期间需要密切
关注监控大盘是否有
异常抖动、星环日志画像是否有
新增的异常日志。
3. 第一批分库或者
实例维度的索引变更完成且确认没有
异常后 需要联系DBA 执
老索引的静
行
默，老索引静默后会正常更新但是对外不可见。一旦新索引有问题，先取消老索引的静默
并 将 新 索 引 静 默 掉 ， 确 认 新 索 引 问题后 再 提工单删 除 新 索 引 。 注 意 索 引 静 默 需 要 特殊 的
SQL语句，dms不支持，只能DBA黑屏操作。
4. 索引静默完成后，需要挑选一条真实的慢SQL在dms上执
了，老索引不可见，验证没问题后，需要线上观察一周左右。
行explain命令，验证新索引生效
5. 第一批索引变更线上观察期间可以基于dbTrace日志配置指定分库指定SQL Parttern Id的
RT监控以及慢SQL量级监控，通过对比
索引变更完成的分库和未变更的分库两者之前的
RT、慢SQL量级
的差异，注意选
对比
择
的分库间慢SQL的量级需要接近，避免慢SQL差异
把整体的平
RT拉长。因为不同分库间数据分布有轻微的差异，在交易场景比
较典型的就
是大买家的分布，会导致不同分库的查询RT天然就会不同，直接做比
较没有太大意义，只
均
```

## PDF 第32页

[查看原页](RAW.pdf#page=32)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
要两 者 的 差 异不大 即 可 ， 重 点关 注 慢 SQL量级
SQL量级可以根据dbTrace日志轻松获取。
的
变 化 ， 同一 个 分 库 变 更 前 后一 天 内 的 慢
▐ 压测验证
1. 第一批索引变更完成，观察3天左右确认RT没问题且慢SQL量级有显著下降
的影子表的索引变更工单，同样按照分库或者
后需要执
实例维度灰度，第一批索引变更完成后同样
对应
行
需要执
老索引的静默。
行
2. 准备 压 测 模 型 ， 注 意 压 测 模 型 必 须 要覆 盖 本 次索 引 变 更 需 要 解决的 慢 SQL
对 应 的 业 务 场
景，压测量级根据去年双11的量级计算出单实例压测的量级
。
3. 同时压测变更完成的实例和未变更的实例，对比两者间的cp
u
RT的差异，持续施压时观察两者的差异是否变大。
、活跃链接数、
逻辑读，读写
4. 持续施压时需要检查压测用户的数据分布是否符合预期，比
如订单场景需要校验单个用户
下 总 的 订单量， 订单量较小 时 新老 索 引 的 差 异不 会 明 显 ，因 为 数 据 量小 时 数 据 基 本都在
Buffer Pool中，即使全
表扫描也很快。
▐ 全量验证
1.
线上观察一周确认RT没问题、慢SQL量级有显著下降且压测验证没问题后可以执
行第二批
分库或者
实例的索引变更，优先执
行第一批用于对比
的分库，这样可以对比
同一个分库变
更前后的平
RT变化，规避数据分布差异的影响。第二批灰度5%，第三批灰度20%，第
四批剩余所有
的，每批优先灰度慢SQL较多的分库并用同样的方式
观察一周左右，整体耗
时1个月左右完成线上变更。
2. 线上变更完成后再一次性完成影子表的索引变更工单以及老索引静默。
3. 双11压测和大促验证通过后再提工单正式删除静默掉的老索引。
均
常见的慢SQL问题
这里
说的慢SQL是应用侧感知
的慢SQL，不是DB内核统计的慢SQL，DB执
行
慢、网络抖动或
者应用GC都会导致慢SQL。另外慢SQL整体可以分为两类，查询慢SQL和更新慢SQL，更新慢
SQL通常是
行
锁等待导致的，即存在多个大事务同时更新一
行
记录，其他事务更新时必须等已
经抢占到
行
锁的事务提交完成后才能抢占到
行
锁，可以借助dbTrace日志快速排查出现并发
冲
突的两个大事务，通常是调整业务逻辑或者加上全局限流来规避大事务的并发。
```

## PDF 第33页

[查看原页](RAW.pdf#page=33)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
查询类慢SQL的主要特征就是处理过程中平
均
逻辑读和同步物理读比
较多，解决慢SQL的核心
就是充分利用索引的二分查找特性来降
低逻辑读，常见的问题原因和治理措施如下：
问题原因 说明 治理措施
区 分 度大 的 字段 上 没有
索
引 ， 此 时 需 要 回表 查 ， 遍 历
大 量记 录 来 找 到 满足 指 定 条
件 的 记 录 ， 产生大 量随 机 I
O， 性能甚
比
至
顺 序 IO的全
表扫描要慢。
区 分 度 差 的 字段 （比
如状 态
类 字段 ） 没有
索 引 时 也 会 回
表 查 ， 但是因 为 过 滤 性不
强， 只 需 遍 历 少 量记 录 即 可
找 到 满足 条 件 的 记 录 ，不 会
导致慢SQL
将过滤性强的字段
二级
索 引 下 ， 范围 查 询 的 字
段排 在 前面 ， 等 值 查 询 的 字
段排在后面
根 据 上 述二级
索 引 的 数 据 结
构可知 ， 等 值 查 询 的 字段排
在 后面无 法 利用 索 引 过 滤 ，
排 在 前面 时 可 以走 索 引 过
滤 ， 进一 步 缩小 范围 查 询 遍
历 的 索 引 记 录 数 ， 即降
低 逻
辑读
将 等 值 查 询 的 条 件 排 在 范围
查询的前面
like 查 询 通配 符 % 在 前面 ，
此 时 相当 于 是 判断 某 个 字段
是 否 以 指 定 字符 串 结 尾 ，无
法利用索引来做过滤
字符 串 类 的 字段 在 索 引中 的
顺 序 是 基 于 字符 串 本 身 的 字
符 ， 从 左 到 右 依 次比
较 的 ，
所 以 判断 某 个 字段 是 否 以 指
定 字符 串 开头， 即 like 查 询
通配 符 % 在 后面 ， 可 以 利用
索 引 的
有 序 性来 缩小 索 引 遍
历范围
更改查询方式
索 引 字段 的 查 询 条 件 带有 函
数表
达 式， 此 时无 法 在 SQL
优 化 阶 段 确 认 函 数 的 值 ， 依
运
赖
行
时 索 引 字段 的 实 际 值
来 做 函 数 计 算 ， 所 以无 法 利
用索引
and ifnull(create_time, 0)
= SUBDATE(now(), INTER
VAL 51 DAY) ifnull 的 结 果
无 法 提前 确 认 ，无 法 利用 索
引
and create_time > SUBD
ATE(now(), INTERVAL 51
DAY) SUBDATE的 值 可 以 提
前计算，可以利用索引
更改查询方式
```

## PDF 第34页

[查看原页](RAW.pdf#page=34)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
优化器索引选
错误
择
fillsort排序
查询的数据在索引B
+
左侧但是按照
倒序排序
Tree的
count 查 询 命中 的 记 录 数 过
大
应用GC MySQL优化器依
赖
的统计信
息来源于Innodb
的周期性索
引页 采 样机 制 ， 没有 动 态 采
样或者 执
反 馈 能力的 ， 即
行
优 化器无 法 感 知
实 际 的 数 据
分 布， 如果 存 在 多 个 可用 索
引时可能导致索引选
错误
择
filesort排序需要把满足条件
的 记 录都查 询 出 来 才 能 执
行
排 序 动 作 ， 导 致 执
过 程中
行
产生 的 逻 辑 读 远 远大 于 预
期；另外filesort排序的记录
数 过 多 会 产生 磁 盘临 时文
件，进一步导致RT变
长
利用 索 引 来 排 序 时 会 根 据 排
序 的方 向来调整 索 引 叶子 节
点 的 读取方 向，比
如倒 序
排 ， 则从 右 往 左 遍 历 ， 正序
排 则从 左 往 由 遍 历 。 如果 查
询的数据在索引B
+
Tree的左
侧 ， 但是按 照
倒 序排 序 则意
味 着需 要 从 右 到 左 遍 历大 部
分 的 索 引 记 录 ， 增 加 没有
意
义
的逻辑读。
count 查 询 执
行
条 件 的 所有 记 录都
时 会 把 满足
捞 出 来 ，
导 致大 量的 逻 辑 读 ， 容 易 产
生 慢 SQL 。 mysql 下无 法 直
接 优 化 ， 只 能 结 合 具 体 的 业
务 场 景 考 虑 使用 count limit
子查询，mysql执
行
时判断
c
ount的结果达到了limit的限
制
后 会 中 断 扫 描 直 接 返 回 结
果，从而减少逻辑读。
GC 时 会 STW ， 导 致 应用 侧
感知到的RT较长，此时通常
合 理 设 计 索 引 ， 较 少 可用 的
索引个数
调整为基于索引排序
根 据 实 际 的 业 务 场 景 ，调整
排 序 顺 序 。比
如订单列表 场
景，通常是查询最近1周内的
数 据 ， 此 时 应 该使用 create
_time desc，不能使用crea
te_time asc。
结 合 上 游 的 业 务 场 景 分 析 去
掉非 必 要 的 count 查 询 或者
使用 count limit子 查 询 ，大
多 数 场 景 下不 需 要一 个 精 确
的 count 数 字的 ，比
如某 个
用 户 最 近 1个月 内 退 款 超 过 1
00笔时就不允许参加指定优
惠 活 动 ， 此 时不 需 要 count
所有
的退款记录，只需要co
unt limit 101笔即可。
应用GC治理
```

## PDF 第35页

[查看原页](RAW.pdf#page=35)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
是 1s内 产生 多 个 慢 SQL， 可
以 根 据 dbTrace 的 慢 SQL日
志快速确认
活跃链接数高，cp
u
高
不
通常是磁盘读写达到瓶颈，I
O处 理 变 慢 导 致 活 跃 链 接 数
高
磁盘升配
变
CPU
也会高
高，通常此时活跃链接
慢 SQL较 多 时 会 产生大 量的
逻辑读，CPU处理不过来，
导 致 其 他 正常的 查 询 请 求 的
CPU等待时间变
长，活跃链
接数升高
增 加 限 流 保 护， 推 动 慢 SQL
治理
主备切换
备库变主库时，buffer pool
缓 存 的 数 据 较 少 ， 产生大 量
的磁盘读，容易产生慢SQL
无
网络丢包
DB对外的网络带宽出现尖刺
时 ， 受网 络 丢 包 影响 可 能 导
致应用侧的RT边长，产生慢
SQL
排 查 产生 带宽 尖 刺 的 原因 ，
通 常是 同一 类 列表 查 询 请 求
被 定 时 触 发 ， 并 发 过高 导
致，调
低并发值即可
参考
13.7.5.30 SHOW PR
OFILE Statement：
https://dev.mysql.com/doc/refman/5.7/en/show-profile.html
8.2.1.14 O
RDER BY Optimization：
https://dev.mysql.com/doc/refman/5.7/en/order-by-optimization.html
8.2.1.17 LIMIT Query Optimization：
https://dev.mysql.com/doc/refman/5.7/en/limit-optimization.html
MySQL Order By排序的底层原理以及filesort排序：
https://juejin.cn/post/7132125495633641508
MySQL · 引擎特性 · 排序实现：http://mysql.taobao.org/monthly/2020/03/09/
```

## PDF 第36页

[查看原页](RAW.pdf#page=36)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
团队介绍
本文作者业空，来自淘天集团-营销&交易技术团队。本团队承担淘天电商全链路营销交易技术
攻坚，致力于通过技术创
新推动业务增长与用户体验升级
。过去一年主导了多个高价值项目，
包括：支撑618、双11、春晚等亿级流量洪峰、构建业界领先的全网价格力体系
面接入微信支付、搭建集团最大的Al创
新平台-ideaLAB，支撑淘宝秒杀等创
、承接淘宝全
新业务的高速增
长。
营销&交易技术是淘天集团核心技术团队，团队年轻充满活力，重视新人成长，技术氛围浓
厚，鼓励突破性思考与实
践。
期待你是：
﻿代码极客：编程能力强悍，痴迷代码与设计之美。
﻿Al 先锋：关注AIGC、大模型等技术趋势，用技术思维撕裂业务天花板，敢想敢造；
创
新行
动派：好奇心强，乐于接受挑战，用技术思维突破业务边界。
﻿
岗位范围：java后端、前端、
后训练、评测、agent 开
发、测
工作
、认真生活 🏖 。 简历可投递邮箱：chenglin.ycl@alibaba-inc.com。
开等，欢迎加入我们，一起快乐
¤ 拓展阅读 ¤
3DXR技术 | 终端技术 | 音视频技术
服务端技术 | 技术质量 | 数据算法
大淘宝技术
大淘宝技术官方账号
967篇原创内容
公众号
```

## PDF 第37页

[查看原页](RAW.pdf#page=37)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
阅读 1.0万
留言 3
写留言
宋蛋 北京 2025年11月19日
在AI时代看到一篇工程文章太不容易了
广告
13
懒懒 浙江 2025年11月20日
哇哦，厉害了👍
孙永贺 浙江 2025年11月19日
满满的干货
张雪教育
在职研究生：学费7980元，2年制免到校，学信网可查，国家认可
进入小程序
```
