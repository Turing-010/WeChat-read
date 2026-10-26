# 原文逐页转写

文本来自本次 PDF 文本层；不补写图片、截断内容或代码。图片和布局请打开每页 PDF 链接核对。AI 解释另见学习笔记。

## PDF 第 1 页

[原页](RAW.pdf#page=1)

````text
这⼤概是我读过最硬核的⼀次 Linux  内核重构⽂章了
2026 年 4 ⽉ 12 ⽇ 02 : 51⼴东腾讯技术⼯程 47 ⼈
作者： TencentOS
背景
Linux 内核的  Swap ⼦系统⾃诞⽣以来，数⼗年间代码复杂度持续累积，逐渐成为内存管理⼦系
统中公认的复杂地带。然⽽，来⾃腾讯的内核⼯程师  Kairui Song 以⼀系列系统性的重构⽅案，
彻底扭转这⼀局⾯。
⾃ 2025 年  Linux 存储、⽂件系统、内存管理与 BPF 峰会上⾸次亮相以来，腾讯服务器操作系统
TencentOS 内核研发⼯程师  KairuiSong 主导的 Swap 现代化⼯程，历经了多个阶段的演进：
swap table 的引⼊（已合并进  Linux 6.18 ）从根本上替代了沿⽤多年的  XArray 结构，带来
5%~20% 的性能提升； swap map 的移除（⾯向  Linux 7.1 ）进⼀步统⼀了  Swap 元数据管理，
节省约  30% 的元数据内存开销；⽽将整个  Swap ⼦系统重新构建于更为清晰、⾼效的数据结构
之上的宏⼤⽬标，正逐步从设想变为现实。
这项持续了 18 个⽉的⼯作在  Linux 内核社区引发了⼴泛关注。 LWN.net 知名作者、 Linux 内核⽂
档核⼼维护者  Jonathan Corbet 专门撰写了连续三篇深度分析⽂章（ "Modernizing swapping"
系列），逐篇解析  Kairui 及其协作者（ Chris Li 等）所做⼯作的技术细节与及其深远影响 —— 这在
LWN 的报道传统中，是对⼀项内核贡献极⾼规格的认可。
本⽂对  Corbet 的三篇⽂章进⾏了系统翻译与整理，以期将这项重要的内核技术进展完整呈现。
（原⽂链接详见⽂末附录）
⼀、引⼊ swap table
内核的  Swap ⼦系统是⼀个复杂且常被忽视的庞然⼤物，但它也是内存管理⼦系统的关键组成部
分，对整个系统的性能有重⼤影响。在  2025 年的 LSF/MM/BPF （ Linux 存储、⽂件系统、内存
管理和  BPF ）峰会上， Kairui Song 提出了⼀个简化并优化内核交换代码的⽅案 ¹ 。该⼯作的第⼀
部分 ² （由  Chris Li 协助）成功进⼊ 6.18 版本内核，开启了整个  Swap ⼦系统现代化的序章。
1.1 虚拟内存与匿名页换出
````

## PDF 第 2 页

[原页](RAW.pdf#page=2)

````text
在虚拟内存系统中，内存不⾜时必须通过页⾯回收来应对，在必要时需要将内存内容写⼊持久化
后备存储。对于⽂件页⾯来说（也就是  page cache ），⽂件本⾝即为后备存储。但匿名页
（ anonymous pages ） —— 也就是⽤于存放进程的堆、栈及各类数据结构的数据区，天然不存在
这样的后备存储。这正是  Swap ⼦系统存在的意义：当匿名页所占⽤的物理内存需要被回收时，
Swap ⼦系统为其提供写出⽬标。换出（ swapping out ）将不活跃（或访问频率低）的页⾯推送
到持久化存储介质，从⽽释放内存，腾出空间当前活跃使⽤的⼯作负载。
1.2 Swap ⼦系统快速⼊门
然⽽完整地描述内核的  Swap ⼦系统确实会很冗长；其中有着巨量的随着时间逐渐积累起来的复
杂问题。以下是  Linux 内核  Swap ⼦系统在  6.17 版本下的简述。
Swap ⼦系统⽀持使⽤⼀个或多个  swap ⽂件，可以是存储设备上的独⽴分区，也可以是⽂件系
统内的普通⽂件。内核中，可⽤的  swap ⽂件由  struct swap_info_struct³ 描述，通常以简单整数
索引来引⽤（内核中每个 swap_info_struct 拥有⼀个独⽴的  type 作为标识符 —— 其实这也是个历
史遗留问题，这⾥的  type 更应该叫作 id 或 index ）。每个  swap ⽂件内部被划分为页⾯⼤⼩的槽
（ page-sized slots ），所有  Swap ⽂件上的任意槽位都可以使⽤  swp_entry_t⁴ 类型来索引到。
这个  long val 被分为两个字段：⾼六位是  swap ⽂件的索引号（也就是上⽂提到的 type ），其余部
分是⽂件内的槽位编号（在  swap ⽂件内部的偏移量）。内核提供了⼀组简单的函数 ⁵ ⽤于创建
swap entry 并获取相关信息。
需要注意，上述为架构⽆关的通⽤格式。各体系结构还有其架构相关的变体，⽤于避免与页表项
（ PTE ）格式产⽣冲突。好奇的读者可参阅x86_64 宏 ⁶，两种形式之间可以进⾏转换。在  Swap
⼦系统内部，统⼀使⽤架构⽆关版本。
1.2.1 换出流程简述
当内存管理⼦系统决定回收⼀个匿名页时，它就会选择⼀个  swap 槽位，将该页内容写⼊该槽
位，然后将对应的  swap entry （以架构相关格式）存⼊页表项（ PTE ）。 swap entry 存储在 PTE
中时，其格式是不包含 PTE 所定义的 "present" 位的，因此下次访问该页时将触发缺页异常
（ page fault ）。内核识别到  swap entry 后，分配新的物理页，从  swap ⽂件读取内容，并相应
更新  PTE 。
现实中的流程远⽐上述复杂。例如，将页⾯写⼊  swap ⽂件需要时间，在写完之前该页⽆法被真
正回收。因此，回收决策做出时，该页⾸先被置⼊  swap cache （与⽂件映射页使⽤的  page
cache ⾼度类似）。页⾯位于  swap cache ，也就意味着已为其分配了⼀个  swap entry 。该页本
⾝仍驻留于内存的这段时间便会与该  swap entry 成为绑定关系，⽤于处理各种同步和反向查询等
操作。例如若写⼊过程中发⽣缺页异常，该页可被迅速重新激活（ reactivated ）。内核在等待页
⾯完成回写后，才可以真正将其释放。同时也有类似于 ZRAM 这样的快速设备，其上的回写极其
迅速因此这⾥的等待操作会更简洁。
1
2
3
typedef struct {
    unsigned long val;
} swp_entry_t;
````

## PDF 第 3 页

[原页](RAW.pdf#page=3)

````text
1.2.2 address_space 与  XArray
如同内核⽂件系统需要维护  page cache 中每个页⾯的状态， swap ⼦系统在处理分配  swap 槽
位和 IO 以外，也需要追踪  swap cache 中每个页⾯的状态。在  6.18 之前的内核中， swap ⼦系统
维护了⼀个名为swapper_spaces⁷ 的结构，复⽤⽂件系统常见的address_space⁸ 结构从⽽维护
了 Swap 地址空间（此处⽂件的内部偏移和 swap ⽂件的槽位偏移⾮常接近），从⽽直接维持了
swap 后备存储与页⾯之间的映射关系，并提供⼀组在  RAM 与后备存储间移动页⾯的操作集。
这⾥复⽤的好处之⼀，就是使很多  page cache 相关代码也能直接作⽤于  swap cache 。
因此长期以来， swap cache 与  page cache 共⽤  XArray 数据结构作为其核⼼数据结构。 XArray
可以存储每个槽位的当前状态，每个槽位状态可以是：
● 空， Xarrayentry 为 NULL
●槽位已分配，且页⾯仍驻留于  RAM ： XArray entry 为指向该页（更准确地说，是包含该页的
folio ）的指针
●槽位已分配，但页⾯已释放，数据只存在于 Swap ⽂件中。在这种情况下， Xarray entry 包含 “ 影
⼦ ” 信息，供内存管理系统⽤于检测换出后快速错误进⼊的页⾯。（有关此机制的概述，请参阅这
篇2012 年的⽂章 ⁹）
此外，每个 swap ⽂件并⾮只有⼀个  address_space 结构和XArray¹⁰ 。相反， swap ⽂件会被划分
为  64MB 的块，从⽽将数据分散到多个  XArray 上，减少 Xarray 锁竞争提升⼤型系统的可扩展
性。
1.2.3 Swap Cluster
Swap ⼦系统还引⼊了另⼀层管理机制：每个  swap ⽂件内部被划分为若⼲  swap cluster （由
struct swap_cluster_info¹¹描述，通常⼤⼩为  2MB ）。 swap cluster 使  swap ⽂件的管理具有更
好的可扩展性：系统中每个  CPU 维护⼀个本地 cluster ，相关  swap entry 可完全在  CPU 本地管
理，只有在  cluster 级别的分配或释放时才需跨  CPU 访问。更早时 Swap ⼦系统还会给每个 CPU
分配⼀个更细粒度的槽位缓存，这⼀设计已经随着 swap cluster 的进⼀步优化和简化⽽移除。
Swap cluster 减少了对全局  swap map 的扫描，但对特定槽位状态的读写仍需访问对应的
XArray 。
1.3 The Swap Table
有了上述背景，便可深⼊理解  6.18 的改动。
注意到， Swap ⼦系统处理  swap entry 时就已经能得知其所属的 swap cluster 。若将所有状态信
息（包括 Swap cache ）随  cluster ⼀并存储，便可消除  XArray ，代之以使⽤更简单和⾼性能的 C
数组。将整个 Swap cache 的管理局部化，简化，从⽽提升可扩展性。
因此， SwapTable 第⼀阶段补丁集增强了  swap_cluster_info 结构；6.17 之后的版本结构¹²新增
了⼀个数组指针：
1atomic_long_t __rcu *table;
````

## PDF 第 4 页

[原页](RAW.pdf#page=4)

````text
新的 table  数组被设计为在多数体系结构上恰好占⽤⼀个物理页，并采⽤动态分配，只有⼀个
cluster 被真正使⽤时才会分配，以此在  swap ⽂件未满时可减少  swap ⼦系统的内存占⽤。数组
中的每个条⽬均为⼀个 swap table entry ，其直接描述  swap ⽂件中某个槽位的状态。 Swap 代码
进⾏了⼤量重构以使⽤这⼀全新的核⼼数据结构。⼤多数内核内部  API 只需极少甚⾄⽆需改动便
可兼容。
如此以来，内核此前所采⽤两套独⽴的聚簇机制（   address_space 和 swap cluster ），现在统⼀为
单⼀聚簇⽅案，进⼀步降低了锁争抢的同时，简化了代码和设计。原本每  64MB ⼀个的
  address_space    结构体数组也已移除， XArray 不再需要， swap 地址空间操作可由单⼀结构体
swap_space¹³ 的单⼀结构提供。
根据  Kairui 的测评，第⼀阶段⼯作就可以 “在基准测试和⼯作负载测试中，吞吐量、 RPS 或构建
时间性能提升⾼达约  5-20%”。这⼀性能提升主要源于消除  XArray 查找，以及通过在更⼩粒度
上管理  swap 空间所带来的竞争减少。
⼆、删除 Swap Map
Swap map 是当前持续推进的  swap 改进⼯作的第⼆个核⼼⽬标。乍⼀看，当前内核中的  swap
map 是⾮常轻量和简单的数组，存储在  struct swap_info_struct 中：
该数组中， Swap 设备中的每个槽位对应⼀个字节。每个字节存储的值是指向该槽位的引⽤数
量。不论分配给该槽位的页⾯是否驻留在  RAM 中，每⼀个指向该槽位的页表项（ PTE ）都会贡
献⼀个引⽤计数。
当然， swap 系统错综复杂，情况⾃然不会那么简单 ——Swap map ⾥每个 entry 都预留⼀些特殊
bit 。其中对本⽂最重要的是第  6 位（ 0x40 ），称为  SWAP_HAS_CACHE ，⽤于表⽰某个槽位所
1unsigned char *swap_map;  /* vmalloc'ed array of usage counts */
````

## PDF 第 5 页

[原页](RAW.pdf#page=5)

````text
对应的页⾯是否还在内存⾥。在某些时间窗⼝内， swap slot 可能已被分配，但尚未有页表项引
⽤它，此时引⽤计数为零。 SWAP_HAS_CACHE bit ⽤于区分这种状态与  slot 未被分配的状态。
这个标志还被⽤作位锁（ bit lock ）同步。内核常常需要并⾏地多次尝试换⼊同⼀页⾯（或进⾏操
作）。在这种情况下，竞争线程会以 SWAP_HAS_CACHE bit 作为同步信号，成功设置这⼀ bit 的
线程才能进⾏⼯作。这引发了不少问题： Swap 代码中有⼤量延迟重试循环（例如¹⁴）或其他
work around 。
Swap map 中还有⼀些其他特殊值；例如  0x3f ： SWAP_MAP_BAD ，表⽰底层存储槽不可⽤。更
特殊的是 0x3e ： SWAP_MAP_MAX 表⽰引⽤计数超过了 swap map 可承载范围。 Swap map 使⽤
byte 作为基础单位，因此只能⽀持最⼤为  62 的引⽤计数。这带来了⼀个问题：当⼤量任务共享
⼀个匿名页⾯时，引⽤计数很容易超过这个值。处理这种情况的⽅式则更是⾮常繁琐。
每次  swap slot 的引⽤计数递增时，都必须检查是否溢出。发⽣⼀溢出时，另⼀个预留标记位
0x80 （ COUNT_CONTINUED ）将被置位。 Swap map 中的计数将被清零，并分配⼀个新的物理
页，为引⽤计数提供更⾼的  8 位。该新页通过关联  page 结构中的  LRU 链表头链接到原 swap
map 页。如果溢出页中的条⽬再次发⽣溢出，就继续分配⼀个页⾯追加到链表中。
考虑低位仍旧保留在 swap map 中，⼤部分引⽤计数操作不需要⾛到额外页⾯⾥，这样的设计尚
可接受。当引⽤计数较低时（这也是常见情况），这种设计提供了最⼩的内存开销和不错的性
能。
2.1 Swap cache bypass 与  SWAP_HAS_CACHE
正如我们提到的， swap cache 的⽤途之⼀是持有追踪槽位与页⾯之间的关系，这在换⼊换出 IO
过程中相当重要。如果对⼀个已换出的  folio 发⽣了缺页中断，就需要分配⼀个新  folio 并从
swap ⽂件中读取其内容。读操作往往需要⼀定时间，因此该  folio 会被加⼊  swap cache ，直⾄
读取完成才会从中移除，竞争的进程看到该页⾯便可直接复⽤和避免忙等待或重复 IO 。通常，
swap ⼦系统还会尝试预读（ readahead ），预读页⾯同样缓存于 swap cache 。
这⼀情况在  2018 年的  4.15 版本中有所改变： Swap ⽂件的 IO 有时⾮常迅速，特别是对于 ZRAM
这样的内存压缩⽅案。在这类设备上， swap cache 的额外开销和预读等⾏为⾮但不能提升性
能，反⽽可能有害。
因此在  4.15 版本中， Minchan Kim 加⼊了 Swap bypass 特性。如果 Swap 设备设置了
SWP_SYNCHRONOUS_IO 标志（表⽰设备速度极快， I/O 应同步执⾏），且  swap map 中特定
slot 的引⽤计数为  1 ，那么换⼊该  slot 中页⾯的请求将同步执⾏，不进⾏预读，且不加⼊  swap
cache 。这给  swap ⼦系统⼜增加了相当多的复杂性，多年来引发了各种  bug ，但也带来了显著
的性能提升。这种提升来⾃两个因素：避免了相对昂贵的 swap cache 操作开销，以及阻⽌了预
读的使⽤。
⽽在 7.0 内核中， Kairui Song 的 swap table 第⼆阶段补丁系列的第⼀部则致⼒于完全移除这⼀
bypass 特性。 Kairui Song 第⼀阶段的⼯作 —— 也就是 swap table 的引⼊，让 swap cache 操作速
度⼤幅提升，以⾄于对于即使像 ZRAM 这样的设备，绕过  swap cache 也不再有实质价值。该系
列后续⼜将  read ahead 的控制独⽴出来，并对快速设备基本上完全禁⽤了预读。让所有 swap
I/O 都通过  swap cache ，不仅简化了代码，更减少了令⼈头疼的竞态条件。
````

## PDF 第 6 页

[原页](RAW.pdf#page=6)

````text
新代码对于  SWP_SYNCHRONOUS_IO 设备，会在换⼊完成后⽴即将  folio 从  swap cache 中移
除，以此释放  swap 数据所占⽤的内存，但完整使⽤ swap cache 作为同步原语，避免忙等待和
优先级反转等问题。
移除  swap bypass 还带来⼀个有趣的副作⽤：在当前内核中，⾼阶 folio （ THP/mTHP ）只能通
过  bypass 路径换⼊，所以也只有在引⽤计数为  1 时才能完整换⼊。移除  bypass 特性后，⽆论
引⽤计数为何值，都可以换⼊完整的 folio 。
这也更进⼀步简化了 swap 的操作原语， swap 的所有管理和操作都被整合进⼀组定义明确的⼩函
数中。这些函数全部基于  folio 和 swap cache ，从⽽减少了  swap ⼦系统历史上以 swap entry 为
中⼼的设计。借助这⼀设计，外加上使⽤ cluster lock 与  folio lock 的组合来管理  swap cache ，
只需再迈⼀步，就可以⽤这两把锁来控制  swap map 的访问了。
⼀旦  swap cache 承担起管理并发的职责，   SWAP_HAS_CACHE bit 就只剩最后⼀个⽤途：标
记已分配但引⽤计数为零的  swap slot 。在换出侧，通过在  slot 分配后⽴即将  folio 加⼊  swap
cache ，消除了这种状态的存在。在另⼀端，当页⾯从  swap cache 中移除时，引⽤计数为零的
swap slot 会被⽴即释放。⾄此， SWAP_HAS_CACHE 不再有存在的必要；系列末尾的这个补丁
将其彻底移除。
2.2 移除 swap map
上述⼯作截⾄本⽂撰写时已进⼊  7.0 版本主线。后续可能在 7.1 之后的版本中，我们会完成  swap
table 的第三阶段，彻底消灭  swap map 。
在新的 swap table 中，每个 entry 是⼀个 64 位（或 32 位，取决于架构） unsigned long 。⽬前为⽌
其中的内容与之前内核  XArray 数据结构中存储的⾼度相同 ——NULL （ 0 ）表⽰空  slot ；对于驻
留  folio ，条⽬存储  folio 地址；对于已换出  folio ，条⽬存储⽤于追踪哪些页⾯能被快速从  swap
换回的  shadow 信息。第三阶段改变了这张表的条⽬格式，以⽀持五种不同类型的条⽬：
●NULL （ 0 ）：仍表⽰空  slot 。
●低⼀位置  1 ：这是⼀个已换出  folio 的  shadow entry ，条⽬⾼位存储该条⽬的引⽤计数。可⽤于
引⽤计数的  bit 数量因架构⽽异。
●低两位置 10   ：该条⽬对应⼀个驻留内存的  folio 。与  shadow entry 类似，最⾼位存储引⽤计
数；为了给引⽤计数腾出空间，存储的是底层页⾯的 ** 页帧号（ PFN ） ** ⽽⾮其地址。
●低三位置 100   ： pointer entry ，当前系列中未使⽤。
●低四位置 1000   ：标记为坏  slot ，不应使⽤。
这种设计将  swap map 最后剩余的职责 —— 追踪引⽤计数 —— 挤进了  swap table ，从⽽使  swap
map 得以彻底移除。长期以来内核⼀直将  swap map 和  swap cache 作为两个独⽴的数据结构分
开维护。这⾥将这两者统⼀，显著减少了记录维护的开销，从整体上加快了  swap 系统的速度，
以及相当可观的内存节省。 Swap ⼦系统约  30% 的元数据开销得以消除，对于  1TB 的  swap ⽂
件来说，可节省约  256MB 内存。
````

## PDF 第 7 页

[原页](RAW.pdf#page=7)

````text
新格式仍旧只是⽤了有限数量的 bit 来引对⼤部分⼯作负载，⽽在处理⼤量共享内存的⼯作负载中
可能出现的溢出上，也更加直观。如果引⽤计数溢出，将为整个  cluster 分配⼀个单独的
unsigned long 计数数组。
第三阶段⽬前已经进⼊了 mm-unstable 等待合并到主线，但⼯作也还没有结束： Kairui 提到了后
续阶段，将把  memory controller （内存控制器）对  swap 的限额管理也整合进  swap table 。因
此，和内核的其他部分⼀样， swap ⼦系统恐怕在很长时间内都会被认为尚未 " 完⼯ " 的状态。
三、  Swap Table 的完善与虚拟 Swap Table
Swap 的故事并不仅限于此。在完成了整个系统现代化重整后，⼤量原本难以实现的特性现在也
变得可⾏。在过去多年的讨论中，虚拟  Swap 这⼀概念被⼴泛提及。近期 Meta 以及 TencentOS 团
队都分别提出了各⾃的解决⽅案，来引⼊虚拟  Swap 空间这⼀概念。
其中 Meta 的⽅案 ¹⁵ 是引⼊⼀个单⼀且必选的中间层作为虚拟  swap 空间（ virtual swap space ），
解决了⼀系列与  swap 相关的问题。同时，腾讯的 TencentOS 团队也提出了全新的  Virtual
GhostSwap ⽅案¹⁶，其结合了 Google 的 GhostSwap ⽅案以及众多社区需求，以更优雅，更灵活
的⽅式实现虚拟  Swap 空间。
3.1 背景与动机
对于虚拟 Swap 的需求和性能平衡问题， Kairui 始终认为虚拟层应该是可选的，⽽不是强制的，
且性能与内存开销不能造成显著问题。在⽬前已有的  Swap 重构的基础上，借助  Swap Table 机
制， Swap table 第四阶段的⽬标，正是从根本上解决上述问题。
3.2 进⼀步系统性重构：统⼀分配路径
这⼀阶段的核⼼⼯作并⾮针对某⼀具体  bug 的修补，⽽是对整个  anon/shmem swap 分配流程
的全⾯重构。此前，匿名页和共享内存的换出路径在  swap cache 操作、 slot 分配与  memcg 计
费上均存在各⾃的逻辑分⽀，代码复杂且同步原语分散。本阶段将两条路径统⼀为基于  folio 的
规范流程： swap cache 层负责确保  folio 对  swap slot 的独占所有权后再⾏计费，从根本上消除
了压⼒场景下因竞态引发的内存抖动（ thrashing ），以及偶发的    VM_FAULT_OOM    泄漏问题。
````

## PDF 第 8 页

[原页](RAW.pdf#page=8)

````text
3.3 移除  swap cgroup 静态数组
在此次重构中，   mm/swap_cgroup.c  —— ⼀个独⽴维护  swap slot 与  cgroup 映射关系的静态数
组模块 —— 被完整移除（共  172 ⾏代码）。其功能被直接整合进  swap table ，由后者统⼀承担
memcg 信息的存储与检索职责。
这带来了显著的内存节省：以挂载⼀块  1TB 的  swap 设备为例，这⼀改动可节省约  512MB 的内
存。
3.4 开创性⼯作： Dynamic Ghost Swapﬁle
第四阶段还附带了⼀组  RFC 性质的补丁，引⼊了  Dynamic Ghost Swapﬁle 的概念 —— 这是
swap ⼦系统在架构层⾯的⼀次前瞻性探索，以动态的⽅式引⼊虚拟 Swap 。
其核⼼思路是：利⽤  Xarray 构建动态⼤⼩的虚拟  swap ⽂件，使  swap 空间的边界不再受制于预
先分配的静态结构。单次    swapon /dev/ghostswap    即可获得近乎  PB 级虚拟  swap 空间，且对
现有⽤户零影响。相⽐⼀个强制的中间层，动态虚拟 swap 在性能和可扩展性上都有显著优势。
当然，社区在技术⽅案上的分歧解决通常都不会太顺风顺⽔，这可能也会是⼀项长期的⼯作。
3.5 社区协作与影响
本阶段⼯作也由 Kairui Song 主导，并得到  Google 的  Chris Li 在  Ghost Swapﬁle ⽅向上的重要
协作贡献。补丁发出后社区有着⼤量的讨论和 Review ，该 RFC 后续应该会继续在社区中迭代完
善。
四、虚拟  swap 空间 —— 两种⽅案的碰撞
⽬前两种不同的虚拟  Swap 实现⽅案仍在社区推进中。其中基于  SwapTable 的⽅案需要进⼀步
的基础设施改造才能有望进⼀步推进。同时  Virtual Swapspace ⽅案的推进也在持续进⾏。在
Virtual Swapspace ⽅案中， Pham 也明确阐述了改⽅案想要解决的问题和设计思路。
4.1 Swap entries 的痛点
正如我们提到的， swap entry ⽤于标识  swap 设备上可⽤于存放⼀页数据的槽位（ slot ），包含设
备索引和设备内的偏移量。当⼀个匿名页被换出到  swap 设备时，对应的  swap entry 将被写⼊
所有指向该页的页表项（ PTE ）。借助该  entry ，内核可在需要将页⾯重新  fault in 到  RAM 时，迅
速定位已换出的页⾯。
这⾥的问题是，每个 swap entry 直接存⼊ PTE ，这导致 PTE 和 swap 设备变成了绑定关系，这给系
统管理员和系统设计者带来了⼀定的⿇烦。
问题⼀： swap oﬀ 设备代价⾼昂
Swap oﬀ 会尝试移除⼀个  swap 设备：在设备移除之前，存储于其上的所有数据页必须先被
fault in 回  RAM ，这⼀步⽆可避免。但还存在额外的问题 —— 我们必须确保所有的 PTE 都不再指
````

## PDF 第 9 页

[原页](RAW.pdf#page=9)

````text
向这⼀设备。为解决这⼀问题，内核必须在移除时扫描系统中全部匿名页的页表项，并将其更新
为页⾯的新位置。这⼀过程相当耗时。
问题⼆： zswap 的困境
这种设计也给zswap ⼦系统¹⁷的⽤户带来⿇烦。 zswap 的⼯作原理是：在换出流程中拦截页⾯，
不将其写⼊磁盘，⽽是将其压缩后存回内存。这也就导致， zswap ⽆法在没有真实物理设备时使
⽤，且 zswap 可压缩内存的量完全限制于物理块设备的⼤⼩：页⾯⾸次进⼊  zswap 时，必须⽴即
在后备设备上预分配⼀个槽位。这意味着，即使从不打算真正将页⾯写⼊磁盘，每次  zswap 使
⽤都必须在后备设备上占⽤空间，造成⼤量存储空间浪费，甚⾄使  zswap 在没有可⽤后备存储
的系统上⽆法使⽤。
4.2 虚拟 swap 空间
Meta 的 Pham 提出的解决⽅案，正如计算机领域的常见的做法：增加⼀层中间层。具体⽽⾔，就
是⽤⼀张独⽴于底层设备的统⼀空间⽤来分配 swap entry ，此时所分配的 swap entry 是⼀个
  swp_desc    结构体数组：
第⼀个  union 告知系统已换出页⾯的位置：要么指向设备特定的  swap 槽位，要么指向  zswap
cache 中的⼀个  entry ，即虚拟  swap 槽位与真实位置之间的映射。
第⼆个  union 包含页⾯在  RAM 中的位置（更准确地说是其  folio ），或内存管理⼦系统⽤于跟踪
页⾯  fault-in 速度的  shadow 信息。
 swap_count    字段记录有多少个页表项引⽤了此  swap 槽位；   in_swapcache    在页⾯被分配⾄该
槽位时置位；   memcgid    记录管理此次分配的控制组（ cgroup ）。
 type    字段指⽰当前  swap 槽位所代表的映射类型：
⦁   VSWAP_SWAPFILE  ：虚拟槽位映射到  swap 设备上的物理槽位（由    slot    字段标识）
⦁   VSWAP_ZERO  ：代表⼀个全零页⾯，⽆需写⼊任何地⽅
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
struct swp_desc {
    union {
        swp_slot_t         slot;
        struct zswap_entry * zswap_entry;
    };
    union {
        struct folio *     swap_cache;
        void *             shadow;
    };
    unsigned int               swap_count;
    unsigned short             memcgid:16;
    bool                       in_swapcache:1;
    enum swap_type             type:2;
};
````

## PDF 第 10 页

[原页](RAW.pdf#page=10)

````text
⦁   VSWAP_ZSWAP  ：指向  zswap ⼦系统中的⼀个槽位（由    zswap_entry    指向）
⦁   VSWAP_FOLIO  ：对应⼀个当前仍驻留于  RAM 的页⾯（由    swap_cache    指⽰）
4.2.1 设计优势
这⼀设计的主要好处在于：页⾯可以轻松地在不同  swap 设备之间迁移。例如，⼀个  zswap 页
⾯被推送到存储设备时，只需修改   swp_desc    结构体中的两个字段即可；该存储设备上的槽位
⽆需在决策之前提前分配，如果某页⾯始终未被推出，就完全不需要在存储设备上占⽤任何空
间。移除  swap 设备时，也⽆需扫描页表，因为虚拟  swap 槽位号保持不变。
4.2.2 代价与争议
当然，这⼀设计也有其代价：内存占⽤增加数倍、复杂度上升。 swap table 中每个  swap entry
占⽤  64 位（ 8 字节），⽽    swp_desc    结构体将其扩⼤⾄最多四倍（ 32 字节）。 Pham 指出，新增
的内存开销应该⽐表⾯看起来要⼩，因为该结构体整合了当前内核中分散存储在其他地⽅的信
息。尽管如此，对于⼀个以释放内存为⼰任的⼦系统⽽⾔，这仍然是相当显著的内存消耗增加。
此外，该代码在多项基准测试中出现了性能回退，尽管相较之前的版本已有较⼤改善。
⽬前，尽管这项⼯作有着可见的价值，但能否达到合并标准尚不明朗。在前⼏篇⽂章中承担了⼤
量  swap 相关⼯作的  Kairui Song 也表达了对内存开销以及系统在⾼负载下性能的担忧¹⁸，以及这
⾥实质上破坏了 swap oﬀ 的语义。 Chris Li 也同样担忧开销问题¹⁹，并指出该设计过于注重改进
zswap ，⽽忽略了其他⽅⾯。
4.2.3 swap 层级（ swap tiers ）
除了上述⼯作外，来⾃  Youngjun Park 的swap tiers patch set²⁰ 也提供了全新的想法。该系列允
许将多个  swap 设备配置为分层（ tier ）结构：⾼性能设备归⼊⼀个  tier ，较慢的设备归⼊另⼀个
tier 。并提供了 cgroup 钩⼦，允许管理员控制特定进程组可使⽤的  tier ，从⽽为延迟敏感（或⾼
优先级）的⼯作负载提供对快速  swap 设备的独占访问。
Park 的设想中，分层 swap 应该成为基础设施通⽤机制。页⾯应该能在不同  tier 之间的迁移，冷
数据可被逐步推向更慢的存储介质。因此，假设两组补丁都能持续推进，未来两者以某种⽅式合
并并不令⼈意外。
五、后续展望
除了对  Swap ⼦系统的深耕和推进以外， TencentOS 团队对整个内存管理领域的探索也在继续深
⼊。今年三⽉份， Kairui Song 为  Linux 内核⼜提交了⼀组补丁，在社区推动了⼀系列讨论，为
沉寂了⼀段时间的的  MGLRU 特性带来了众多进展。
此次补丁共⼋个，聚焦于  MGLRU 页⾯回收循环与脏页处理逻辑的优化。对于⽂件页⾯较多和涉
及回写的⼯作负载，在测试中可有有约  30% 的性能提升，在  HDD 等慢速设备上部分⼯作负载
提升幅度甚⾄超过  100% 。⽣产环境  OOM 问题也明显减少，代码复杂度也随之降低。
````

## PDF 第 11 页

[原页](RAW.pdf#page=11)

````text
值得⼀提的是，部分问题正是  Kairui Song 所在团队于腾讯⽣产环境中发现并着⼿解决的，体现
了⼤规模真实场景对内核优化的重要驱动价值。同时这⼀系列补丁也是后续对整个内存  LRU 进
⾏系统性优化的铺垫。⽬前相关补丁已提交⾄  Linux 内核邮件列表，等待社区审阅合⼊。也期待
有着更精彩的后续社区发展。
注释：
1. https://lwn.net/Articles/1016136/
2. https://lwn.net/ml/all/20250916160100.31545-1-ryncsn@gmail.com/
3. https://elixir.bootlin.com/linux/v6.17.13/source/include/linux/swap.h#L294
4. https://elixir.bootlin.com/linux/v6.17.13/source/include/linux/mm_types.h#L285
5. https://elixir.bootlin.com/linux/v6.17.13/source/include/linux/swapops.h#L83
6. https://elixir.bootlin.com/linux/v6.18.6/source/arch/x86/include/asm/pgtable_64.#L183
7. https://elixir.bootlin.com/linux/v6.17.13/source/mm/swap_state.c#L39
8. https://elixir.bootlin.com/linux/v6.17.13/source/include/linux/fs.h#L485
9. https://lwn.net/Articles/495543/
10. https://docs.kernel.org/core-api/xarray.html
11. https://elixir.bootlin.com/linux/v6.17.13/source/include/linux/swap.h#L238
12. https://elixir.bootlin.com/linux/v6.19-rc5/source/mm/swap.h#L21
13. https://elixir.bootlin.com/linux/v6.19-rc5/source/mm/swap.h#L201
14. https://elixir.bootlin.com/linux/v6.19-rc5/source/mm/swap_state.c#L465
15. https://lore.kernel.org/linux-mm/20260320192735.748051-1-nphamcs@gmail.com/
16. https://lore.kernel.org/linux-mm/20260220-swap-table-p4-v1-0-
104795d19815@tencent.com/
17. https://docs.kernel.org/admin-guide/mm/zswap.html
18. https://lore.kernel.org/all/CAMgjq7AQNGK-a=AOgvn4-
V+zGO21QMbMTVbrYSW_R2oDSLoC+A@mail.gmail.com/
19. https://lore.kernel.org/all/CACePvbVvzh8PcF47hz+MfFu3tta5vh3oD+WpGxEL_-
NrzYZG3Q@mail.gmail.com/
````

## PDF 第 12 页

[原页](RAW.pdf#page=12)

````text
阅读 1 . 0 万
20. https://lwn.net/ml/all/20260217000950.4015880-1-youngjun.park@lge.com/
附录：
1. Modernizing swapping: introducing the swap table
[LWN.net]https://lwn.net/Articles/1056405/
2. Modernizing swapping: the end of the swap map [LWN.net]https://lwn.net/Articles/1057102/
3. Modernizing swapping: virtual swap spaces [LWN.net]https://lwn.net/Articles/1059201/
4. https://lore.kernel.org/linux-mm/20260220-swap-table-p4-v1-0-
104795d19815@tencent.com
留⾔
写留⾔
````

## PDF 第 13 页

[原页](RAW.pdf#page=13)

````text
还没有留⾔，来写⾸评
````

