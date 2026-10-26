# 支配树算法原理及鸿蒙工具实践：PDF文本转写

> 这是原始PDF文本层转写，不是学习摘要。页码为PDF物理页序；图表、代码版面和图片文字不能完整表达在此文本层。已查看图像的内容和质量问题见AI学习笔记及META.json。

[原文PDF](RAW.pdf) · [AI学习笔记](AI_支配树算法与鸿蒙工具.md) · [处理与质量记录](META.json)

## PDF 第1页

[查看原页](RAW.pdf#page=1)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
支配树算法原理及鸿蒙工具实
践
原创
终端平台基础工程 2026年1月14日 03:11 浙江
大淘宝技术 3人
本文 介 绍 了支配 树 （D
ominator Tree） 算 法 在鸿 蒙系
统 ArkTS 内存分 析工 具中的应
用。为应对淘宝 App 鸿蒙版因内存溢出导致的 Crash 问题，作者构建了一套从客户端采
集内存快照
、服务端自动分析的工具链。文中对比了多种支配树构建算法（如朴素算法、
Lengauer-Tarjan 算 法 和迭 代 算 法 ） ， 并 说 明 选用 优 化 后 的迭 代 算 法 的原因 ： 实 现 简
便于验证、且适合存在大量循环引用的内存图结构。
单、
前言
随着淘宝App鸿蒙版UV⽇渐增⻓，ArkTS的内存溢出导致的Crash也在逐步上升，因此，团队
实现了⼀套从客户端采集内存镜像⾄服务端⾃动分析聚合⼯具。本⽂介绍该⼯具的核⼼原理：
内存对象的⽀配树算法
▐ ⽀配树是什么
在⼀个有向图中，存在⼀个⼊⼝节点 ，如果节点 ⽀配节点 ，当且仅当从 → 的所有
路径都经过节点 ，记 如果不存在 使得 且 ，则 是
的直接⽀配节点，记做 。从⼊⼝ 通过直接⽀配节点形成的树则称为⽀配树，即
⽀配树中每个节点的⽗节点都是其直接⽀配节点。
▐ ⽀配树作⽤
在分析内存泄漏或者内存溢出的时候，内存镜像
中的对象通常会很多(数量可达百万)。⾸要的
问题是如何找出占⽤内存较⼤
那些对象，对象占⽤内存可以分为两类：
1
class B {
2
int c;
3
}
```

## PDF 第2页

[查看原页](RAW.pdf#page=2)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
4
5
6
7
8
class A {
B b = new B();
}
A a = new A();
1. ，指的是对象本身的内存⼤⼩。上⽅代码中，a对象中有⼀个引⽤指针b，
为4bytes。b对象中有⼀个变量c， 为4bytes
2. ，指的是回收该对象之后虚拟机能够回收的内存⼤⼩。a对象的
为8，释放a之后可以同时释放b，所以
显然，只要将那些 占⽤较⾼的对象回收掉就可以解决内存溢出的问题。如果将对
象抽象为有向图中的节点，对象间的引⽤关系则可以抽象为有向图中的边，例如上⾯的代码，
a对象引⽤b对象，可以抽象为下图。
因此，内存镜像
中的对象集合可以抽象为以GC root为⼊⼝节点的
有向图，通过有向图构建出
对应的⽀配树。假设在⽀配树中 ，根据⽀配树的特性，回收 a 对象，
在内存中就成了孤⽴对象可以被GC，由此可以得出：
▐ ⽀配树算法种类
1. 朴素算法，原理是对每个节点 ，依次删除图中的其他节点，判断
是否存在路径从根节点
到达
节点 ，算法复杂度为 ，复杂度过⾼，⼀般不使⽤。
2. Lengauer-Tarjan算法，经典的⽀配树算法，⼀般情况是 优化后的算法复杂度
， α 是阿克曼函数，可以理解为趋近于线性 。
3. 迭代算法，通常是用于在编译
的控制流当中，算法复杂度是 ，优化后算法复杂度
。
器
实现鸿蒙ArkTS内存镜像分析⼯具使⽤的是迭代算法，主要有以下⼏个原因：
```

## PDF 第3页

[查看原页](RAW.pdf#page=3)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
1. Lengauer-Tarjan算法原理及其优化⽐
较复杂，⼯具类对于构建⽀配树的速度要求没有那
么⾼；
2. 可以使⽤华为已
3. 实现的profiiler插件以及chrome的开源代码作为对⽐，防⽌
在内存对象 的引⽤ 关 系中， 存在很多 循 环 引⽤ ， 节点 与节点 之 间 的环⽐
算法出错；
较 严重 ， 这让
Lengauer-Tarjan算法在计算半⽀配节点的时候算法复杂度⼤⼤增加。
Lengauer-Tarjan算法原理
介绍Lengauer-Tarjan算法的主要原因是⽹上对于该算法的介绍⼤部分证明过程都是论⽂翻译
⽐
较复杂，包括有时AI的解答也存在错误。
例如上⾯是⼀个AI关
⼤于x。
于半⽀配
者的定义
描述错误，正确的描述应当是所有
节点的DFS 编号都
▐ 基础知
识
下⾯是⼀张有序图通过DFS之后形成的节点和边的关系图，节点0-10是dfs遍历的顺序，下⾯
称为dfs序，边的类型可以分为4种：
1. 树边，即DFS过程中建⽴的边，在下图中显示为⿊⾊；
2. 前向边，即祖先节点到⼦树⾮⼉⼦的边，在下图中显示蓝⾊, 2->6，1->4，0->2；
3. 返祖边，即节点到祖先节点的
变，在下图中显示为橙⾊，4->2,3->2,6->2；
4. 横叉边，即从⾮⼦树、
⾮祖先横叉过来的边，在下图中显示为绿⾊，8->5,9->8。
```

## PDF 第4页

[查看原页](RAW.pdf#page=4)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
▐ 理解半⽀配节点
如何理解半⽀配节点是理解Lengauer-Tarjan算法关键点，以下是半⽀配节点 的定
义：
对于任
意节点 ，如果存在一个节点 ，且
节点可以不存在)的序号都
的半支配节点。
的路径中所有
节点 （
大于 ，则 是 的半支配候选，其中dfs序最小的 被称为
在基础知
识中介绍过4种边的类型，对于任
到达 最远祖先节点(⽐
意节点 的半⽀配节点可以理解为是通过这四
种边
当前节点dfs序⼩的节点只有可能是祖先节点或者左⼦树节点，dfs必
须遍历完左⼦树再遍历右⼦树，左⼦树节点不可能存在到右⼦树节点的边，只可能是祖先节
点)。由半⽀配节点的定义可得：
1. ⽗节点是半⽀配候选，例如: 3->5
2. 前向边的节点是半⽀配候选，例如: 2->6
3. 返祖边的节点是半⽀配候选，例如：1->4->2
4. 横叉边的节点是半⽀配
者选，例如: 1->7->8->5
换个说法，整个半⽀配候选的集合是 的直接⽀配
者，更进⼀步，从半⽀配候选增加⼀条边指向
不改变
的⽀配
关系，于是对于任
意节点 ，都可以简化为下⾯的连接
关系，其中
隐含的结论: 半⽀配候选都是在
的树边上
▐ 计算直接⽀配节点
```

## PDF 第5页

[查看原页](RAW.pdf#page=5)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
半⽀配节点 还不能直接⽀配节点，因为还不⽀配 的树边，例如上⾯的
dfs序为5的节点，它存在树边(3->5)和横叉边(1->7->8->5)，通过定义可以算出它的半⽀配
节点 。但实 际 上还 存在0->2->3->5这条 路 径不 经 过 1号 节点 ， 实 际 上
。
计算直接⽀配节点的⽅式，计算从半⽀配节点出发经过树边到达
的最⼩dfs序 。
节点所有中间节点 的
在论⽂中，这两个结论是通过反
证法来进
证明，⽐
⾏
证明，不
保证完全正确，如有错误，请以论⽂为准。
较难理解，这⾥尝试通过⾃然语⾔来进
⾏
1. ⽐
较 好推 导 ， 说 明不 存在有
的祖 先 节点不 通 过
到达 ，⼜由于半⽀配集合都是处于 的树边上，所以到达
半⽀配
集合都得通过 ，故
2. 说明⾄少存在⼀个节点不通过 可以到达
节
点 ，其中 ，可以证明 不⽀配 ，可以⼤致得
到下图的节点关系，最主要问题是为何不需要考虑其他 的情况，例
如： 。可 以假 设 ， 则存在不 经 过
到达 ，但是该条路径必须经过 的半⽀配候选集，根据前⾯半⽀配节点隐含
的结论， 的半⽀配候选集都在 的树边上，且 ，
由 于 存 在 树 边 到 达 ， 这 与 的 定义 相 悖 ， 故
。
```

## PDF 第6页

[查看原页](RAW.pdf#page=6)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
Lengauer-Tarjan算法实现代码可以参考 Andro
id perfllib（cs.andro
id.com/andro
id-
studi
o/platform/tools/base/
+
/mirror-goog-studi
o-
main:perflib/src/main/java/com/andro
id/tools/perflib/heap/analysis/LinkEvalD
minators.kt）
o
迭代算法
▐ 算法原理
迭代算法的原理利⽤了⽀配节点存在传递性，即 ⽀配节点 当且仅当⽀配其前驱
节点
，简要⽤公式表
达:
迭代算法过程如下
1. 初始化根节点 s , Dom(s) = {s}
2. 初始化其他节点 n ， Dom(n) = {全集}
3. 对于⾮根节点 n ， Dom(n) = n ∪ (∩Dom(p)) ，即当前节点 n 并上所有前驱
⽀配节点的交集
4. 重复步骤3，直到所有
的 Dom(n) 不再变化
节点 p的
▐ JS内存镜像分析
```

## PDF 第7页

[查看原页](RAW.pdf#page=7)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
js内存镜像
实际上是⼀个json⽂件，分为以下⼏个部分
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
{"snapshot":
{"meta":
{"node
fields":
_
["type"
,
"name"
,
"id"
,
"self
size"
_
,
"edge
count"
_
ss"
,
"native
_
size"],
"node
_
types":
[["hidden"
,
"array"
,
"string"
,
"object"
,
"code"
,
"closure"
,
"native"
,
"synthetic"
,
"concatenated
string"
,
"slicedstring"
,
"symbol"
,
"bigint"],
"string"
,
mber"
,
"number"
,
"number"],
"edge
_
fields":["type"
,
"name
or
index"
,
"to
_
_
_
node"],
"edge
_
types":
[["context"
,
"element"
,
"property"
,
"internal"
,
"hidden"
,
"string_
or
_
number"
,
"node"],
"trace
function
info
_
_
_
fields":[...],
"trace
node
_
_
fields":[...],
"sample
_
fields":[...],
"location
fields":[...]
_
},
"node
_
count":100056,
"edge
_
count":384773,
"trace
function
count":0
_
_
},
"nodes":[...],
"edges":[...],
"trace
function
_
_
infos":[],
"trace
_
tree":[],
"samples":[],
"strings":[...],
}
,
"trace
node
id"
_
_
,
"detached
"regexp"
,
"number
"number"
,
"number"
"
,
"shortcut"
,
"weak"
"locations":[],
meta: 定义了节点和边的结构
node_fiields: 定义了
单个内存节点(node)的属性
node_types:内存节点(node)的类型
edge_fiields:定义了
edge_types: 定义了边的类型
单个边(edge)的属性
node_count: 节点数量
edge_count: 边的数量
nodes: 节点的集合
edges: 边的集合
strings:所有
的字符串，包括边的名称，内存节点的名称等等
```

## PDF 第8页

[查看原页](RAW.pdf#page=8)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
内存节点node
在nodes中，每⼀
代表⼀个节点，其中
⾏
⾏
中的每个数字由node_fiields来描述，例如：
1
2
3
4
5
6
7
8
"node
fields":
_
["type"
,
"name"
,
"id"
,
"self
size"
_
,
"edge
count"
,
"trace
node
id"
,
"detachedn
_
_
_
ss"
,
"native
_
size"],
"nodes":[9,11693,1,0,6386,0,0,0
,8,11696,3,48,1,0,0,0
,8,11696,5,48,1,0,0,0
,...]
以第⼀
⾏ 9,11693,1,0,6386,0,0,0
为例，解析后是这样
1
2
3
4
5
type: 9, //节点类型的偏移
name: 11693, //节点名字，大概率是文件名，对应strings中的index
id: 1, //无特殊含义，节点的标号
self
edge
_
size: 0, //大概率是shallow
_
size，0大概率是数组
_
count: 6386, //跟其他内存节点的引用关系
nodes_type存储了节点的14种类型，这个例⼦中，节点的类型是synthetic，不过这种类型似
乎是虚拟机内部类型，不
展示
1
2
3
4
5
"node
_
types":
[["hidden"
,
"array"
,
"string"
,
"object"
,
"code"
,
"closure"
,
"regexp"
,
"number"
"native"
,
"synthetic"
,
"concatenated
string"
,
"slicedstring"
,
"symbol"
,
"bigint"],
"string"
,
"number"
,
"number"
,
"n
mber"
,
"number"
,
"number"],
strings存储 了 所有
SyntheticRoot。
的字符 串 ， 包 括了 节点 名 字， 在这个例⼦ 中name转 为字符 串 是
引⽤关系
edge
edges中存储 了 内存节点 的引⽤ 关 系， 每⼀
⾏
edge_fiields进
表示
1
2
3
4
5
⾏
"edge
_
fields":["type"
,
"name
or
index"
_
_
"edges":[5,11673,527080
,5,11673,527072
,5,11673,527056
代表 ⼀条 边 ，
⾏
中的每⼀个数字通 过
,
"to
_
node"],
```

## PDF 第9页

[查看原页](RAW.pdf#page=9)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
6 ,...]
type存储的边的类型，也是节点之间引⽤关系
是⼀个shotcut
的类型，例如：第⼀
⾏
的例⼦代表这条边的类型
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
"edge
_
types":
[["context"
,
"element"
,
"property"
,
"internal"
"string_
or
number"
_
,
context //暂时没有用处
"node"],
element //DOMTree中的元素
property //类当中的属性
internal //内部属性
hidden //隐藏属性
shortcut //和property中差不
多，通过赋值得到的引用
weak //弱引用
,
"hidden"
,
"shortcut"
,
"weak"]
name or__index存储 的是strings中的名 字index， 11673对应 的是-subroot-字符 串
to_node代表的是这条边指向的节点索引，因为内存引用构成是一个有向图，所以还需要知道
这条边来自于哪个节点。边属于哪个节点的计算是通过内存节点索引
+边来进
计算的，举个
行
例子：如果一个节点的序号是0，有10条边，那么edges[0,10)就是属于节点0的，如果序号1
的节点有
5条边，那么edges[10,15)就是属于节点1的。
▐ 构建边的索引
内存节点的属性edge_count，代表该节点持有
的边的数量，由此可以算出每个节点持有
索引范围[fiirstEdgeIndexes[nodeOrdinal], fiirstEdgeIndexes[nodeOrdinal
+1])
边的
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
private void buildEdgeIndexes() {
firstEdgeIndexes[nodeCount] = edges.length;
int nodeOrdinal = 0;
for (int edgeIndex = 0; nodeOrdinal < nodeCount; ++nodeOrdinal) {
firstEdgeIndexes[nodeOrdinal] = edgeIndex;
//nodes[nodeOrdinal * nodeFieldCount + nodeEdgeCountOffset]当前
edgeIndex += nodes[nodeOrdinal * nodeFieldCount + nodeEdgeCount
}
}
▐ 构建前驱
节点
```

## PDF 第10页

[查看原页](RAW.pdf#page=10)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
构建前驱
节点的算法⽐
较巧妙
1. 遍 历 所有
的边 ， 找 到 边 的toNode， 然 后 计 算 toNode的前驱
在 firstRetainerIndex
中，和firstEdgeIndexes类型，每个节点的前驱
来了，就是
[fiirstRetainerIndex[nodeOrdinal],fiirstRetainerIndex[nodeOrdinal
+1])
节点 (retainer)的数量存储
节点的范围也计算出
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
int edgeLength = edges.length;
for (int edgeToNodeIndex = edgeToNodeOffset; edgeToNodeIndex < edgeLeng
int toNodeIndex = edges[edgeToNodeIndex];
if (toNodeIndex % nodeFieldCount != 0) {
TBPLogger.error("Invalid toNodeIndex is {}"
, new Object[] {toNo
} else {
int toNodeOrdinal = toNodeIndex / nodeFieldCount;
if (isValid(toNodeOrdinal, firstRetainerIndex.length)) {
firstRetainerIndex[toNodeOrdinal]++;
}
}
}
2. 遍历所有
的节点，然后为前驱
节点预留好位置，retainingNodes是前驱
节点的集合
1
2
3
4
5
6
7
8
9
int firstUnusedRetainerSlot = 0;
for (int nodeOrdinal = 0; nodeOrdinal < nodeCount; ++nodeOrdinal) {
int retainerCount = firstRetainerIndex[nodeOrdinal];
firstRetainerIndex[nodeOrdinal] = firstUnusedRetainerSlot;
if (isValid(firstUnusedRetainerSlot, edgeCount)) {
retainingNodes[firstUnusedRetainerSlot] = retainerCount;
firstUnusedRetainerSlot += retainerCount;
}
}
3. 遍历所有
的节点，再根据节点持有
的边找到toNode，那么该节点就是toNode的前驱
节点
1
2
3
4
5
6
7
for (srcNodeOrdinal = 0; srcNodeOrdinal < nodeCount; ++srcNodeOrdinal)
firstEdgeIndex = nextNodeFirstEdgeIndex;
nextNodeFirstEdgeIndex = firstEdgeIndexes[srcNodeOrdinal + 1];
srcNodeIndex = srcNodeOrdinal * nodeFieldCount;
for (int edgeIndex = firstEdgeIndex; edgeIndex < nextNodeFirstEdge
int index = edgeIndex + edgeToNodeOffset;
```

## PDF 第11页

[查看原页](RAW.pdf#page=11)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
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
if (isValid(index, edges.length)) {
int toNodeIndex = edges[index];
if (toNodeIndex % nodeFieldCount != 0) {
TBPLogger.error("Invalid toNodeIndex is {}.
"
, new Obje
} else if (isValid(toNodeIndex / nodeFieldCount, firstReta
//retainningNodes的起点
int firstRetainerSlotIndex = firstRetainerIndex[toNode
//由后向前添加，直到retainingNodes[firstRetainerSlotIndex
int nextUnusedRetainerSlotIndex = firstRetainerSlotInd
if (isValid(nextUnusedRetainerSlotIndex, retainingNode
retainingNodes[nextUnusedRetainerSlotIndex] = srcN
retainingEdges[nextUnusedRetainerSlotIndex] = edge
}
}
}
}
}
▐ 计算节点distance
计算节点就是使⽤bfs进
遍历
⾏
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
private void calculateDistances() {
for (int nodeOrdinal = 0; nodeOrdinal < nodeCount; nodeOrdinal++)
nodeDistances[nodeOrdinal] = noDistance;
}
int[] nodesToVisit = new int[nodeCount];
int nodesToVisitLength = 0;
//遍历根节点
for (int edgeIndex = firstEdgeIndexes[rootNodeIndexInternal];
edgeIndex < firstEdgeIndexes[rootNodeIndexInternal + 1];edgeI
int childNodeIndex = edges[edgeIndex + edgeToNodeOffset];
int childNodeOrdinal = childNodeIndex / nodeFieldCount;
if (isUserRoot(childNodeIndex)) {
nodeDistances[childNodeOrdinal] = 1;
bfsNodes[bfsIndex++] = childNodeOrdinal;
nodesToVisit[nodesToVisitLength++] = childNodeIndex;
}
}
//从根节点进
遍历
行
bfs(nodesToVisit, nodesToVisitLength, nodeDistances);
nodeDistances[rootNodeIndexInternal / nodeFieldCount] =nodesToVisi
nodesToVisit[0] = rootNodeIndexInternal;
```

## PDF 第12页

[查看原页](RAW.pdf#page=12)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
22
23
24
25
nodesToVisitLength = 1;
//遍历其他
单独的节点，synthetic节点
bfs(nodesToVisit, nodesToVisitLength, nodeDistances);
}
▐ 构建⽀配树
chrome的开
发
者 ⼯ 具 和鸿 蒙 IDE的profiiler插 件 使 ⽤ 的都是优 化 过 的迭 代 算 法 ， 参 考 论 ⽂
《A Simple, Fast D
ominance Algorithm》，有两个重要的优化点：
1. 计算节点的D
om顺序不是采⽤先序遍历，⽽是采⽤逆后序进
⾏
遍历加速收敛。从基础知
识
那
⾥可以得知dfs树有四
种边，其中前向边和树边，先序遍历和逆后序遍历都是⼀次遍历就
可以计算，对于返祖边，都是需要多次遍历才能计算，但对于横叉边，逆后序只需要⼀次
遍历⽽先序遍历就要多次。
2. 在计算 D
om(p) 的交集的朴素算法是对所有前驱
节点的⽀配节点⼀⼀查找匹配，这样的效率
很低很低，甚
⾄可以到达 O(n2) 。论⽂中提出了⼀个新的⽅
案，由于前驱
节点的dom树已经
构建完成，例如下图dom(7) = {7,1,0}, dom(6) = {6,2,1,0}， dom(3) ={3,2,1,0}，此时求
dom(5)，通过观察很容易发现dom(5)={5,1,0}。根据树的特点，求解idom(n)就转换为求
解n的前驱
节点在⽀配树上的公共祖先节点。
这⾥给出论⽂中的伪代码⽅便理解。具体实现代码可以参考chrome的代码HeapSnapshot.ts
（ github.com/ChromeDevTools/devtools-
frontend/blob/chromium/6194/front_end/entrypo
ints/heap_snapshot_worker/Hea
pSnapshot.ts）
```

## PDF 第13页

[查看原页](RAW.pdf#page=13)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
计算⽀配节点的核⼼就在intersect⽅法中，找当前节点的dom和前驱
先，优化后的迭代算法可以降
低到 ，m是遍历次数logn是⽀配树的
步，如果m是⼀个常量的话，⼀般算法复杂度可以做到 。
节点之间的最近公共祖
深度，更进⼀
▐ 计算retainSize
retainSize就是如果通过GC释放这个内存节点，能释放的内存⼤⼩。计算⽀配树的⽬的就是
确定节点的retainSize =
当前节点的shallowSize(⾃身⼤⼩) +
⽀配节点的retainSize。
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
void calculateRetainedSizes(int[] postOrderIndex2NodeOrdinal) {
int postOrderIndex;
for (postOrderIndex = 0; postOrderIndex < nodeCount;++postOrderInd
retainedSizes[postOrderIndex] = nodes[postOrderIndex *nodeField
if (nodeNativeSizeOffset != 0) {
retainedNativeSizes[postOrderIndex] = (long)nodes[postOrde
}
}
//后序遍历，让被支配节点先于支配节点计算retainSize
for (postOrderIndex = 0; postOrderIndex < nodeCount - 1;++postOrder
int nodeOrdinal = postOrderIndex2NodeOrdinal[postOrderIndex];
int dominatorOrdinal = 0;
if (isValid(nodeOrdinal, dominatorsTree.length)) {
dominatorOrdinal = dominatorsTree[nodeOrdinal];
}
if (isValid(dominatorOrdinal, retainedSizes.length) &&isValid(
retainedSizes[dominatorOrdinal] +=retainedSizes[nodeOrdina
if (nodeNativeSizeOffset != 0) {
retainedNativeSizes[dominatorOrdinal] +=retainedNative
}
}
}
```

## PDF 第14页

[查看原页](RAW.pdf#page=14)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
24
25 }
▐ 聚合计算
虽然最难的部分⽀配树已经计算完成，但还需要将引⽤链聚合起来，⽅便⼈⼯分析和上报到平
台进
⾃动化分析。
⾏
具体流程如下：
节点，拿到所有
1. 先遍历所有
类型的retainSize和个数，然后进
节点的stringIndex，根据stringIndex进
⾏
⾏
过滤掉⼀些泄漏不
多的对象类型，得到⼤
聚合，可以得到对象
对象类型。
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
public Map<Integer, ConstructorNode> getBigHeapNode() {
Map<Integer, ConstructorNode> heapNodes = new HashMap<>(nodeCount)
for (int nodeOrdinal = 0; nodeOrdinal < nodeCount; nodeOrdinal++)
int nodeIndex = nodeOrdinal * nodeFieldCount;
if (isHidden(nodeIndex)) {
continue;
}
}
if (isSynthetic(nodeIndex)) {
continue;
int stringIndex = nodes[nodeIndex + nodeNameOffset];
if (heapNodes.containsKey(stringIndex)) {
ConstructorNode heapNode = heapNodes.get(stringIndex);
heapNode.addRetainedSize(1, retainedSizes[nodeOrdinal]);
} else {
String constructorName = strings.get(stringIndex);
if (HarmonyAnalyzeUtils.containsTaobao(constructorName)) {
ConstructorNode heapNode = new ConstructorNode(stringI
heapNodes.put(stringIndex, heapNode);
}
}
}
ConfigParams configParams = CmdArgs.getInstance().getConfigParams(
Map<Integer, ConstructorNode> bigNodes = new HashMap<>();
for (ConstructorNode heapNode : heapNodes.values()) {
if (heapNode.getRetainedSize() >= configParams.minRetainedSize
bigNodes.put(heapNode.getStringIndex(), heapNode);
}
}
return bigNodes;
```

## PDF 第15页

[查看原页](RAW.pdf#page=15)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
32 }
2. 重新通过bfs的顺序遍历节点，如果是⼤
对象类型就进
回溯，找到到根节点的路径并记录
⾏
下来，最后进
根据引⽤路径进
⾏
⾏
聚合成aggregatedRefTree。
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
36
37
38
39
private void aggregateReferenceTree() {
Map<Integer, ConstructorNode> bigNodes = getTBHeapNode();
//对节点进
bfs
行
for (int i = 0; i < bfsIndex; i++) {
int nodeOrdinal = bfsNodes[i];
int nodeIndex = nodeOrdinal * nodeFieldCount;
int stringIndex = nodes[nodeIndex + nodeNameOffset];
if (bigNodes.containsKey(stringIndex)) {
Map<String, List<ConstructorNode>> referenceTrees = new Ha
calculateReferenceTree(nodeOrdinal, new StringBuilder(), n
for (String key : referenceTrees.keySet()) {
List<ConstructorNode> refChain = referenceTrees.get(ke
if (aggregatedRefTree.containsKey(key)) {
ConstructorNode cached = aggregatedRefTree.get(key
//相同节点的链路不用相加
if (cached == refChain.get(0)) {
continue;
}
cached.addCount();
cached.addRetainedSize(retainedSizes[nodeOrdinal])
cached.addShallowSize(nodes[nodeIndex + nodeSelfSi
} else {
if (!refChain.isEmpty()) {
aggregatedRefTree.put(key, refChain);
}
}
}
}
}
}
private void calculateReferenceTree(int nodeOrdinal, StringBuilder pat
Map<String, List<ConstructorNo
int nodeIndex = nodeOrdinal * nodeFieldCount;
int stringIndex = nodes[nodeIndex + nodeNameOffset];
pathKey.append(stringIndex).append('
-
');
ConstructorNode node = new ConstructorNode(stringIndex, strings.ge
refChain.add(node);
if (nodeDistances[nodeOrdinal] == 1) {
String key = pathKey.toString();
```

## PDF 第16页

[查看原页](RAW.pdf#page=16)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
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
List<ConstructorNode> newRefChain = new ArrayList<>(refChain);
referenceTree.put(key, newRefChain);
return;
}
List<Integer> retainers = findRetainers(nodeOrdinal);
for (Integer retainer : retainers) {
StringBuilder newPathKey = new StringBuilder(pathKey);
List<ConstructorNode> newRefChain = new ArrayList<>(refChain);
calculateReferenceTree(retainer, newPathKey, newRefChain, refe
}
}
总结
⽀配树算法属于是内存泄漏/溢出分析的核⼼算法，我们基于此算法实现鸿蒙ArkTS内存镜像分
析⼯具，希望本⽂对
⼤家实现类似功能的⼯具有⼀定帮助。
参考⽂档
《A Simple, Fast D
ominance Algorithm》：
https://www.cs.tufts.edu/~nr/cs257/archive/keith-cooper/dom14.pdf
《A New, Simpler Linear-Time D
ominators Algorithm》：
http://adambuchsbaum.com/papers/dom-toplas.pdf
《A Fast Algorithm for Finding D
ominators in a Flowgraph》：
https://faculty.cc.gatech.edu/~harrold/6340/cs6340_fall2009/Readings/lenga
uer91jul.pdf
团队介绍
本文作者灵貎，来自淘天集团-终端平台基础工程团队，团队负责淘宝App基础架构和基础链
路业务，致力于通过技术创
新和系
统优化，打造一个更稳定、更流畅的手机淘宝。同时我们也
在持续探索通过AI搭建高效、智能的研发体系，提升团队的研发效能。
```

## PDF 第17页

[查看原页](RAW.pdf#page=17)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
¤ 拓展阅读 ¤
3DXR技术 | 终端技术 | 音视频技术
服务端技术 | 技术质量 | 数据算法
大淘宝技术
大淘宝技术官方账号
967篇原创内容
公众号
阅读 1634
留言
写留言
还没有
留言，来写首评
```
