# 原文逐页转写

文本来自本次 PDF 文本层；不补写图片、截断内容或代码。图片和布局请打开每页 PDF 链接核对。AI 解释另见学习笔记。

## PDF 第 1 页

[原页](RAW.pdf#page=1)

````text
DeepSeek  Harness  拆解：⼀套能拼装的 Agent  架构
腾讯程序员 2026 年 8 ⽉ 14 ⽇ 02 : 20⼴东原创 腾讯技术⼯程 1086 ⼈
作者：chino ，腾讯 WXG 微信⼩店前端开发⼯程师
DeepSeek 发布了第⼀款  Agent 产品，DeepSeek Harness。这次的重点放在了运⾏时架
构上，官⽅给的关键词是 "everything is a plugin" ，模型接⼊、⼯具执⾏、会话记录、循环
本身、界⾯，全部⾛插件机制。
这篇⽂章跳过  agent 领域已经成为共识的那部分 —— 检测⼯具调⽤、执⾏、回填、循环，这
套流程眼下⼏乎每个框架都⻓⼀个样，不值得再讲⼀遍。重点放在  DeepSeek Harness 真
正跟别⼈不⼀样的⼏处设计：Cordis 这套插件运⾏时具体怎么管⽣命周期， preset 的
scope 继承链为什么拆成两层， Code Mode 为什么选了⼀个听起来不太 " 安全 " 的隔离⽅
案，⼯具注册的遮蔽算法怎么写。顺带会跟  Codex 的⼏个具体⼯程决策做对⽐，只挑不⼀
样的地⽅讲。
⼀、为什么是  Cordis
"everything is a plugin" 的基础是  Shigma 的开源项⽬  Cordis 。定位是 "Meta-
Framework for Modern JavaScript Applications" ，⼀个通⽤的插件框架，处理依赖注
⼊、作⽤域服务、⽣命周期清理这⼏件事，与  agent 、与  LLM 都没有直接关系，在
DeepSeek Harness 出现之前就已经存在。
Cordis 在开源社区有实际的使⽤者。最典型的是  Koishi，⼀个跨平台聊天机器⼈框架
（ QQ / Discord / Telegram / 微信都接）。聊天机器⼈场景天然是 " ⼏⼗个插件拼在⼀起、
热插拔、随时改配置 " ，与  agent 的场景⼏乎相同，只是没有  LLM 。DeepSeek Harness 把
整个框架的源码  vendor 进⾃⼰的仓库，改了个  scope 叫  @deepseek-ai/cordis，然后
````

## PDF 第 2 页

[原页](RAW.pdf#page=2)

````text
把公司⾃⼰写的每⼀个包，都设成对它的  peer dependency 。这⽐ " 使⽤⼀个第三⽅库 " 更
进⼀步：整个产品都构建在  cordis 之上。
先对⽐⼏种常⻅的插件形态：传统  DI 容器、轻量钩⼦⽅案、 Cordis 。这三种⽅案各有取
舍，值得摆在⼀起看。
传统  DI 容器的三个缺⼝。 " 主流 " ⽅案是⼀个  DI 容器加⽣命周期注解。你  bind 了⼀个
service ，谁来负责  unbind 和  cleanup ？传统  DI 要么不管（泄漏），要么要求你⼿写
lifecycle hook 。 LLM provider 热替换了，依赖它的  ToolRegistry 应该⾃动重启，传统  DI
做不到这种 " 依赖驱动的重载 " 。配置上，传统  DI 的配置在启动时读⼀次；
⽽  cordis.yml  ⾥⼀⾏就是⼀个插件实例，改配置直接触发  HMR 。
Pi 也是 Agent 界的明星产品了，但Pi 的  Extension ⾛的是另⼀条路。 Pi 的⾃我定位是  "self
extensible coding agent" ，它的插件叫  Extension （扩展），基于  TS ，在扩展点上通过钩
⼦塞逻辑：没有依赖注⼊，没有插件间依赖管理（加载顺序即优先级），也不能卸载。
Cordis 的插件是带依赖声明、⽣命周期、可逆副作⽤的 " 组件 " ：有依赖注⼊，有反应性
coeffects ，插件间可以声明依赖，卸载时能完整逆转副作⽤。
这最后⼀点 ——" 可逆副作⽤ "—— 是整篇⽂章的地基。 Cordis 的设计论⽂把这件事上升到理
论层⾯，核⼼问题问得很直接：
进程和容器的好处在于： kill 掉再启动，状态就清空了。代价是重启会丢掉进程内的
cache 、 connection 、 partial computation 。插件系统希望不⽤重启，也能完成同样的清
理。论⽂为此给了两个定义：
时间可组合性
：卸载组件时，组件对共享环境所做的修改必须被完整、安全地逆转 ⸺ 这要求追踪组件执⾏
的每⼀次资源分配、事件注册和状态变更。
空间可组合性
：依赖变化时，相关组件⾃动激活或停⽤。
时间可组合性是这篇⽂章的主线。剩下的事情 ——Fiber 、 effect 、系统边界、 preset 、 Code
Mode—— 都在回答同⼀个问题：怎么在⼯程上实现 " 卸载  = 完整逆转 " 。
Cordis ⽣态还带了⼏个配套包，随项⽬⼀起  vendor 进来：⼀个配置⽂件加载器（负责解
析  cordis.yml  这类声明式配置），⼀个  include 插件（负责把⼀份配置当成⼦树挂载进
来， preset 机制⽤的就是它改名后的版本），⼀个  HMR 模块（⽀持插件热替换），外加⽇
志和定时器这两个基础设施插件。这⼏块拼起来，才能真正理解 "everything is a plugin" 。
⼆、Fiber 与  effect ：可逆副作⽤的地基
Cordis ⾥，插件的类型定义是⼀个联合类型：
有没有⼀种  programming model ，能让动态本身具备类似进程那样的⽣命周期隔离？
````

## PDF 第 3 页

[原页](RAW.pdf#page=3)

````text
type Plugin<T> = Plugin.Function<T> | Plugin.Constructor<T> | Plugin.Object<T>
裸函数、类、带  apply  ⽅法的对象，三种写法最终都被解析成⼀个统⼀的回调。挂载⼀个
插件调⽤  ctx.plugin(plugin, config)，内部先找有没有已经存在的  Runtime 记录
（按回调函数身份做  key ，同⼀个插件多次挂载共享同⼀条  Runtime ），没有就新建，再造
⼀个  Fiber ，塞进这条  Runtime 的  fibers 列表⾥。
Fiber 是插件实例的⽣命周期状态机，六个状态：PENDING、LOADING、ACTIVE、
FAILED、DISPOSED、UNLOADING。插件声明了  inject: ['tools', 'shell']，对
应的  Fiber 会停在  PENDING，直到这两个服务都在依赖链上出现，才真正跑这个插件的代
码，进⼊  ACTIVE。这套等待机制是  Cordis ⾃⼰实现的依赖解析，插件作者不需要⼿写 " 等
对⽅准备好 " 的轮询逻辑。这对应空间可组合性：依赖出现后，组件⾃动激活。
卸载⼀个插件是否安全，由  effect 机制决定。插件注册的任何东⻄ —— 事件监听、服务、定
时器 —— 都通过  ctx.effect()  登记。登记时⽴刻执⾏⼀次，返回的撤销函数被推进⼀个
disposables 列表。论⽂  5.1.1 指出： Cordis 中每⼀次上下⽂变更都通过唯⼀原
语  ctx.effect 完成 —— 提供服务、实例化组件、所有修改上下⽂的操作都归约成⼀
次  ctx.effect 调⽤。⽤法⻓这样：
ctx.effect(() => {
  // 做副作⽤：注册监听、开定时器、提供服务 ……
  return () => { /* 逆：撤销上⾯的操作  */ }   // 返回  disposer
})
callback 可以返回⼀个  disposer 函数、⼀个  Promise，或者⼀个（异步）迭代器，逐段
yield disposer—— 每做⼀步副作⽤就交⼀个撤销函数。
在这⾥， " 副作⽤ " 的定义是：任何通过  Context 对共享环境进⾏的修改。这张表把⽇常操作
都覆盖了：
类别 例⼦
事件注册 ctx.on("foo", handler)
 ⸺ 往共享事件总线挂监听器
提供服务 ctx.provide(name, service)
 ⸺ 往上下⽂上 " 放 " ⼀个服务
挂载⼦组件 ctx.plugin(plugin)
 ⸺ ⼦插件本身就是⼀个 " ⽗级上的副作⽤ "
上下⽂扩展 ctx.extend()
 / ctx.intercept() / ctx.isolate()
外部资源 定时器、⽂件监听、 HTTP server 、⼦进程、 DB 连接等
状态变更 改  config 、改注册表、改  store
````

## PDF 第 4 页

[原页](RAW.pdf#page=4)

````text
Koishi ⾥  ctx.command(...)  注册命令、ctx.router.get(...)  注册  HTTP 路由；
DSH ⾥注册⼯具、挂  HMR 监听、起调度器 —— 全是副作⽤。 " 怎么逆转 " ，实现上很直接：
每个副作⽤都带着⾃⼰的撤销函数，运⾏时把它们按  LIFO 叠起来，卸载时整体执⾏⼀遍：
disposables.splice(0).reverse().forEach(dispose => dispose())
按注册的相反顺序逐个撤销，类似退栈。⼦  Fiber 的销毁函数本身也是通
过  parent.fiber.effect(...)  挂在⽗  Fiber 上注册的 —— 在源码⾥就是  Fiber 构造函数
末尾这⼀⾏：
this.dispose = parent.fiber.effect(() => { /* 注册插件  */ 
  return async () => { /* 注销插件  */ }
})
也就是说，⼀个插件本身  = ⽗  fiber 上的⼀个  effect ：插件的启动逻辑就是副作⽤，卸载逻
辑就是逆。⼦组件的逆会被  prepend 到⽗上下⽂的累加器上，形成递归结构（论⽂⾥叫
twisted composition ，记作  𝜕 ²Γ ）。所以卸载⼀个插件，会连带把它下⾯挂的⼦插件⼀起按
栈的顺序拆⼲净，不需要单独维护⼀张 " 谁依赖谁 " 的清理表。
这个机制还有两个细节保证可靠性。⼀是幂等：dispose()  ⾸次调⽤把  armed 标志置
false ，之后再次调⽤直接返回 —— 每个逆最多执⾏⼀次。 " 执⾏两次会在从未产⽣过该效应的
状态上应⽤逆，⽆从还原。 " ⼆是中断：如果  callback 返回的是迭代器，每⼀步之前会查
guard ，⼀旦失效⽴即停⽌，只执⾏已累积的逆 —— 热重载、卸载中途失败都能安全停住。事
件监听器也遵循同样的可逆机制：ctx.on(...)  返回  unsubscribe 函数，监听器登记在
fiber 的  hook 表⾥， fiber 卸载时统⼀移除。_unload()  跑完所有撤销函数后，如果发现
依赖⼜重新满⾜了，会⽴刻调  _reload()  重新拉起来 ——" 换掉某个服务的实现 " 在运⾏时
层⾯就是⼀次⾃动的卸载再加载。
⼀个插件的写法⼤致是这样（在 UI 界⾯上添加⼀个时钟）：
// 会话⽇志插件：注册⼀个事件监听  + ⼀个定时器，卸载时⾃动清理
export const name = 'session-logger'
````

## PDF 第 5 页

[原页](RAW.pdf#page=5)

````text
export function apply(ctx: Context) {
  // effect 回调在注册时⽴即执⾏
  ctx.effect(() => {
    // 副作⽤  1 ：订阅事件总线，把事件追加进⽇志
    const off = ctx.on('tool/result', (event) => appendToLog(event))
    // 副作⽤  2 ：开⼀个定时器，定期把缓冲刷到磁盘
    const timer = setInterval(flushBuffer, 1000)
    // 返回撤销函数：卸载时按注册的相反顺序执⾏
    return () => {
      clearInterval(timer) // 后注册，先撤销
      off()                // 再退订监听
    }
  })
}
挂载这个插件时，ctx.effect  的回调⽴即执⾏：监听器挂上、定时器启动，返回的撤销函
数被推进  disposables 列表。卸载时（插件被移除、会话结束、 HMR 重载），
disposables.splice(0).reverse()  按逆序逐个执⾏ —— 先  clearInterval ，
再  off()。撤销逻辑写在注册逻辑旁边，作者不需要在别处维护⼀份 " 哪⾥注销 " 的清单。
这个写法真的很像  React 。 useEffect  的形状⼏乎⼀样：useEffect(() => {
subscribe(); return () => unsubscribe() }, deps)—— 回调⾥做副作⽤，返回清理
函数，组件卸载时⾃动调⽤。两边共享同⼀个核⼼约定：副作⽤和它的逆写在⼀起，销毁由
框架触发。差异也清楚： React 的  effect 在渲染后执⾏，依赖变化时先清理再重建； Cordis
的  effect 在注册时⽴即执⾏，卸载时统⼀撤销，清理顺序有明确的  LIFO 保证（后注册的先
撤销，⼦插件随⽗插件逆序级联）。
那 " 逆转 " 为什么值得花这么⼤篇幅？论⽂把 " ⾃进化  Agent Harness" 列为两⼤动机之⼀，原
⽂⾮常尖锐：
这是 " ⾃进化 " 的前提： Agent ⾃⼰写插件 / ⼯具，运⾏时装进⾃⼰。装了坏的能回滚，⽽且回
滚机制本身（宿主进程）不能被新组件弄坏。普通插件系统做不到这⼀点，因为重启宿主意
味着丢失当前进程的所有状态。对照⼀下现有⽣态： VSCode 的扩展宿主⽆法卸载单个扩
展，禁⽤ / 卸载必须重启整个宿主； Koishi 社区⾥，改完配置  reload daemon 是很常⻅的操
作。 Cordis 的逆转让 " 卸载 " 成为与 " 加载 " 对称的⼀等操作 —— 服务不中断，其他插件不受影
响。
这套机制顺带解决了两个常⻅⼯程问题。⼀是失败原⼦性：插件初始化中途抛错（配置校验
失败、依赖缺失）， fiber 进⼊  FAILED 状态并  dispose—— 已经应⽤的⼀半效应被逆序清
未来的  harness 会在持续服务请求的同时⽣成并部署对⾃⼰组件的修改 …… 没有时间可
组合性，每次⾃我修改都迫使完整重启，丢弃所有进程内累积状态；更糟的是，⼀个有
缺陷的⾃我修改可能废掉唯⼀能⽤来恢复的那个进程。
````

## PDF 第 6 页

[原页](RAW.pdf#page=6)

````text
掉，不会残留部分初始化状态。⼆是级联清理，作者不⽤写卸载代码。论⽂  5.3 的关键论断
是：
卸载⼀个插件  → 逆序级联卸载它的⼦插件、释放它的定时器 / 监听器 /HTTP server/DB 连
接。清理正确性从 " 每个作者写对  deactivate" 变成 " 框架结构保证 " 。 VSCode 模型在这⾥有
⼀个短板：它的  deactivate 钩⼦和  activate 分离， " 效应清理与创建分离，违背关注点局部
性，完整清理难以验证 " 。
逆转机制的关键作⽤可以归纳为四点：① 开发期  HMR（改代码不重启、出错可事务回
滚）；② ⽣产期运⾏时插件装卸（服务零中断）；③ ⾃进化  Agent（改⾃⼰、坏了能⾃
救）；④ 失败原⼦性与级联清理（坏插件不残留影响、作者不⽤写卸载代码）。它把 " 卸
载 " 从⼿动善后变成框架保证的结构性操作，这是 " ⼀切皆插件、插件可热插拔 " 能成⽴的前
提。
三、四条约束与系统边界：框架怎么保证  effect 被执⾏
看到这⾥可能有⼈会问：如果作者把副作⽤写在  effect 外⾯，⽐如直接
给  globalThis.foo  赋值，这套机制还有效吗？论⽂正⾯回答了这个问题。框架的处理分
两边：⼀边在  API 层⾯约束，上下⽂修改只能通过  effect 完成；⼀边明确声明系统边界，
边界外的操作不受追踪。
框架从四个层⾯约束  effect 的⽤法。
第⼀， API ⼊⼝唯⼀。想⽤框架的任何能⼒ —— 事件  ctx.on、服务  ctx.provide、挂插
件  ctx.plugin、配服务  ctx.use—— 都只有  ctx  这⼀个⼊⼝，⽽  ctx  上的每个操作
内部都是  ctx.effect  的封装。 API 设计上不存在绕过  effect 使⽤框架功能的路径。
第⼆， Context 是  Proxy 。源码⾥就是⼀⾏：const self = new Proxy<this>(this,
ReflectService.handler)。对  ctx 的属性  get/set 全部⾛代理，这也是反应性  coeffect
（ " 访问即通知 " ）和  interception 的机制来源。所以  ctx.foo = x  这种直接赋值也会被
拦截并记录。
第三，⽣命周期状态机。每个  fiber 有状态机，ctx.effect()  第⼀⾏
是  this.assertActive()，在已卸载的  fiber 上创建  effect 会直接抛  CordisError
INACTIVE_EFFECT。卸载之后再注册副作⽤会被框架拒绝，从时间上消除了这类泄漏。
第四，事务性  HMR 。即使作者的逆写得有问题，新代码  import 失败（⽐如语法错误）时，
Algorithm 10 的  backup/restore 会让整个重载回滚到旧版本，系统不会停留在部分加载的
状态。这是机制层⾯的最后⼀道保障。
因为通过  context 的效应被⾃动追踪、逆⾃动复合，即使是没经验的作者，也能为⼀个
插件的  context 介导效应获得有序清理，⽽不⽤写卸载路径 —— 正确性从依赖每个作者
的⾃觉，变成由抽象层⼀次性承担。
````

## PDF 第 7 页

[原页](RAW.pdf#page=7)

````text
边界外的操作，框架明确不追踪。  论⽂  §6.1 把环境分成两半：边界内（ inside ）是系统能
独占修改、且能恢复原状的位置，操作记录在  Γ ，可以  recover ；边界外（ outside ）⼆者缺
⼀，操作表现为  idΓ ，既不追踪也不恢复。注意边界按位置划分，与介质⽆关：私有路径的
scratch ⽂件、只有本系统写的内存属于边界内；公共⽂件、别的进程也在写的东⻄属于边
界外。直接改全局变量、 monkey-patch 、写公共⽂件，都是边界外的操作。框架不会追踪
这些操作，也不会声称能恢复它们。这是设计上明确声明的边界。
更细的⼀层是获取 / 发射两阶段：获取阶段（ open/malloc/fork ）在边界内、可逆；发射阶段
（ write/send 的数据离开系统）在边界外、不可逆 —— 恢复只能靠  withholding （暂缓发
射，直到状态确定）或  compensation （补偿动作：删除创建的⽂件、退还收到的款项）。
补偿也按  LIFO 组合，但元理论不再保证。
⼯程上怎么处理边界外的资源？论⽂  §6.1 给了⼀个⼿段：coeffect 通过物化外部位置来移
动边界—— 把所有对该位置的访问限制在⼀组操作内，其中每个操作都提供逆，于是原本表
现为  idΓ 的操作变得可追踪、可恢复。在⼯程上，这就是服务（ service ）抽象：开发者通
过  ctx.database、ctx.assets  访问这些资源，不直接接触数据库连接、⽂件句柄、⼦
进程。资源⽣命周期被关进服务⾃⼰的  effect ⾥，服务提供者负责写对的逆，消费者只⾯对
⾼层接⼝。副作⽤从插件代码各处集中到服务实现内部，作者义务集中到少数服务实现者身
上。
还有最后⼀个问题：逆写得对不对，怎么判定？论⽂  §3.3.2 不要求 " 物理复原 " ，因为那做不
到（ free 不会还原堆布局，⽣成式名字不会再⽣）。恢复保证读作观察等价：
" 逆转 " 的含义是观察层⾯的还原：恢复前后的状态，没有任何观察者能区分。这就是逆的正
确性标准。堆布局没有还原也没关系，只要没有任何  coeffect 操作能察觉差异，就算恢复
成功。
这⼀章的保证可以分层整理成⼀张表：
层次 谁保证 内容
路径强制 框架（ API 设计） ⽤框架功能只能⾛  ctx ， ctx 内操作全是  effect 封装  → 必然
被追踪
时间强制 框架（状态机） 已卸载  fiber 上建  effect 直接抛  INACTIVE_EFFECT
属性拦截 框架（ Proxy ） ctx 属性读写被代理拦截、可记录
模块级事
务
框架（ HMR backup/restor
e ） import 失败整体回滚，不进半重载态
逆的正确
性 作者义务 运⾏时不验证  witness （ g(δ)=γ ），论⽂明说
两个状态相关，当没有任何观察者能区分它们。⽐较⾏为⽽⾮表示 …… 等价关系由
coeffect 各⾃携带的等价组装⽽成。
````

## PDF 第 8 页

[原页](RAW.pdf#page=8)

````text
层次 谁保证 内容
边界外⾏
为 ⽆保证 全局变量  / 公共⽂件  / 发射出去的数据  = idΓ
边界移动 coeffect / 服务物化 把外部位置封装成 " 可逆的服务 " ，访问受限、逆由服务提供
总结⼀下。框架把 " 必须通过  ctx.effect 修改上下⽂ " 变成唯⼀路径，把 " 逆是否正确 " 留给作
者义务，并明确声明系统边界。⼯程上的落点是服务物化：副作⽤集中在服务实现内部，义
务从 " 每个插件作者 " 收敛到 " 少数服务实现者 " 。论⽂还有⼀句很诚实的话： " 回调提供了逆，
但该逆是否真的恢复了伴随它的效应，是组件作者的责任（ obligation ），⽽不是运⾏时验
证的性质（ property ） " 。运⾏时保证 " 逆会被调⽤ " （结构性），不保证 " 逆写得对 " （语义
性）。
顺带⼀个观察：这套设计在  TS/JS ⾥落地最直接。  ⼤多数编译语⾔的类型系统基于类，类
型布局在编译期固定，⽆法通过动态加载新的编译结果来覆盖；加载进内存的类型信息通常
也⽆法卸载。 TS/JS 是原型系统，类型结构可以动态调整： Agent 造⼀个新⼯具，直接挂在
原型上，所有⼦组件⽴即感知并调⽤；撤销时从原型链切断，系统状态⽴即恢复。 Proxy 提
供 " 逻辑上极度解耦、语法上完全透明 " 的动态路由 —— 代码写下  ctx.tool  时， Proxy 完成
动态寻址与权限检查，静态语⾔很难实现这⼀点。 Module Augmentation 让插件能动态修
改全局  Context 的类型定义， agent ⽣成的新⼯具，类型提示和安全检查瞬时同步给整个系
统，实现 " 动态演化 " 与 " 类型安全 " 并存。另外， JS 有程序化的模块注册表，可以卸载模块并
让垃圾回收回收相关对象；在像  Swift 这种语⾔⾥，彻底清理已加载的类型元数据⼏乎不可
能。
四、 ctx.<service> 怎么解析：⼀个  Proxy 加⼀条  Fiber 链
插件之间怎么互相拿到对⽅提供的能⼒，值得单独说⼀下，这是 "everything is a plugin" 能
落地的另⼀半。
根上下⽂被包了⼀层  Proxy ：new Proxy(this, ReflectService.handler) 。访
问  ctx.tools、ctx.llm、ctx.session  这类属性时，⾛的是  Proxy 的  get 陷阱。⾃
身已有的属性直接⾛原⽣的  Reflect.get，遇到没⻅过的属性名，先查⼀下有没有注册过
的访问器，没有就沿着当前  Fiber 往上找：
let fiber = ctx.fiber
while (true) {
  const impl = fiber.store?.[prop]
  if (impl) return impl.value
  if (prop in fiber.inject) throw new Error('service not active')
  if (!fiber.runtime) throw new Error('unknown service')
  fiber = fiber.parent.fiber
}
⼀路往⽗  Fiber ⾛，直到找到提供这个服务的那⼀层，或者确认真的没⼈提供，抛错。
````

## PDF 第 9 页

[原页](RAW.pdf#page=9)

````text
真正把⼀个服务 " 发布 " 出去的地⽅是  Service  这个基类，构造时调
⽤  self.ctx.reflect.provide(name, self, check) 。provide()  本身也包
在  ctx.fiber.effect(...)  ⾥：往当前  Fiber 的  store ⾥塞⼀条  {name, value,
fiber, check}  记录，再唤醒等着这个服务的依赖⽅。返回的撤销函数负责把这条记录从
store ⾥摘掉，并重新通知⼀遍。⼀个服务被移除，⾛的是跟插件卸载完全⼀样的那套
effect 撤销机制，没有另开⼀条特殊路径。系统⾥没有⼀个专⻔的 " 服务注册中⼼ " 类。
ctx.<name>  这种写法背后就是⼀次  Proxy 拦截加⼀次沿  Fiber 链的查找。谁在哪⼀层注
册了什么，直接决定了谁能看到什么。
这套设计带来⼀个直接后果：作⽤域隔离是天然的。⼦  Fiber 能看到⽗  Fiber 注册的服务，
反过来不⾏。想让某个插件的服务只在特定范围内⽣效（⽐如某个  preset 专属的⽂件系统
实现），不需要额外的可⻅性控制逻辑，把这个插件挂在对应层级的  Fiber 下⾯，查找链条
⾃然会把它限制在那个范围⾥。
这套机制的价值在⼀个真实场景⾥能看清楚。 DeepSeek Harness 定义了⼀份 "llm" 服务接
⼝（packages/llm/llm），只规定 " 怎么发⼀次流式调⽤、怎么处理重试 " ，不关⼼具体是
哪家模型。系统⾥同时挂着两个实现这份接⼝的插件：dsh-llm-deepseek，专⻔适配⾃家
模型；dsh-llm-pi-ai，内部包了⼀个第三⽅  npm 库  @earendil-works/pi-ai，专⻔
做多家模型⼚商的协议转换（这个 "pi" 和外界拿来对⽐的那个  Pi agent harness 是两个不相
关的东⻄，撞了名字）。官⽅近  40 家可选模型⼚商，⼤部分由后⾯这个插件⽀持。两个插
件互不知道对⽅存在，装哪个、换哪个，上层  agent loop 的调⽤⽅式不⽤改⼀⾏，因为它
调的是接⼝本身。官⽅⽂档管这种搭配叫 " 设计验证双胞胎 " ：两套完全独⽴的实现都能满⾜
同⼀份定义，从侧⾯证明这份接⼝写得⾜够通⽤。
五、 Agent Loop ⾥真正值得说的⼏处设计
Loop 的整体形态跟眼下⼤多数框架差不多，模型输⼊输出、检测⼯具调⽤、执⾏、回填，
不重复讲。挑⼏处具体做法值得展开。
第⼀，轮次的结束条件有多种来源。除了 " 没有新的⼯具调⽤ " ，⼯具执⾏结果本身可以带⼀
个  concludesTurn: true  标记。⼯具的执⾏逻辑⽤这个标记声明 " 这⼀轮该停了 " ，不需
要等模型再说⼀句 " 好了 " 。
第⼆，max-tokens  状态是粘性的：
if (turnEnds === null || turnEnds.kind !== 'max-tokens') turnEnds = stepEnd
⼀旦某个  step 因为撑满输出上限被截断，即便后续的  step 正常完成，轮次最终报告的结束
原因也不会被覆盖为 " 正常完成 " 。上层（统计、⽇志展示）看到的 " 这轮被截断过 " 的信号，
不会因为后续步骤正常完成⽽被覆盖。
第三，轮次真正关闭前会⼴播⼀个  agent/turn-stopping  事件，这是⼀个可以被插件截
住的钩⼦。插件调⽤  agent.steer(...)  塞⼀条新消息，轮次会继续跑下去；什么都不
做，默认就真的结束。 " 什么时候真正收尾 " 这件事从  loop 内部移到了外部，任何插件都能
````

## PDF 第 10 页

[原页](RAW.pdf#page=10)

````text
在最后⼀刻决定 " 还没完，我还要说点什么 " ， loop 本身不需要预先知道有多少种 " 还没完 " 的
理由。
第四，⼯具调度这块，每次实际调⽤前都会向⼯具询问能否并⾏，判断不依赖静态⽩名单：
executionMode(exec): ToolExecutionMode {
  const tool = this.resolveExecution(exec.name, exec.agent)
  if (!tool?.isConcurrencySafe) return { kind: 'exclusive' }
  return tool.isConcurrencySafe(exec.arguments) === true
    ? { kind: 'parallel' }
    : { kind: 'exclusive' }
}
同⼀个⼯具，不同的参数组合能给出不同的答案（读⽂件永远并⾏安全，写⽂件只有⽬标路
径不冲突才安全）。调度器组队执⾏时，会在启动下⼀个调⽤之前重新判定⼀次模式。并⾏
组⾥如果混进了⼀个当下判定为互斥的调⽤，会就此截断这⼀组，不会把互斥调⽤硬塞进并
⾏批次。结果按模型原始给出的调⽤顺序提交，与调度完成顺序⽆关。
第五，⼯具执⾏前后的检查是独⽴的、可插拔的阶段，各⾃单独注册，不写在⼯具执⾏函数
内部。tools/pre-execute  是⼀个  waterfall 事件，任何插件都能在这⾥拦截或者要求审
批；通过后才进⼊内置的防护检查（⽐如同⼀个⼯具带同样参数被连续调⽤太多次会被提
醒）；然后才是真正调⽤⼯具体；跑完还有  tools/post-execute 让插件对结果做⼆次处
理。这四段是固定顺序、彼此独⽴注册的插件挂载点。新增⼀种审批策略或者防护规则，不
需要改动执⾏链路本身，挂⼀个新的事件监听就⾏。
六、 Preset 的两层  Scope 链：真实继承与影⼦路由表
Preset 的挂载机制解决了⼀个具体问题：怎么让同⼀份配置被多个会话复⽤，⼜不⽤每次都
重新解析⼀遍配置⽂件。
⼀份预设是⼀个⽬录，核⼼是⼀份  agent.cordis.yml，按顺序列出要挂载的插件和参
数。挂载这份⽂件⽤的是⼀个复⽤⾃  cordis ⽣态的  Include  插件，改名
叫  PresetTree：
const handle = agentCtx.plugin(PresetTree, { path: pathToFileURL(preset.path).href })
await handle.await()
PresetTree  重写了两个⽅法：解析裸模块名时，查找基于系统⾃⼰的  baseUrl ，预设⽬录
不参与解析；写回配置被直接禁⽤，预设源⽂件不会被意外修改。挂载完成后还会核对两件
事：有没有哪⼀⾏插件配置停在不可⽤的状态，有没有哪个服务在挂载过程中 " 泄漏 " 到预设
作⽤域之外。任何⼀项不满⾜，都会整体回滚。
scope 链的构造⽅式值得细看。从全局到某个预设，是⼀次真实的上下⽂派⽣：
createScope()  内 部调  ctx.plugin(scope)  拿 到 ⼀ 个  Fiber ，
再  fiber.ctx.extend({[kScope]: key})，这⼀步在  Cordis 的上下⽂树⾥真实存在⼀
个节点。从预设到具体某个会话，则使⽤另⼀种⽅式：
````

## PDF 第 11 页

[原页](RAW.pdf#page=11)

````text
this.bindings.set(agentKey, bindScopeParent(agentKey, standing.key))
bindScopeParent 往⼀张  WeakMap ⾥记⼀条 " 逻辑上级 " 关系，不在  Cordis 的  Fiber 树
⾥新开任何节点。
这么拆开的动机很直接：⼀份预设的 " 标准挂载实例 " 只建⼀次（ensureStanding()），后
续任意多个会话 —— 写作的、编码的、调研的 —— 都可以复⽤同⼀份实例，靠的就是往这张
WeakMap ⾥追加⼀条绑定，不⽤每接⼀个新会话就重新跑⼀遍插件加载。⼦  agent 要继承
⽗  agent 当前挂的预设，调⽤的  composeFrom(childCtx, parentCtx)  也只是这张表上
的⼀次查找加绑定，是同步操作，不会重新触发任何插件的挂载流程。⼦  agent 拿到的是跟
⽗  agent 完全同⼀份插件实例，包括同⼀批已经注册好的⼯具和提示词⽚段。
会话当前⽣效的是哪个预设，判定逻辑是倒着扫事件⽇志，找最新⼀条  agent-
preset/selected：
for (let index = session.events.length - 1; index >= 0; index -= 1) {
  const event = session.events[index]
  if (event?.type === 'agent-preset/selected') return event.data.agentPreset
}
return session.header.agentPreset
完全没有这类事件才回退到会话创建时的默认值。理论上，⼀个会话中途换预设是架构允许
的操作，查找逻辑天然⽀持这种情况，实际⽤不⽤是产品层⾯的决定。
预设的发现机制也值得⼀提。扫描⼀个预设根⽬录时，只认⽬录名匹配特定命名规则、且内
部有  agent.cordis.yml  的⼦⽬录。逐个校验  YAML 是否能解析、结构是否合法，损坏的
条⽬标记出来，不会中断整个扫描。多个根⽬录合并时，按顺序先出现的  id 优先，后⾯根⽬
录⾥同名的预设被忽略 —— 这给了 " ⽤户⾃定义预设覆盖官⽅预设 " （或反过来）的空间，取
决于根⽬录的注册顺序。
七、 Code Mode 的隔离⽅案： worker_threads
让模型写代码去编排多个⼯具调⽤，这个思路眼下不算新鲜， Codex 也做了⼀套。值得细看
的是隔离⽅案的选型和落地⽅式。
DeepSeek Harness 跑这段代码⽤的是  node:worker_threads，⼀个普通的  Node ⼯作
线程，与常⻅的  V8 隔离环境或者  vm2  是不同类型的⽅案。选这条路有⼀个明确考量：
node:vm 那类基于同进程的沙箱，原型链可以逃逸到主环境，热循环也⽆法从外部真正打
断，被认为不可靠。换成独⽴的⼯作线程，代价是每次跑代码都要开⼀个新线程，换来的是
⼀个真正独⽴的  V8 堆，以及⼀个可以从外部强制终⽌的执⾏环境。
模型写的代码，先过⼀遍  stripTypeScriptTypes  把类型标注剥掉，剥的时候⽤⼀层包装
前后缀撑住位置：
const stripped = stripTypeScriptTypes(prefix + program + suffix)
````

## PDF 第 12 页

[原页](RAW.pdf#page=12)

````text
保证剥完之后代码原本的⾏列号不变，报错定位对得上。剥完的代码被塞进⼀个动态构造的
异步函数：
const AsyncFunction = (async () => {}).constructor
const fn = new AsyncFunction(...bindingNames, ...errorClassNames, 'console', code)
const value = await fn(...bindings, ...errorClasses, consoleShim)
每个⼯具命名空间、每个约定好的错误类、还有⼀个替换⽤的  console ，都变成这个函数的
形参和实参。模型写的代码⾥可以直接⽤顶层  await，也能直接  return  ⼀个值出来。
⼯作线程本身有资源上限，resourceLimits.maxOldGenerationSizeMb  限制堆内存。另
外有两道独⽴的超时：⼀道拿事件循环利⽤率轮询，计算这段代码占了多少  CPU 时间；⼀
道是⼀个简单的  setTimeout，兜底总耗时。任意⼀道触发都会强制中断。
代码⾥调⽤⼯具，通过消息通道完成，不直接引⽤函数：
{ type: 'call', id, global: 'tools', name, args }   // worker → host
{ type: 'reply', id, ok: true, value }              // host → worker
宿主收到调⽤请求后，把它当成⼀次正常的⼯具调⽤，推进第五章讲的那条  pre-execute/ 防
护 /dispatch/post-execute 流⽔线，与模型直接发起的结构化⼯具调⽤共⽤同⼀套执⾏内
核，只是⼊⼝不同。通道两端都⼿动校验每⼀条收到的消息字段。宿主侧查找绑定函数
⽤  Object.hasOwn()  精确判断⾃有属性，构造暴露给代码的  tools  命名空间时，
⽤  Object.create(null) 起⼿，再逐个  Object.defineProperty  挂载。这些做法都是
为了同⼀个⽬的：防⽌代码⾥塞进  __proto__ 或  constructor  这类字段，绕过原型链产
⽣意料之外的⾏为。代码注释⾥直接写 " 把  worker 当成敌对的另⼀⽅来处理 " ，这个信任假
设是明确声明的。
Codex 那套做法的核⼼差异在隔离层：⽤⼀个独⽴的  V8 isolate ，⼯具挂在⼀个全局
的  tools  对象上，官⽅描述是 " 在⼀个全新的  V8 隔离环境⾥执⾏这段  JavaScript" 。两边
解决的是同⼀个问题 —— ⽤代码编排多个⼯具调⽤、减少往返 —— 隔离技术选型不同，背后权
衡的是 " 每次新建⼀个  isolate 的开销 " 和 " 每次开⼀个⼯作线程的开销 " 哪个更划算，以及各
⾃⽣态⾥现成的隔离原语是什么。
⼋、⼯具注册的分层遮蔽算法
⼯具怎么在不同作⽤域之间 " 就近覆盖 " ，是插件化设计⾥容易被忽略但很关键的⼀块，决定
了  preset 能否真正替换⼯具。
每个作⽤域维护⼀份⾃⼰的  ToolLayer，内部是⼀份按名字索引的表。决定 " 当前  agent
能看到哪些⼯具 " 的，是  view()  这⼀步：先加载全局层的⼯具，作为基础；再让每⼀层祖
先  scope 依次覆盖同名条⽬，越靠近当前  scope 的祖先优先级越⾼ —— 这⼀步只处理继承
来的那部分。限制规则（⽐如某个  preset 明确禁掉了某个⼯具）在这之后筛⼀遍。最后，
当前  scope ⾃⼰直接注册的⼯具，覆盖前⾯所有继承来的同名条⽬，即使限制规则禁⽤了这
个名字。这⼀步的顺序很关键：⾃⼰注册的⼯具优先于继承和限制规则。
````

## PDF 第 13 页

[原页](RAW.pdf#page=13)

````text
注册这⼀步本身也有硬校验：
register(definition: ToolDefinition): () => void {
  if (definition.name === RUN_CODE_NAME) {
    throw new Error(`tool name "${RUN_CODE_NAME}" is reserved for the Code Mode trans
  }
  assertSupportedJsonSchema(definition.output.schema)
  return this.layers.effect(this.ctx, layer => layer.tools.insert(definition.name, de
}
run_code  这个名字被硬编码保留，任何插件都不能注册或者覆盖它。理由写在代码注释
⾥：任何  agent 都可能给⾃⼰选⼀个代码模式，⼀个在默认部署下看似空闲的名字，⼀旦某
个  preset 挂载进来，随时可能跟  Code Mode 的调⽤⼊⼝产⽣冲突，所以⽆条件预留。
注册动作本身也⾛  effect()：调⽤  register()  拿到的撤销函数，插进当前  Fiber 的
disposables 列表。⼀个插件注册的⼯具，会随着这个插件被卸载⾃动从层⾥摘掉，不需要
额外写⼀段 " 卸载时记得把⼯具删掉 " 的清理代码 —— 这跟第⼆章讲的效果撤销机制是同⼀条
路径，⼯具注册只是众多 " 注册即副作⽤ " ⾥的⼀种。
⼯具执⾏本身也复⽤了这套调度器的并发契约。 Code Mode ⾥模型代码调⽤⼯具时，调⽤
会进⼊宿主侧同⼀个  TOOL_RUNTIME_SCHEDULER  的待处理队列，与模型直接发起的结构化
⼯具调⽤共享同⼀份并发控制、同⼀套前置检查 —— 这也是上⼀章说  Code Mode 与普通⼯
具调⽤ " 共⽤同⼀套执⾏内核，只是⼊⼝不同 " 的原因。
九、跟  Codex ⽐，⼏个⼯程决策的差异
核⼼循环的可替换性。 Codex 的⼯具接⼝、审批策略、沙箱策略都能配置，但驱动 " 采样 - 执
⾏ - 反馈 " 这条循环的代码固定在核⼼中，⽆法作为独⽴单元替换。 DeepSeek Harness ⾥这
条循环的具体实现（ReactLoopAgent）注册为⼀个⼯⼚，理论上可以被另⼀套完全不同的
循环实现替换掉。⽬前只有这⼀个实现挂在系统⾥，⼯⼚只允许注册⼀次。
沙箱的位置。 Codex 把  Linux 下的  bwrap/Landlock 、 macOS 下的  Seatbelt ，直接编译
进核⼼执⾏路径，属于基础设施。 DeepSeek Harness 把沙箱做成⼀层能⼒插件， Linux 上
通过⼀个独⽴的原⽣  Node 扩展调⽤  Landlock ，⾛的是前⾯⼏章讲的同⼀条服务注册路
径，理论上可以换成别的隔离实现，调⽤它的⼯具代码不需要改动。
代码规模的拆分粒度。 Codex 的  Rust 代码分成⼤约上百个  crate ； DeepSeek Harness 的
TypeScript 代码分成两百多个包。两边都不是单体架构，但  Codex 拆出来的模块最终都服
务于同⼀个不可替换的核⼼循环； DeepSeek Harness 拆出来的模块（包括循环本身）理论
上都处在同⼀个可替换层级上，没有哪⼀个模块的地位特殊。
代码编排⼯具调⽤的隔离选型。  两边独⽴得出了同⼀个功能判断：⼯具调⽤除了单个结构化
请求之外，还应该⽀持⽤代码编排。落地时隔离技术不同： Codex 选了独⽴的  V8 isolate ，
DeepSeek Harness 选了  worker_threads 。第七章已经展开过这个差异背后的取舍。
⼯ 具 暴 露 ⽅ 式 的 粒 度 。  Codex 的 ⼯ 具 接⼝⾥ ， 暴 露 ⽅式
（DIRECT/DEFERRED/CODE_MODE/Hidden ）是⼯具⾃⼰声明的⼀个静态标记。
````

## PDF 第 14 页

[原页](RAW.pdf#page=14)

````text
DeepSeek Harness ⾥，⼀个⼯具在某个  scope 下可⻅还是被覆盖，是运⾏时按  scope 链
实时计算出来的，同⼀个⼯具在不同会话⾥的可⻅性可以完全不同，取决于挂载了哪些
preset 。
附：从进程启动到⼀次⼯具调⽤，整条链路⾛⼀遍
进程启动，先看⽤的是哪个启动档（ Profile ），决定整个进程要装哪些插件包，交给  Cordis
的加载器逐个挂载，每个插件对应⼀个  Fiber 。装完， host 这⼀层准备好模型接⼊、凭据管
理、沙箱这些运⾏时基础设施。
⼀个会话开始， agent 注册表分配⼀个具体实例，这个实例挂在 " 全局 - 预设 - 会话 " 这条
scope 链下⾯。能看到哪些⼯具、哪些提示词，取决于它在这条链上的位置，以及第⼋章讲
的那套遮蔽规则。
Agent Loop 接管这个会话的运转：读取当前上下⽂，请求模型，检测⼯具调⽤，交给统⼀
的⼯具流⽔线⾛⼀遍前置检查、执⾏、后置处理。
每⼀步发⽣的事，不管是模型的输出还是⼯具的结果，都作为⼀条事件追加进这个会话的⽇
志⾥，不删除、不覆盖。这份⽇志同时是持久化的来源、下⼀次请求的上下⽂来源、⽹⻚界
⾯的展示来源，三条⽤途都从同⼀份⽇志投影出来。⽹⻚界⾯本身也是挂在这套体系⾥的⼀
组插件。
````

## PDF 第 15 页

[原页](RAW.pdf#page=15)

````text
这篇⽂章讲了不少具体机制： Cordis 的  Fiber ⽣命周期和  effect 撤销栈，ctx.
<service>  的  Proxy 解析， agent loop ⾥⼏处细节设计， preset 的两层  scope 链， Code
Mode 的隔离选型，⼯具注册的分层遮蔽算法。这些机制拼在⼀起，解决的是做  agent 产
品、或者深度使⽤  agent 时会反复遇到的⼏个具体问题。
第⼀个问题是加能⼒和改能⼒的⻛险。常⻅的做法是在⼀个核⼼循环外⾯挂插件，核⼼本身
很少改动，因为改动⼀次要担⼼影响⾯，回归测试也要重新跑。 DeepSeek Harness 把⻛险
控制粒度做到了插件级：⼀个插件注册的所有东⻄都通过  effect 登记，卸载时按注册的反顺
序原样撤销。新增或者替换⼀个能⼒，影响范围被框定在这个插件⾃⼰的边界⾥，验证范围
也缩⼩到这个边界。
第⼆个问题是，想让同⼀套  agent 服务不同场景，⼜不想每次都重新搭⼀遍环境。 preset
的两层  scope 链解决的是这个：⼀份预设的插件树只挂载⼀次，写作、编码、调研⼏种不同
⽤途的会话共享同⼀份已经跑起来的实例，靠⼀张逻辑⽗⼦表分流复⽤。
````

## PDF 第 16 页

[原页](RAW.pdf#page=16)

````text
第三个问题是多步骤任务⾥，⼀次⼀个⼯具调⽤的来回成本。 Code Mode 把这类任务的编
排逻辑交给模型⾃⼰写代码解决，减少了 " 说⼀句、等⼀下 " 的往返次数。这块  DeepSeek
Harness 和  Codex ⼏乎同时给出了同⼀个判断，只是隔离⽅案选得不⼀样。
第四个问题是⼯具的可⻅性和权限，在不同场景下常常只有两种状态：⼀个⼯具要么全局可
⽤，要么全局不可⽤。分层遮蔽算法把可⻅性变成运⾏时按  scope 链实时计算的结果，同⼀
个⼯具在不同预设、不同会话⾥可以有完全不同的可⻅性，⼯具代码⾥不需要写⼀堆条件判
断。
这⼏处设计共同指向⼀个更⼤的判断： agent 产品的竞争⼒，除了模型效果，还取决于运⾏
时这⼀层。运⾏时怎么组织、扩展成本有多⾼、换⼀个组件要付出多⼤代价，这些⼯程决策
同样会影响⼀个  agent 产品⽤起来顺不顺⼿。 DeepSeek Harness 把重点放在这⼀层，⽤
Cordis 这套现成的插件框架，以及 " 可逆副作⽤ " 这套设计哲学，把这⼀判断落实到具体的代
码结构上。效果怎么样，还得看这套架构在真实使⽤⾥能撑多久，能不能撑住更复杂的场
景。
展望：⼀个能对⾃⼰热更新的运⾏时，会⾛到哪
社区⾥已经有⼈给  DSH 做了连接通讯⼯具的插件了，⽐如把  Telegram 、 Discord 上的消息
接进来。当年  Koishi 靠  Cordis 把  QQ 、 Discord 、 Telegram 、微信的⼏⼗个插件拼在⼀
起，成了聊天机器⼈圈的现象级项⽬，也留下了 " 改完配置  reload daemon" 的⽇常。如今同
⼀个运⾏时内核被搬进  agent 产品，通讯⼯具插件开始出现 —— 当年那条路正在  DSH 上重
演，只是这⼀回，底层⾃带⼀条  agent loop 。
另⼀条路也在同时进⾏。 Hermes 、 OpenClaw 这类个⼈  AI 助⼿的成⻓⽅式，是往技能库⾥
不断加  skill ：能⼒变多，运⾏时的结构基本不动。 DSH 的成⻓⽅式在另⼀个维度：插件可以
热装卸，界⾯是插件、会话记录是插件、循环本身是插件，连  webui 都能在持续服务的同时
被换掉。论⽂⾥那句 "未来的  harness 会在持续服务请求的同时⽣成并部署对⾃⼰组件的修
改" ，在这件事上已经开始兑现了。
所以问题值得认真问⼀遍：那个整天  reload daemon 的 " ⻰虾 " ，动不动就把⾃⼰给搞炸，
这次是不是真的可以下班了？ DSH 会成为旧⼀代 " 插件机器⼈框架  + ⼿动配置 " ⼯作流的  AI
P.S. 在写这篇⽂章中提到的那个示例插件的时候还把 UI 给搞崩了，看来 HMR 的稳定性还
有待提升啊
````

## PDF 第 17 页

[原页](RAW.pdf#page=17)

````text
上位替代吗？
现在没有答案，但  webui 即插件，意味着产品形态本身可以热更新：改界⾯、换交互、加新
视图，不需要重启宿主，也不需要发布新版本。要替代的如果是⼀种⼯作⽅式，那它就是 " 拼
插件、写配置、重启验证 " 这个循环本身被压缩了。
对个⼈开发者来说，想做⼀个  AI 产品，以前要写前端、配后端、搭  agent 框架，三块互不
相通；在  DSH 上，这三层都是插件，挂进同⼀个运⾏时，界⾯还能直接热更新。⼀个想法
到可⽤的原型，甚⾄到能交付的成品，中间的距离正在被明显压缩。原型阶段跑通的东⻄，
加⼀个  preset 、配⼀个插件，就可能直接变成产品的⼀部分。
不过，从 " 偏开发者 " ⾛到 " ⾯向普通开发者 " ，中间还有⼀段路。现在跑  DSH 需要装  Node
环境，开终端⼿动敲命令启动  server 。这套⽤法对写代码的⼈是⽇常，对普通开发者来说确
实算不上优雅。技术复杂度不降下来， " 个⼈快速做出  AI 产品 " 就只对少数⼈成⽴。好在插件
化的好处恰恰在这⾥：宿主怎么启动、界⾯怎么呈现，都是可以替换的插件。把这层复杂度
包进安装包、包进⼀键启动，属于产品化的问题，架构上已经有位置放它了。
它能不能成为这个家族⾥下⼀代的现象级项⽬，最后取决于⼏件事：⽣态⾥⻓出来的插件够
不够多，真实场景撑不撑得住，⾯向普通开发者那层使⽤复杂度什么时候能被包起来。
⽬前  DeepSeek Harness 还是⼀个偏向开发者的产品，但相信距离其发展成⼀个 “Agent 界
的  VSCode” 这⼀天已经不远了。
推荐插件：⽣态建设⻜快！
这篇⽂章写到这⾥， GitHub 上  #dsh-plugin 这个  topic 下已经有  1000+ 个仓库了（检索
时  API 统计  1008 个）。官⽅本体  deepseek-ai/deepseek-harness  之外，第三⽅插件、
客户端、教程都在⻓。要翻全量清单，从⼏个精选索引⼊⼿最快：
awesome-dsh-plugin/awesome-dsh-plugin（ 256 ⭐ ） — 插件精选列表，中英双语
AdamPlatin123/awesome-dsh-plugins（ 507 ⭐ ） — ⾃动扫描索引所有  dsh 插件候选
0xsline/awesome-deepseek-harness（ 227 ⭐ ） — DSH ⽣态精选：插件、⼯具、基础设施
Electricitysheep/dsh-handbook（ 74 ⭐ ） — 从  0 到  1 的  DSH 深度⼿册，含插件开发
Web UI 增强  ：
zhu1090093659/dsh-web-ui（ 922 ⭐ ） — 任务⾯板、 Git 图、⽪肤中⼼合集
omdsh-dev/DSH-better-sidebar（ 371 ⭐ ） — 侧边栏⼯作台：⽂件、终端、 Git 、⼦代理
Small-tailqwq/dsh-deep-whale（ 237 ⭐ ） — 鲸⻥娘⽪肤系列
lhh010/dsh-minigames（ 10 ⭐ ） — 右侧  18 款⼩游戏摸⻥⾯板
视觉  / 多模态
liustack/modlens（ 857 ⭐ ） — 第⼀个视觉插件： OCR 、布局、语义结构化证据
Anionex/dsh-vision-toolkit（ 232 ⭐ ） — 图⽚问答、⻓截图  OCR 、 UI 还原
终端与桌⾯端 ——" 把复杂度包进安装包 " 已经有社区在做：
````

## PDF 第 18 页

[原页](RAW.pdf#page=18)

````text
ccch1mneyyy/dsh-TUI（ 487 ⭐ ） — Claude Code ⻛格全屏终端  UI
Ruler4396/dsh-launcher（ 40 ⭐ ） — Windows 轻量启动器
bruc3van/dsh-desktop（ 10 ⭐ ） — 社区第三⽅桌⾯客户端
记忆  / 上下⽂ —— 让会话跨过  session 的边界。
csyangwen/dsh-memory-evolve（ 24 ⭐ ） — 跨会话⻓期记忆  + ⾃我进化
Anionex/dsh-turn-rewind（ 25 ⭐ ） — 对话  / 代码状态回退
多  Agent / ⼯作流 —— 把  agent 编排成团队。
NanmiCoder/dsh-agent-teams（ 142 ⭐ ） — AgentTeams 插件
icetomoyo/dsh_workflow（ 42 ⭐ ） — 把⼀次性调度升级为可治理的  Workflow 层
通讯与通知
PlutoKeating/dsh-lark-bot（ 4 ⭐ ） — ⻜书机器⼈
sliverp/DeepSeek-harness-qqbot — QQ 机器⼈
LoserFox/telegram — Telegram
omdsh-dev/dsh-notification（ 26 ⭐ ） — 桌⾯通知
开发配套 —— 做插件的⼈先给⾃⼰做了⼯具。
omdsh-dev/dsh-genui（ 36 ⭐ ） — 对话内⽣成式  UI
omdsh-dev/dsh-at-file（ 62 ⭐ ） — Codex ⻛格  @file 引⽤
vlln/plugin-registry（ 21 ⭐ ） — 插件⽣态基建  + 开发引导
star 数为写⽂时参考值，具体以实际为准。完整清单，可以查看  github.com/topics/dsh-
plugin  。
撰⽂的参考资料，感谢⼤佬们分析：
为什么⽤  Cordis 做  AI Agent 运⾏时：从  QQ 机器⼈框架到  DeepSeek Harness（ CSDN ）
DeepSeek Harness 背后的秘密， Cordis 的设计哲学深度解读（知乎）
Cordis 88 ⻚设计论⽂：⼀个运⾏中的  Agent ，能不能 " 换零件 " ⽽不重启？
今晚 19:00 直播 DeepSeek Harness 拆解，不⻅不散～
腾讯程序员
已结束直播，可观看回放
DeepSeek Harness
观看回放
````

## PDF 第 19 页

[原页](RAW.pdf#page=19)

````text
阅读 5 . 2 万
留⾔
还没有留⾔，来写⾸评
写留⾔
````

