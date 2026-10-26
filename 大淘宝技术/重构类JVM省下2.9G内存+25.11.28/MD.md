# 重构一个类，JVM竟省下2.9G内存？：PDF文本转写

> 这是原始PDF文本层转写，不是学习摘要。页码为PDF物理页序；图表、代码版面和图片文字不能完整表达在此文本层。已查看图像的内容和质量问题见AI学习笔记及META.json。

[原文PDF](RAW.pdf) · [AI学习笔记](AI_重构类JVM省下2.9G内存.md) · [处理与质量记录](META.json)

## PDF 第1页

[查看原页](RAW.pdf#page=1)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
重构一个类，JVM竟省下2.9G内存？
不琢 2025年11月28日 01:22 浙江
大淘宝技术 5人
本文 讲 述 了 作 者 通 过 重 构一个核心类 的数据 结 构， 将 原本 使用 HashSet<String>>
的 设 计 ， 优 化 为 基 于 HashMap<Long,
FastUtil 库
的 Long2ObjectOpenHashMap<int[]>，并利用标签为小整数且数量稀疏的业务特性，
改用排序后的
int[]
配合二分查找替代 HashSet。这一改动在生产环境中使 JVM 堆内存
占用从约 3.2GB 降
至 211MB，节省近 3GB 内存，降幅达
94% 以上。文章深
入分析了
原始结构的内存浪费原因，并通过实测
对比多种方
案，验证了新结构在内存效率和查询性
能上的优越性，强调
了在大数据量场景下应警惕“通用容器”的隐性成本。
优化效果
仅重构一个类，JVM 堆内存直降 2994MB（≈3GB）——从 3205MB 降
内存占用仅为老方
案的 6.5%。
这不是压测数据，也不是理论推演，而是生产环境双写验证的真实结果：
上线期间，新老结构并
行写入，内存指标实时对比；
验证无误后，正式切换至新结构，老结构彻底下线
。
至 211MB，新结构
如此巨大的收益，竟源于对
撼动近 3GB 的内存水位？”
单个核心类的数据结构重构。你或许会问：“一个类的改动，何以
```

## PDF 第2页

[查看原页](RAW.pdf#page=2)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
答案，藏在那些被我们习以为常的“通用容器”之中——HashMap、HashSet、自动装
象头开销……它们在小规模场景下优雅高效，却在海量数据面前悄然变成“内存吞噬者”。
本文将完整复盘此次优化的思考路径、技术选型、实测
对比与落地细节。
箱、
对
背景
在我们的核心业务链路中，存在一个对城市维度下某特定类型商品标签进
行
口。其过滤逻辑极为复杂：
支持多条件与/或 嵌套组合；
条件结构呈多层级
树状表
达式；
动态过滤的关键接
且部分规则涉及运
行
时上下文计算，无法静态预编译。
由于这类逻辑难以被搜
索引擎原生表
达，也无法通过简单
的字段匹配或脚
本高效实现，我们最
终选
择
将全量商品标签数据加载至内存，在应用层完成实时过滤计算。为此，我们设计了一个
以城市 ID为键、商品标签集合为值的内存数据结构，并辅以 3 分钟 TTL 的本地缓存 以支持
跨请求复用。
⚠ 值得注意的是：若无此缓存机制，每次请求
都将重建全量结构，内存瞬时峰值将远高于当
前水平。
正是在这一背景下，我们发现：看似合理的“通用集合嵌套”设计，在十万级商品 × 万级城市
× 多标签的规模下，竟成为内存消耗的“沉默杀手”。
先看下重构前的对象设计
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
publicclassRecallPlatformTagsRespextendsBasePageResponse<RecallPlatform
privatestaticfinallong serialVersionUID = 8030307250681300454L;
/**
* key:shid, 商品id
* value:platformTags Set结构，对应商品的标签集合
*/
privateMap<Long, Set<String>> resultMap;
}
resultMap样例
1
2
[
{1:["2246"
,
"2288"
,
"3388"
,
"1022"]},
```

## PDF 第3页

[查看原页](RAW.pdf#page=3)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
3
4
{2:["12246"
,
"12288"]}
]
从业务数据特征来看，所有标签 ID
均为 小于 5000 的正整数——这是一个典型的稠密小整数
域。
然而 ， 在原有模 型 中， 这些 标 签 却 被 表 示 为 String类 型 （ 如 "12345"） 。从 内存效 率角 度
看，这是一个显著的结构性浪费。
我们推测，当初的设计者可能是出于“未来扩展性”考虑（例如支持非数字标签），但在当前业
务场景下，这种通用性牺牲了巨大的内存效率。
而 正是这一设 计 ， 让 BasePageResponse<RecallPlatformTag>成 为内存中的“巨无 霸 ”
——单实例在高并发缓存下累计占用高达
3.13 GB 堆内存。
问题随之而来：“为何一个泛型响应类会吃掉 3GB 内存？”
接下来，我将逐层拆解这 3.13 GB 的构成，带你透视 JVM 堆中那些被忽视的对象开销、嵌套
容器
膨胀与装
箱陷阱——真相，往往藏在细节之中。
老结构内存分析
为了精准评估优化空间并指导新结构设计，我们基于百万级商品样本（约 100 万 itemId）对
标签分布进
了
行
深度统计。核心指标是：“拥有 k 个标签的商品数量”。结果如下（节选关键区
间）：
80% 的商品标签数 ≤ 16
90% 的商品标签数 ≤ 32
99% 的商品标签数 ≤ 64
最大标签数 < 128
这一分布具有两个关键特征：
高度右偏（长尾极短）：绝大
绝对上限明确：任
多数商品标签数量极少；
意商品的标签数均未超过 128。
这一数据洞察，成为我们后续结构选型的决定性依据：
既然标签数极少且有界，无需动态扩容的复杂集合（如 HashSet）；
既然数据只读且初始化后不变，排序
二分查找 成为高性价比
方
案；
+
既然标签本质是小整数，int[]可彻底替代 String
+
HashSet，消除对象开销。
换言之：不是我们选
了
择
int[]，而是数据分布告诉我们——它是最优解。
```

## PDF 第4页

[查看原页](RAW.pdf#page=4)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
接下来，我以100w个商品为例，以表格的形式
详细展现该对象所占内存情况。
```

## PDF 第5页

[查看原页](RAW.pdf#page=5)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
对内存敏感的同学，会注意注意到 标签字符串对象（未去重）和└─ 若字符串去重
两列。由
于标签个数有限，实际上可以使用string的常量池做优化(如何做常量池，最简单
的方法是使用
全局Map<String,String>)。未去重表示的是没有放常量池，老结构中并未放入常量池中。
新结构方
案选型
看 完上 述 的老 结 构的内存占用 分 析表 ， 相信不 少 同学会心
头一紧 ——一个看 似 普 通
的
HashMap<Long, HashSet<String>>，竟在海量数据下吞噬数 GB 堆内存。问题的根源
其实
非常清晰：HashMap
及其衍生结构（如 HashSet，底层同样是 HashMap）在大规模场
景下，是典型的“隐形内存黑洞”。
```

## PDF 第6页

[查看原页](RAW.pdf#page=6)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
这并非否定 HashMap
进入百万/千万级
的价值——它在通用性、易用性和平
均性能上无可替代。但当数据规模
、且对内存敏感时，我们必须重新审视：是否有更紧凑、更高效的数据结构？
幸运的是，Java 生态早已为我们准备了答案。
在方
案设计阶段，我脑海中迅速闪过多个候选方
案：
使用 FastUtil 的原始类型 Map（如 Long2ObjectOpenHashMap）；
将 HashSet<String> 替换为
int[]
二分查找；
+
采用
RoaringBitmap（若标签可映射为整数 ID）；
甚
至考虑自定义
紧凑对象池；
经过内存占用、查找性能、初始化开销、代码复杂度四维度实测，最终筛选出最优组合，并整
理成下表供参考：
```

## PDF 第7页

[查看原页](RAW.pdf#page=7)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
本次内存优化包含两个关键改动：
将 HashMap<Long, ?> 替换为 FastUtil 的
除 Long
装
箱开销及Map内部table 和Entry对象开销；
Long2ObjectOpenHashMap<?>，消
将 HashSet<String> 替换为排序后的
int[]，并用二分查找替代 contains()。
值得注意的是，第二项优化带来的收益更为显著：
仅将 value 改为
64MB；
int[]（仍用普通
HashMap）时，测试数据内存由老结构的1.3GB降
进一步采用 Long2ObjectOpenHashMap<int[]>
后，内存进一步压缩至 25MB。
这说明：数据结构的“双重优化”中，value 层的精简贡献了主要收益。
至
▐ 为何 int[] 可替代 HashSet？
原设计使用 HashSet 出于两点考虑：
去重：标签数据在初始化阶段已由上游保证唯一性，无需运
行
时去重；
高效查找（contains()）。
我们对比两
种方
案的查找时间复杂度：
```

## PDF 第8页

[查看原页](RAW.pdf#page=8)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
其中
k 为单个实体的标签数量。
虽然 HashSet 理论上平
均为 O(1)，但其最坏情况
Entry 节点、指针、哈希桶数组等）。
而
int[]
二分查找：
+
时间复杂度稳定在 O(log k)，无哈希冲突风险；
空间开销极低：仅需 4k 字节（k 个 int），无额外对象；
缓存友好：连续内存布局，CPU 预取效率高。
结合业务数据分布：
80% 的实体标签数 < 16 → 最多 4 次比
90% < 32 → 最多 5 次比
较；
最大标签数 < 128 → 最多 7 次比
较；
较；
不可控，且伴随显著内存开销（对象头
、
这意味着：90% 的查询在 5~6 次比
下降 94%
+
的巨大收益。
结 论 ： 在小 规模 （ k ≤ 128）、静 态、
是 HashSet
的高性价比
高确定性替代方
案。
细心的同学会看到表格中有个实测列，这里我特地准备了
出来，查看各方
案所占内存大小。
较内完成，实际延迟与 O(1) 几乎无感差异，却换来内存
有序 的数据 场 景下 ，紧 凑 数组 +
二 分 查找
、
测试case，并且用JProfiler dump
```

## PDF 第9页

[查看原页](RAW.pdf#page=9)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
同时附上测试代码，有兴趣的同学可以一试。
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
package com.taobao.trip.search.testMemery;
import it.unimi.dsi.fastutil.longs.Long2ObjectMap;
import it.unimi.dsi.fastutil.longs.Long2ObjectOpenHashMap;
import org.roaringbitmap.RoaringBitmap;
import java.util.*;
import java.util.concurrent.ThreadLocalRandom;
publicclassMemoryComparisonTest2 {
privatestaticfinalint COUNT = 1000
_
000; // 10万商品
privatestaticfinalint TAG
_
MIN = 1000;
privatestaticfinalint TAG
_
MAX = 10000;
privatestaticfinalint TOTAL
UNIQUE
_
_
TAGS = 3000; // 总标签数不超过300
// 所有可能的标签池（3000个）
privatestaticfinal List<Integer> ALL
_
TAGS = new ArrayList<>();
static {
Set<Integer> tagSet = new HashSet<>();
while (tagSet.size() < 3000) {
int tag = ThreadLocalRandom.current().nextInt(TAG
_
tagSet.add(tag);
MIN, TAG
}
ALL
_
TAGS.addAll(tagSet);
}
// 模拟标签数量：90% <=16，10% 17~100
privatestaticintrandomTagCount(){
```

## PDF 第10页

[查看原页](RAW.pdf#page=10)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
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
return ThreadLocalRandom.current().nextDouble() < 0.9
? ThreadLocalRandom.current().nextInt(1, 17)
: ThreadLocalRandom.current().nextInt(17, 101);
}
// 随机取 n 个标签
privatestatic List<Integer> randomTags(int count){
Collections.shuffle(ALL
_
TAGS);
return ALL
_
TAGS.subList(0, count);
}
publicstaticvoidmain(String[] args) throws InterruptedException {
System.out.println("开始生成 10万 酒店标签数据...
");
Dto dto = getDto();
System.out.println(dto.bitmapMap.size());
Thread.sleep(10 * 60 * 1000); // 10分钟，足够分析
System.out.println(dto.bitmapMap.size());
}
privatestatic Dto getDto(){
Map<Long, Set<String>> resultMap = new HashMap<>();
Map<Long, int[]> intArrayMap = new HashMap<>();
Long2ObjectOpenHashMap<int[]> fastutilIntArrayMap = new Long2O
Long2ObjectOpenHashMap<RoaringBitmap> bitmapMap = new Long2Obj
Map<Long, Set<String>> resultpoolMap = new HashMap<>();
Long2ObjectMap<BitSet> bitSetMap = new Long2ObjectOpenHashMap<
Dto dto = new Dto(resultMap, intArrayMap, fastutilIntArrayMap,
// ==================== 方
案1：Map<Long, Set<String>>（当前线上）
long t1 = System.currentTimeMillis();
for (long shid = HOTEL
_
COUNT; shid <= 2*HOTEL
_
COUNT; shid++) {
List<Integer> tags = randomTags(randomTagCount());
putResultMap(tags, resultMap, shid);
putPoolMap(tags, resultpoolMap, shid);
int[] arr = tags.stream().mapToInt(i -> i).toArray();
intArrayMap.put(shid, arr);
fastutilIntArrayMap.put(shid, arr);
putBitMap(tags, bitmapMap, shid);
putBitSet(tags, bitSetMap, shid);
}
System.out.println("resultMap.size " + resultMap.size());
System.out.println("resultpoolMap.size " + resultpoolMap.size
System.out.println("bitSetMap.size " + bitSetMap.size());
System.out.println("bitmapMap.size " + bitmapMap.size());
System.out.println("intArrayMap.size " + intArrayMap.size());
System.out.println("fastutilIntArrayMap.size " + fastutilIntA
// 保持对象存活，供 JProfiler 抓取内存
System.out.println("==========数据构建完成，等待 10 分钟，启动 JPro
return dto;
}
```

## PDF 第11页

[查看原页](RAW.pdf#page=11)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
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
99
100
privatestaticvoidputBitSet(List<Integer> tags, Long2ObjectMap<BitS
BitSet bs = new BitSet();
for (int tag : tags) {
bs.set(tag);
}
bitSetMap.put(shid, bs);
}
privatestaticvoidputBitMap(List<Integer> tags, Long2ObjectOpenHash
RoaringBitmap bitmap = new RoaringBitmap();
for (int tag : tags) {
bitmap.add(tag);
}
bitmapMap.put(shid, bitmap);
}
privatestaticvoidputPoolMap(List<Integer> tags, Map<Long, Set<Stri
Set<String> stringTags = new HashSet<>();
for (Integer tag : tags) {
stringTags.add((String.valueOf(tag)).intern());
}
resultpoolMap.put(shid, stringTags);
}
privatestaticvoidputResultMap(List<Integer> tags, Map<Long, Set<St
Set<String> stringTags = new HashSet<>();
for (Integer tag : tags) {
stringTags.add(String.valueOf(tag));
}
resultMap.put(shid, stringTags);
}
}
从测试结论可见，最合适的模型为Long2ObjectOpenHashMap<int[]>，最终模型优化为：
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
publicclassRecallPlatformTagsRespextendsBasePageResponse<RecallPlatform
privatestaticfinallong serialVersionUID = 8030307250681300454L;
/**
* 老结构保留，便于验证阶段双写比
* key:itemId,
* value:platformTags
*/
较效果
private Map<Long, Set<String>> resultMap;
/**
```

## PDF 第12页

[查看原页](RAW.pdf#page=12)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
12
13
14
15
16
17
18
19
* 新增结构
* key:itemId, long 对象非Long,省掉包装类的开销,
* value:platformTags 目前总2000多个，且增长缓慢，标签id为数字类型
*/
private Long2ObjectOpenHashMap<int[]> itemTags = new Long2ObjectOpe
}
终于到了讲 Long2ObjectOpenHashMap，如果这篇文章只能让你记住一件事，那我希望你
记住的就是Long2ObjectOpenHashMap。
Long2ObjectOpenHashMap详解
在本次模型优化中，我们引入了
库 FastUtil 的一个专用哈希映射
背景、成熟度及底层机制进
了评估。
行
Long2ObjectOpenHashMap —— 来自高性能 Java 集合
实现。为确保技术选型的可靠性与长
期可维护性，我们对其
可靠性与社区成熟度
项目历史悠久：FastUtil 自 2000 年代初启动，持续活跃维护至今，版本稳定，文档完
善。
广 泛工 业 验 证 ： 已被 多 个主 流 开 源 项目及 商 业系
统 深 度 集 成 ， 包 括 Apache Spark、
Elasticsearch、Neo4j、
Deeplearning4j 等，证明其在高并发、大数据场景下的稳定性
与性能表现。
轻量无依
赖
：FastUtil 为纯 Java 实现，无外部依
赖
，易于集成与升级
。
▐ 为什么选
择
Long2ObjectOpenHashMap
该类 是专为 long 类 型 键 → 对象 值 映 射 场 景设 计 的高 性能 Map 实 现 ， 相比 JDK 原
生 HashMap<Long, V>，具有以下优势：
避免装
箱开销：直接使用原始 long 类型作为键，无需 Long
对象封装，显著减少内存占
用与 GC 压力。
开放寻址（Open Addressing）：采用线性探测解决哈希冲突，缓存局部性更优，访问速
度更快。
内存紧凑：内部使用连续数组存储键值对，无链表或红黑树结构，空间效率更高。
接下来我讲详细介绍Long2ObjectOpenHashMap底层实现和原理。
```

## PDF 第13页

[查看原页](RAW.pdf#page=13)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
▐ 1.底层存储结构：数组 + 开放寻址
核心数据结构（简化版）
Long2ObjectOpenHashMap 内部使用
两个平
行数组 存储键值对：
1
2
long[] key; // 存放所有
的 long 键
Object[] value; // 存放对应的 Object 值
还
⚠ 注意：这不是链表数组，而是扁平数组，采用
开放寻址法（Open Addressing）
有一个关键变量：
mask：用于快速计算索引，mask = array.length - 1（当容量是 2 的幂时）；
哈希索引：index = (Hash(key)) & mask；
▐ 2.哈希函数与索引计算（避免误解）
虽然 long是 64 位，但不能直接用 key % capacity，因为：
%运算慢；
负数处理麻烦；
所以 fastutil 使用：
1
2
int hash = (int)(key ^ (key >>> 32)); // 混合高低32位
int index = hash & mask;
这是经典的
“哈希扰动
+
位与取模” 技巧，类似于
HashMap，但针对
long 优化。
▐ 3.
冲突产生的本质：哈希碰撞 + 存储空间有限
场景重现
假设容量为 8，mask = 7（二进制
我们插入以下键：
111）
👉 三个 key 都映射到
index=0，哈希冲突爆发！
```

## PDF 第14页

[查看原页](RAW.pdf#page=14)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
▐ 4.底层存储状态变化（冲突处理过程）
初始状态（容量=8）：
1
2
key: [0, 0, 0, 0, 0, 0, 0, 0]
value: [null, null, null, null, null, null, null, null]
Step 1: put(1000, "A")
index = 0
key[0] == 0（空）→ 可插入
插入后：
1
2
key: value: ["A"
[1000, 0, 0, 0, 0, 0, 0, 0]
, null, null, null, null, null, null, null]
Step 2: put(1008, "B")
index = 0
key[0] == 1000 ≠ 0
→
冲突！
线性探测：检查
index
+1 = 1
key[1] == 0
→ 空 → 插入
1
2
key: value: ["A"
[1000, 1008, 0, 0, 0, 0, 0, 0]
,
"B"
, null, null, null, null, null, null]
Step 3: put(2000, "C")
index = 0
key[0]=1000 ≠ 0 → 冲突
key[1]=1008 ≠ 0
→ 冲突
key[2]=0
→ 空 → 插入
1
2
key: [1000, 1008, 2000, 0, 0, 0, 0, 0]
value: ["A"
,
"B"
,
"C"
, null, null, null, null, null]
冲突通过向后查找空槽解决，这就是
线性探测（Linear Probing）
▐ 5.get() 操作如何应对冲突？（关键路径）
调用 get(2000L) 时：
```

## PDF 第15页

[查看原页](RAW.pdf#page=15)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
1 int index = (hash(2000)) & mask; // = 0
1.查 key[0] == 1000 ≠ 2000
2.查 key[1] == 1008 ≠ 2000
→ 不匹配，继续；
→ 继续；
3.查 key[2] == 2000
→ 匹配！返回 value[2] = "C"；
查找必须沿探测链一直走，直到找到 key 或遇到空槽为止。
关键规则：
空槽（key[i] == 0）表示“查找终止”，因为插入时不会跳过空槽，所以一旦遇到空，说明这
个 key 不存在。
▐ 6.删除操作的挑战（为什么不能直接置空？）
核心问题：为什么不能直接置空？
如果 remove(1000) 后直接设置 key[0] = 0L：
1 key: [0, 1008, 2000, 0, ...] // 错误！
调用 get(2000) 时：
起始索引 = 0；
key[0] == 0L → 立即终止查找；
结果：无法找到实际存在的 2000 ；
正确解决
方
案：后向位移（Backward Shift）
Long2ObjectOpenHashMap 使用非持久化墓碑标记加后向位移算法：
删除步骤详解
Step 1: 定位并临时标记
1
2
// 找到 key=1000 在位置0
key[0] = REMOVED
_
KEY; // 设置为 -1L（临时墓碑）
Step 2: 执
后向位移
行
从位置1开始，检查后续元素是否需要前移：
检查位置1 (key=1008)：
1008 的理论位置 = 0；
由于位置0现在是空洞，1008 可以前移到位置0；
执
位移：
行
1 key[0] = 1008; // 1008 前移到位置0key[1] = REMOVED
_
KEY; // 位置1临时标
检查位置2 (key=2000)：
```

## PDF 第16页

[查看原页](RAW.pdf#page=16)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
执
2000 的理论位置 = 0；
位置1现在是空洞，2000 可以前移到位置1；
位移：
行
1 key[1] = 2000; // 2000 前移到位置1key[2] = REMOVED
_
KEY; // 位置2临时标
检查位置3 (key=0L)：
遇到空槽，停
止位移；
清理最后一个墓碑：key[2] = EMPTY_KEY (0L)；
最终结果
1
2
key: value: ["B"
[1008, 2000, 0, 0, 0, 0, 0, 0]
,
"C"
, null, null, null, null, null, null]
▐ 7.
冲突带来的性能问题（实际影响）
⚠ 当负载因子 > 0.7 时，性能急剧下降。
▐ 8.如何缓解冲突？（优化策略）
1. 合理初始化容量
1
2
// 预估 10000 个元素，避免频繁扩容
Long2ObjectOpenHashMap<String> map = new Long2ObjectOpenHashMap<>(16384
2. 使用高质量哈希函数
fastutil 已优化，无需手动干预。
3. 避免连续 key 导致聚集
比
如 1000, 1008, 1016, ...
都是 8 的倍数 → 全
解决：增加随机性，或使用 ID 分布更均匀；
部 &7 == 0
→ 严重冲突；
```

## PDF 第17页

[查看原页](RAW.pdf#page=17)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
▐ 9.建议使用场景
✅ 适用：
高频 long -> Object 映射（如用户 ID → 用户对象）；
线程或外部同步的并发场景；
对 GC 和性能敏感的
系
统（避免 Long 装
箱）；
❌ 不适用：
并发写频繁（需自己加锁）；
key 分布极不均匀（如全为 8 的倍数）；
内存极度受限（开放寻址）
单
小结
本 次优 化 的 核心， 是 将 ： HashMap<Long, HashSet<String>> 重 构为 FastUtil 的
Long2ObjectOpenHashMap<int[]>， 内存占用 直降 94%
+
（ 从 3.13G 降
至 200M 量
级）。
这一实
践带来两点关键启
示：
警惕“隐形”内存黑洞：看似普通的集合嵌套，在海量数据下会指数级放大内存开销；
心中常怀资源成本：优秀
系
的
统设计，应以内存敏感为默认思维，而非依
堆机器
赖
掩盖低
效。
¤ 拓展阅读 ¤
3DXR技术 | 终端技术 | 音视频技术
服务端技术 | 技术质量 | 数据算法
大淘宝技术
大淘宝技术官方账号
967篇原创内容
公众号
```

## PDF 第18页

[查看原页](RAW.pdf#page=18)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
阅读 4059
```
