# 原文逐页转写

文本来自本次 PDF 文本层；不补写图片、截断内容或代码。图片和布局请打开每页 PDF 链接核对。AI 解释另见学习笔记。

## PDF 第 1 页

[原页](RAW.pdf#page=1)

````text
DeepSeek  Harness 背后的“⼼脏”： Cordis  到底是什么
腾讯程序员 2026 年 9 ⽉ 4 ⽇ 02 : 36⼴东原创 腾讯技术⼯程 874 ⼈
作者：lss233
1. 插件系统为什么要⼀个框架
1.1 四个问题
假设你写了⼀个聊天机器⼈，最初逻辑都在⼀个⽂件⾥。功能变多后你开始拆模块，但模块化
只解决 " 代码怎么组织 " ，解决不了另外四件事：
1. 安装：新功能怎么被 " 接 " 进系统？
2. 配置：同⼀功能在不同部署环境⽤不同配置，写在哪⾥？
3. 卸载：功能下线时，它的定时器、监听器、连接由谁来清理？清理不⼲净就是泄漏。
4. 协作：功能  A 依赖功能  B 的能⼒，但  B 可能还没启动、之后可能被替换成别的实现， A
该如何应对？
插件系统就是对这四个问题的回答。 Cordis 的特点是：它把 " 卸载 " 和 " 协作 " 这两件事，从 " 插
件作者的⾃觉 " 上升为 " 框架级保证 " 。
1.2 作者： Shigma
先认识⼀下写出它的⼈ ——Shigma。
Shigma  在第三⽅  QQ 机器⼈圈⼦⾥是相当出名的存在， ( 群友们 ) 亲切地称呼他为梦梦。他的
GitHub 账号（shigma）下有  130 多个公开仓库，如果你把  npm 上⼏个包的主页打开，会看
到⼀长串  maintainer 都是同⼀个⼈：
包 ⼀句话描述
koishi 跨平台聊天机器⼈框架（ npm 官⽅描述： "Made with Love" ）
DeepSeek Harness 的 " ⼀切皆插件 " 背后，跑的是⼀个叫  Cordis 的框架 —— 原本服务于
第三⽅  QQ 机器⼈，如今被  DeepSeek ⽤作整个  Agent 运⾏时的地基。这篇⽂章希望⽤
通俗易懂的语⾔，把  Cordis 的魅⼒介绍给⼤家：为什么 " 卸载 " 和 " 协作 " 能变成框架的默
认⾏为，为什么 " 改配置不⽤重启 " 是理所当然，为什么⼀篇  88 页的论⽂会以它为研究对
象。
````

## PDF 第 2 页

[原页](RAW.pdf#page=2)

````text
包 ⼀句话描述
cordis 插件化应⽤框架，本⽂的主⾓
@satorijs/core跨平台聊天协议适配层（ Koishi ⽀持  QQ 、 Discord 、 Telegram 的地基）
schemastery 类型驱动的  schema 校验器
minato 类型驱动的数据库框架（ Koishi 的数据层）
cosmokit 通⽤⼯具集
这是⼀套⼀个⼈撑起来的技术栈： Cordis 是⾻架（⽣命周期与依赖）， Schemastery 管配置校
验， Minato 管数据存取， Satorijs 管平台协议，Koishi  是集⼤成者，整个体系共同运⾏在
Cordis 之上。这篇⽂章⾥讲到的每⼀个概念（ ﬁber 、 eﬀect 、 Schema 、 Service ），都出⾃他
⼀⼈之⼿。
Shigma 在  2023 年底接受过腾讯媒体研究院《 20 多岁做什么时间更有价值》系列的专访
（BV1AQ4y157S8），那时他是研⼆学⽣，做  QQ 机器⼈开发五年了。被问到  AI 会不会取代⼈
类时，他说旧的岗位被取代，⼀定会创造出新的岗位，⼈类反⽽更有机会⽣活在更好的世界
⾥。他做  QQ 机器⼈的初衷之⼀，就是帮⾃⼰提升⼯作效率。那时  Cordis 还在  Koishi 的⼩圈
⼦⾥，没⼈想到它两年后会成为  DeepSeek Harness 的⼼脏。
如今， Cordis 的配套论⽂《 A Programming Paradigm for Spatiotemporal Composability 》以
预印本发布，署名单位是北京⼤学与  DeepSeek-AI ，第⼀作者  Yifan Shi ，合著者  Wei
Zhang 、 Tianyi Cui 。论⽂把  Cordis 的机制形式化，给出了定义、定理与证明。
1.3 出⾝与名字
Cordis 诞⽣于  Koishi——Shigma 创⽴的跨平台聊天机器⼈框架， 2020 年  1 ⽉发布⾸个正式
版本。 Koishi 的插件体系成熟后，核⼼层被独⽴出来成为通⽤框架： 2022 年  4 ⽉   cordis 包
登上  npm ； 2023 年底进⼊  3.x ； 2024 年底开始迭代  Cordis 4 （⾸个  4.0 预发布发布于  2024
年  11 ⽉），⼀次彻底重构，引⼊了基于  ﬁber  的⽣命周期体系。
````

## PDF 第 3 页

[原页](RAW.pdf#page=3)

````text
名字的由来： Cordis 是拉丁语 " ⼼ " （ cor ）的所有格，意为 " ⼼脏 " 。它是  Koishi 的⼼脏，如今
也成了  DeepSeek Harness 的⼼脏。
1.4 定位：元框架
Cordis 不是机器⼈框架（ Koishi 才是， Cordis 只是它的底层），也不是  DI 容器。传统  DI 回
答 " 谁创建谁 " ， Cordis 回答的是更困难的问题： " 谁在什么时候活着 " 。论⽂给它的定位
是  meta-framework：它规定 " 副作⽤如何组合、依赖如何解析 " ，但不预设任何业务领域，
QQ 机器⼈可以⽤它， Agent 运⾏时也可以。
2. 核⼼机制：五个概念，七个⼩节
Cordis 的全部语义可以浓缩为五个概念：插件、上下⽂、注⼊、事件、可逆副作⽤。由浅⼊
深逐⼀拆开。
2.1 第⼀个插件
写  Cordis 插件最爽的⼀点：完全不需要框架启动代码。
// hello.ts
import type { Context } from '@deepseek-ai/cordis'
export const name = 'hello'
export function apply(ctx: Context) {
  console.log('hello from my first plugin')
}
# cordis.yml —— 应⽤本身就是⼀个配置⽂件
- name: './hello.ts'
运⾏  DSH  ⾃带的⼩启动器（创建根  Context 、挂载  Loader 插件、读取   cordis.yml），输
出   hello from my first plugin。注意分⼯：插件只描述贡献，应⽤长什么样由配置决定。这就
是 " 配置即组合 " 。
插件有三种形态：
import { Service, type Context } from '@deepseek-ai/cordis'
export function apply(ctx: Context) {}          // 1. 函数形态（最常⻅）
export const objectPlugin = {                   // 2. 对象形态
  name: 'object-plugin',
  apply(ctx: Context) {},
}
````

## PDF 第 4 页

[原页](RAW.pdf#page=4)

````text
export class MyService extends Service {        // 3. 类形态（要对外提供服务时⽤）
  constructor(ctx: Context) {
    super(ctx, 'myService')
  }
}
2.2 上下⽂（ Context ）：⼀切操作的⼊⼝
在  Cordis ⾥，你⼏乎只会跟⼀个东西打交道：ctx。它是上下⽂，也是服务容器，承载了插
件能做的所有事情：
export function apply(ctx: Context) {
  ctx.on('some/event', (payload) => { /* ... */ })   // 监听事件（卸载时⾃动移除）
  ctx.effect(() => { /* ... */ })                    // 注册副作⽤（卸载时⾃动回滚）
  ctx.plugin(SomePlugin)                             // 挂载⼦插件（随⽗插件卸载）
  ctx.get('someService')                             // 读取服务（没有则  undefined ）
  ctx.provide('someValue', 42)                       // 提供服务
}
ctx.plugin(child) 不是简单的 " 注册 " ，⽽是派⽣出⼀个⼦上下⽂。插件因此不是平铺的，⽽是
⼀棵树：
⼦上下⽂能看到⽗上下⽂的⼀切（继承），但卸载是按层级的：⽗插件卸载，它的所有⼦插件
递归卸载；⼦插件卸载，不影响兄弟和⽗级。这棵插件树是  Cordis ⼀切⽣命周期语义的⾻
架。
在  DSH ⾥：你写的每⼀个⼯具插件、适配器插件、⾯板插件，都是这三种形态之⼀。
在  DSH ⾥：你看到的每个功能（⼯具、模型、会话、⾯板）都对应着这棵树上的⼀次   c
tx.plugin()。
````

## PDF 第 5 页

[原页](RAW.pdf#page=5)

````text
2.3 ﬁber ：插件的⽣命周期
Cordis 4 为每个已加载的插件实例维护⼀个  ﬁber （纤维），状态机如下：
PENDING ：已声明，但   inject 的服务尚未就绪，等待中；
LOADING / ACTIVE ：apply  正在执⾏、已完成；
FAILED ：apply  抛异常或配置校验失败；
UNLOADING / DISPOSED ：清理中、已拆除。
插件可能因配置修改、热重载、显式   dispose()  或依赖服务消失⽽被卸载。⽆论哪种原因，清
理都是⾃动的。
2.4 eﬀect ：可逆的副作⽤
这是  Cordis 的第⼀个核⼼机制，也是它与传统  DI 容器的区别所在。
ctx.effect(() => {
  const conn = createConnection()
  return () => conn.close()      // disposer ：如何清理
})
effect 的主体在加载时执⾏，返回的  disposer 在卸载时执⾏。你永远不需要⾃⼰调⽤清理函
数，不管插件因为什么原因被卸载， Cordis 都会替你把定时器、监听器、连接全部回滚。
此外， Cordis 的内置  API 本⾝就是  eﬀect ：ctx.on() 的监听器随插件卸载、ctx.plugin() 的⼦
插件递归卸载、服务注册随提供⽅消失。论⽂的实现章节有⼀个关键结论：Cordis 中所有对
上下⽂的变更，最终都归结为   ctx.effect  这⼀个原语，提供服务、挂载插件、注册监听器，
全是它的特例。因此 " 任何通过上下⽂进⾏的操作都⾃动可追踪、可恢复 " 不是设计⼝号，⽽是
结构事实。
插件作者只需要记住⼀条铁律：凡是⾃⼰创建、 Cordis 不管的资源，都包进   ctx.effect()。
在  DSH ⾥：cordis_inspect  巡检的就是每个  ﬁber 的状态；⼀个插件 " 加载了却没反应 " ，
多半是蹲在  PENDING 。
````

## PDF 第 6 页

[原页](RAW.pdf#page=6)

````text
因为副作⽤可逆，插件就可以被安全地卸载与重装，由此获得热重载（ HMR ）、故障⾃动恢
复、测试隔离。我们在第  5 章会看到， DSH 的 " 动态插件装了就卸 " 全部建⽴在这⼀⾏原语
上。
2.5 服务与注⼊：响应式的依赖
这是  Cordis 的第⼆个核⼼机制。
把⼀项能⼒挂到   ctx  上，让别的插件按名字取⽤，这就是  Service ：
import { Service, type Context } from '@deepseek-ai/cordis'
export class GreeterService extends Service {
  constructor(ctx: Context) {
    super(ctx, 'greeter')        // 注册：以后谁都能  ctx.greeter 拿到我
  }
  greet(who: string) {
    return `Hello, ${who}!`
  }
}
消费⽅只声明名字，不  import 实现：
export const inject = ['greeter']          // 声明依赖
export function apply(ctx: Context) {
  console.log(ctx.greeter.greet('world')  // 此时  greeter 必定就绪
}
inject 的语义是：插件保持  PENDING ，直到所列服务全部就绪。配置⽂件顺序⽆关紧要，启
动顺序由依赖关系决定。
与传统  DI 的本质区别在于：传统  DI 假设 " ⼀旦绑定，服务就⼀直在 " ； Cordis 的假设是 "服务
可以随时出现，也可以随时消失" 。在  Agent 场景⾥这是常态， LLM 提供⽅被限流、 MCP 服
务器崩溃导致⼯具被注销、⽂件  watcher 被系统杀死。 Cordis 的处理是：提供⽅被卸载时，
所有依赖它的插件⾃动卸载（ eﬀect 回滚）；新提供⽅就绪后，⾃动重载。依赖⽅不需要写任
何重连代码。
此外还有两个配套机制：
ctx.isolate(key, realm)：隔离。让⼀个作⽤域内某项服务解析到独⽴实例，两个组各⾃⽤
各⾃的实现，互不⼲扰；
在  DSH ⾥：改配置  →  旧插件卸载（所有  eﬀect 回滚）→  新插件加载，进程不重启。这
就是 " 改配置不⽤重启 " 的底层原理。
````

## PDF 第 7 页

[原页](RAW.pdf#page=7)

````text
ctx.intercept(key, meta)：拦截。给依赖访问附加元数据，外层上下⽂可以约束组件如何使
⽤某个依赖，⽽不修改组件本⾝。
2.6 事件：喊话与决策链
服务适合 " 直接打电话 " ，但很多时候插件只想 " 喊⼀嗓⼦ " 或者 " 拦⼀下 " ，不关⼼谁在听。
Cordis 的事件系统是类型化的，事件名和监听器签名靠  TypeScript 声明合并获得全链路类型
安全：
declare module '@deepseek-ai/cordis' {
  interface Events {
    'stats/report'(name: string, count: number): void
  }
}
ctx.emit('stats/report', 'tool_call', 42)   // 发出
ctx.on('stats/report', (name, count) => { /* 监听，卸载时⾃动移除  */ })
事件采⽤哪种分发模式，是它的公开契约，决定了监听器能否返回值、能否并发、能否短路：
模式 语义
emit 同步⼴播；不等待、不收集返回值
parallel 所有监听器并发执⾏并等待
serial 按序执⾏；第⼀个⾮空返回值胜出，停⽌后续
bail serial 的同步版本
waterfall 环绕中间件（ around-middleware ），见下
waterfall 是  DSH ⽤得最多的模式，本质是把  Koa 、 Express 的中间件搬进事件系统：每个监
听器收到参数和⼀个   next() continuation ：
ctx.on('some/decision', async (input, next) => {
  if (!hasPermission(input) return { denied: true }   // 不调  next() = 否决，短路
  return next()                                        // 调  next() = 放⾏
})
多个互不相识的插件，就这样组成⼀条决策链。这⾥有⼀条  DSH 明⽂纪律：只负责观察和记
录的  waterfall 监听器必须调⽤   next()，否则会⽆声地吞掉下游所有默认⾏为。
在  DSH ⾥：ctx.tools、ctx.llm、ctx.shell、ctx.sessions、ctx.skills  全都是这样的服
务（第  4 章会列出完整的槽位表）。
````

## PDF 第 8 页

[原页](RAW.pdf#page=8)

````text
2.7 Schema 与声明式组合：配置即程序
cordis.yml  ⾥的每⼀项（ entry ）都可以带元数据：
- id: greeter          # 稳定身份： loader 靠它区分" 修改 "与" 删了重加 "
  name: './greeter.ts'
- id: consumer
  name: './consumer.ts'
  disabled: true       # 保留条⽬但不挂载；改回后⾃动加载
id：不带   id 的条⽬每次读取都会获得新  id ，于是配置⽂件的任何编辑都会被当作 " 先删
后加 " 。带   id 才能精准增量更新。
group：把⼀组插件打包成单元整体装卸；配合   isolate  可让组内使⽤独⽴的服务实例。
Schema 校验：插件⽤  schema 声明配置结构（ schemastery ，就是  Shigma 写的那个），
Cordis 在调⽤   apply 前校验。配置⾮法则加载失败并给出精确错误，插件绝不会在配置
不完整时半启动。
export const Config: Schema<Config> = Schema.object({
  greeting: Schema.string().default('Hello'),
  targets: Schema.array(String).default(['world']),
})
!!js  表达式： DSH 的  Loader 扩展⽀持在   config  与   disabled  字段内写运⾏时求值的表
达式（如   !!js process.env.X ?? 'default'），并在依赖就绪后才求值。
配置即程序：修改配置  = 局部热替换，⽆需重启。
在  DSH ⾥：⼯具执⾏管道   tools/pre-execute → tools/execute → tools/post-execute  就是⼀
条  waterfall 链；approval/request、agent/request  也是。
在  DSH ⾥：cordis.patch.yml  与   --patch  覆盖层，就是这套声明式组合在⽣产环境的使
⽤⽅式（下⼀章详述）。
````

## PDF 第 9 页

[原页](RAW.pdf#page=9)

````text
Cordis 的五个核⼼概念全部出场：插件、上下⽂、注⼊、事件、可逆副作⽤，加上把它们串
起来的  Schema 。这些机制组合起来，能搭出多⼤的系统？下⼀章⽤  DeepSeek Harness 来
回答。
3. 在  DeepSeek Harness 中：⼀切皆插件
以下内容来⾃  DSH 0.1.0-rc.6 的实际源码（@deepseek-ai/cordis 4.0.1 ）。
3.1 启动：约⼆⼗⾏代码搭起整个应⽤
import { Context } from '@deepseek-ai/cordis'
import Loader from '@deepseek-ai/cordis-plugin-loader'
async function boot(binName, configPath, patches, prepare, baseUrl) {
  const ctx = new Context()
  ctx.baseUrl = /* 相对路径基准  */
  ctx.provide('dshHomePath', dshHomePath)                    // 引导值
  await ctx.plugin(Loader)                                   // 挂载  Loader
  await prepare?.(ctx)
  await mountRootInclude(ctx, configPath, patches, baseUrl)  // Include 挂载配置树
  await ctx.get('loader')?.await()                           // 等整棵树稳定
  await assertEntriesActivated(ctx, binName)                 // 审计：不允许条⽬半死不活
  return ctx
}
根  Context 只做了三件⼩事。其余⼀切，来⾃配置树。
3.2 Proﬁle ：应⽤被拆成可叠加的层
DSH 引⼊了  Proﬁle 概念：$DSH_HOME/profiles/< 名字 >  下的⼀个⽬录，包含  manifest （ds
h.profile.bundles  列出按顺序应⽤的组合包）和⽤户⾃⼰的   cordis.patch.yml。配置树的组装
顺序：
````

## PDF 第 10 页

[原页](RAW.pdf#page=10)

````text
Bundle （组合包）就是⼀个  npm 包，其   package.json  声明   "dsh": { "bundle": { "patch": "./cor
dis.patch.yml" } }。核⼼组合包   @deepseek-ai/dsh-base 的  patch 就是把⼏⼗个插件⼀次
insert 进空根：
- insert:
    - id: timer
      name: '@deepseek-ai/cordis-plugin-timer'
    - id: hmr
      name: '@deepseek-ai/cordis-plugin-hmr'
      config:
        root: ['.']
    - id: llm
      name: '@deepseek-ai/dsh-llm'
    - id: session
      name: '@deepseek-ai/dsh-session'
    - id: agent
      name: '@deepseek-ai/dsh-agent'
    - id: jobs
      name: '@deepseek-ai/dsh-jobs-local'
    # …… 以及更多
部署⽅想改默认⾏为，⽆需改任何源码，在⾃⼰的  patch 层按   id  覆盖⼀⾏即可（后写覆盖
先写、可   insert、可   disabled）。连 " 应⽤由哪些插件组成、各是什么配置 " 本⾝，都是可叠
加、可覆盖、可审计的声明，这就是 " ⼀切皆插件 " 的技术底座。
3.3 ⼯具流⽔线： Agent 的每⼀项能⼒
Agent 的能⼒边界是   ctx.tools  服务。注册⼀个⼯具，本质就是⼀个  Cordis 插件：
````

## PDF 第 11 页

[原页](RAW.pdf#page=11)

````text
export const name = 'greet-tool'
export const inject = ['tools']
export function apply(ctx: Context) {
  ctx.tools.register(defineTool({
    name: 'greet',
    description: 'Greet the named person.',
    parameters: { name: { type: 'string', required: true } },
    async execute(args) { return `Hello, ${args.name}!` },
  })
}
inject: ['tools'] 等待注册表就绪；ctx.tools.register(...)  注册即  eﬀect ，插件卸载时⼯具⾃动注
销；tools/result  事件让任何插件都能观察每次⼯具调⽤，⽆需认识执⾏者。本⽂写作过程中
⽤到的   bash、read、grep、subagent 等⼯具，全部挂在   ctx.tools  上。
3.4 ⾃指的设计： Agent 检查并改装⾃⼰的运⾏时
DSH 最值得注意的包是   @deepseek-ai/dsh-tool-cordis，官⽅称之为 " ⾃指的  Cordis ⼯具
集 " （ self-referential Cordis toolset ）。它给  Agent 提供五个⼯具：
cordis_inspect：对当前进程只读巡检，哪些服务在运⾏、各  ﬁber 的状态、注册了哪些⼯
具、每个   ctx.<key> 的完整契约；
cordis_define：现场定义⼀个⼩插件包（可带 " 宿主半  + 浏览器半 " ），只记录不执⾏；
cordis_run：把宿主半放⼊   node:vm 沙箱执⾏，把浏览器半推送到每个打开的⽹页；
cordis_stop  、   cordis_undefine：卸载动态包。
Agent 可以检查⾃⼰运⾏的框架、现场编写并运⾏动态插件、⽤完再卸载，全程不动   cordis.y
ml、不装  npm 包、不重启进程。 DSH 的信任⽴场很明确：动态包与  bash 同权，沙箱隔离
全局但不构成安全边界。
与之配套的 " 双半插件 " 设计：宿主半跑在服务端管逻辑，浏览器半跑在⽹页⾥管  UI ，⼆者通
过   host.call  做  RPC 。 " ⼀切皆插件 " 在  DSH ⾥是字⾯意义上的：前端  UI 组件也是插件（dsh
-client-ui-*  系列有⼏⼗个包），浏览器⾥运⾏着⼀个独⽴的  Cordis 客户端运⾏时。
⾃省  + 现场改装，这两点叠加就是 " 可进化  Agent" 的雏形，论⽂的结论部分恰好把 " ⾃进化
Agent 运⾏时 " 列为这套理论未来的验证⽅向（见  5.9 ）。
4. 在  DSH ⾥能开发什么：插件槽位与插件创意
这⼀章回答⼀个更实际的问题：如果我想在  DSH ⾥做点什么，有哪些 " 槽位 " 可以插？以下槽
位清单来⾃  DSH 的能⼒⽂档（ capability-seams ）与安装包中实际注册的服务键。
4.1 槽位：扩展点全部是服务
````

## PDF 第 12 页

[原页](RAW.pdf#page=12)

````text
DSH 的扩展点不是⼀个 "API 列表 " ，⽽是⼀张  Cordis 服务注册表：任何插件都可以注册新服
务，也可以替换已有服务的提供⽅（这正是  §2.5 响应式依赖的直接应⽤）。常⽤槽位按类别整
理如下：
类别 槽位（ctx.<key>） ⽤途 现有提供⽅（可替换）
执⾏ shell Bash 执⾏
bash-local
、bash-sandbox、pwsh-loc
al、 E2B
执⾏ codeRuntime 代码执⾏ code-runtime-worker
执⾏ subprocess
  、  terminals ⼦进程、持久  PTY subprocess-local
、terminal-bash
执⾏ lsp 语⾔服务器导航 lsp-local
模型 llm LLM 适配器注册表 llm-deepseek
、llm-pi-ai、llm-replay
智能
agents
  、  agentLoop  、  agent
DefaultModel
Agent 注册表、循环驱
动、默认模型
agent-loop
、agent-default-model
智能 agentPresets 会话级  Agent 组合 agent-presets
智能 subagents ⼦  Agent 提供⽅
subagent-spawn/fork-in-
process
、 ACP 、 Codex 、 Claude Code
数据
sessions
  、  sessionPersisten
ce
会话⽇志、持久化
session-persistence-jso
nl
、-sqlite
数据 sessionQuery 会话读取与检索 session-query-sqlite
数据
storage
  、  attachments  、  spi
llStore
通⽤存储、附件、溢出
存储
storage-json
、storage-sqlite、attach
ment-local、spill-local
数据
sessionTitle
  、  sessionProjectio
ns
会话标题、投影单元
session-title-first-pro
mpt-llm
 等
环境 fs ⽂件系统提供⽅ fs-local
、fs-sandbox、fs-e2b
环境 web Web 访问（抓取、搜
索）
web-fetch-http
、web-search-deepseek/ex
a/perplexity
环境 credentials
  、  settings 凭据、⽤户设置 credentials-local
、settings-file
环境 webServer
  、  directoryPickerHTTP 路由、⽬录选择
webserver
、directory-picker-nativ
e/browse
````

## PDF 第 13 页

[原页](RAW.pdf#page=13)

````text
类别 槽位（ctx.<key>） ⽤途 现有提供⽅（可替换）
治理 tools ⼯具注册表与受保护执
⾏管道 所有  dsh-tool-*
治理
approval
  、  permissionPreset
s  、  sandboxPolicy
审批、权限、沙箱策略
approval
、permission-presets、sa
ndbox-policy
编排
goals
  、  jobs  、  workflowEn
gine  、  planMode
长期⽬标、后台任务、
⼯作流、计划模式
dsh-goal
、dsh-jobs-local、workfl
ow-worker-thread
⾃指 dynamicCordisRunner
  、  cordisInspect
动态包宿主、运⾏时巡
检 cordis-host-runner
前端
slots
  、  clientModules  、  t
heme  、  locale
UI 槽位、客户端插件
图、主题、语⾔
dsh-client-ui-*
  系列
4.2 槽位背后的设计：三种⾓⾊
DSH 对 " 可替换能⼒ " 有⼀套固定模式，Service Deﬁnition 、 Service Provider 、
Consumer 三种⾓⾊，以   shell  为例：
Deﬁnition 只声明服务与类型，⼏乎不变；
Provider 可以独⽴替换，换⼀个提供⽅（⽐如换成沙箱执⾏），通过   cordis.yml  改⼀⾏配
置， Deﬁnition 和所有  Consumer 保持不变；
Consumer 与  Provider 互不依赖。
这套模式就是 " ⼀切皆插件 " 在能⼒层⾯的落地：每⼀项能⼒都是⼀个  seam （接缝），接缝两侧
可以独⽴演进。
4.3 开发⼊⼝：三种⽅式把插件装进去
1. patch 覆盖层（最快）：写⼀个  YAML ，dsh web --patch ./my-plugins.yml 启动时插⼊条
⽬：
   - insert:
       - id: my-plugin
````

## PDF 第 14 页

[原页](RAW.pdf#page=14)

````text
         name: '/abs/path/to/my-plugin.ts'
2. proﬁle 的   cordis.patch.yml：常驻⽣效的⽤户层；
3. bundle 包：把⼀组插件打包成  npm 包，声明   dsh.bundle.patch，成为可复⽤的 " 组合
包 " 。
插件代码本⾝依然是  Cordis 那套：函数、对象、类三种形态、inject  声明依赖、ctx.effec
t  管理资源、Schema  校验配置、ctx.tools.register(defineTool(...)  注册⼯具。
4.4 已经存在的插件（举例）
内置的插件（dsh-* 包）按⾓⾊分四类：
⼯具类（挂在   ctx.tools  上，即  Agent 能调⽤的能⼒）：tool-bash、tool-fs  、   tool-fs-sea
rch、tool-web、tool-subagent  、   tool-subagent-control、tool-workflow、tool-goal、
tool-jobs、tool-todo、tool-skill、tool-ralph、tool-ask-user、tool-lsp、tool-cordis
（⾃指⼯具集） ……
提供⽅类：模型适配器（ DeepSeek 、 pi-ai 多提供⽅、 replay ）、 shell 提供⽅（本地、沙
箱、 PowerShell ）、 fs 提供⽅（本地、沙箱、 E2B ）、 web 搜索源（ DeepSeek 、 Exa 、
Perplexity ）、持久化后端（ JSONL 、 SQLite ）、存储后端、技能提供⽅、会话标题⽣成
器 ……
系统类：上下⽂压缩（compaction-basic）、 token 计量、消息反馈、权限预设、计划模
式、长期⽬标、审批管道 ……
前端类：dsh-client-ui-*  数⼗个包，设置页、模型选择、插件管理、任务⾯板、⼦  Agent
⾯板、⽬标⾯板、主题 ……
内置之外，社区已经长出了⼀⽚插件⽣态。 GitHub 上有⼀个社区维护的精选列表  awesome-
dsh-plugin（搜   dsh-plugin 话题就能找到），截⾄  2026 年  8 ⽉收录  174 个可通过   dsh plugi
n add  安装的插件：
⼏个有代表性的例⼦：
改界⾯：dsh-visualize 让模型把交互式  HTML 卡⽚直接画进会话流；dsh-TUI  是像素鲸鱼
顶栏的全屏终端  UI ；dsh-deep-whale  是⼀系列  Web ⽪肤；dsh-balance-meter  在输⼊框显
⽰账户余额与花费；
改记忆：dsh-memento  提供有界、分层、带审批门、可审计的跨会话记忆；dsh-mneme  ⽤
SQLite + 可编辑的  Markdown 镜像做跨会话记忆；
改能⼒：dsh-computer-use 让  Agent 控制  macOS ；dsh-data-agent  帮  AI 连数据库写
SQL ；dsh-docker  是带护栏的容器控制；dsh-toolkit  ⼀键装⼗件套零依赖⼯具；
改协作：dsh-agent-teams  多智能体团队；dsh-crosstalk  跨会话互发消息；dsh-chat-
import  把  Claude Code 、 Codex 、 ChatGPT 的聊天记录导⼊为  DSH 会话；
````

## PDF 第 15 页

[原页](RAW.pdf#page=15)

````text
⾃进化：dsh-evolve 让  Agent 在会话内给⾃⼰热挂载、卸载持久化插件；dsh-continual-
evolve 从会话轨迹沉淀可审计、可回滚的  harness 状态；
插件基建：dsh-find-plugin 让  Agent 在会话内直接搜索并安装插件；dsh-plugin-
manager  提供   dsh pm  多源插件管理。
4.5 可能的插件：常规与 " 惊艳 "
常规⽅向（模式成熟、直接照着现有插件写）：
新⼯具：数据库查询、浏览器⾃动化、 Docker 、 K8s 操作、 MCP 客户端、 Git 操作、部署
与测试运⾏器；
新提供⽅：接⼊任意  LLM 的适配器、远程、容器  shell 提供⽅、新的搜索源、新的持久化
与存储后端、新的技能提供⽅；
治理与可观测：审批策略插件（挂在  waterfall 链上）、权限预设、审计⽇志、 token 预算
控制、 OTel 遥测（已有  seam ）；
界⾯：新的  Web ⾯板（slots）、命令⾯板、通过   webServer 暴露  HTTP API 。
````

## PDF 第 16 页

[原页](RAW.pdf#page=16)

````text
" 惊艳 " ⽅向（以下都不是空想，每⼀步都落在  DSH 现成的机制上）：
1. 会写插件的插件：插件可以⽤   ctx.loader.create()  在运⾏时动态挂载、更新、移除其他配
置条⽬，插件本⾝去 " 组装 " 插件；再配合   cordis_define  、   cordis_run， Agent 可以现场
⽣成并运⾏⾃⼰的⼯具。这是 " ⾃进化 " 的闭环：⽣成  →  沙箱运⾏  →  观测结果  →  保留或
卸载。
2. 会话级隔离的 " 分⾝ "：ctx.isolate +  agentPresets 让每个会话拥有独⽴配置的服务实例，
这个会话⽤  DeepSeek 模型  + 本地执⾏，那个会话⽤别的模型  + 沙箱执⾏，互不⼲扰。相
当于⼀个进程⾥跑多个 " 虚拟  Harness" 。
3. ⽣产环境不停机换引擎：在  patch 层替换   llm、shell 的提供⽅，所有依赖⽅⾃动卸载重
载；如果按论⽂的  service broker 模式实现（见  5.7 ），还能做灰度与滚动切换（新旧提供
⽅并存，按权重分配请求）。
4. 策略⽹关：⽤  waterfall 事件把 " 审批  →  权限  →  限流  →  审计 " 串成⼀条决策链，新增⼀条
策略  = 新增⼀个监听器插件，不需要改执⾏管道。
5. 专家  Agent 池：基于   ctx.subagents 构建⼀组常驻⼦  Agent （代码审查员、测试员、⽂档
员），主  Agent 按需调度、失败续接，⼦  Agent 从 " ⼀次性⼯具 " 升级为 " 常驻服务 " 。
6. 分层记忆系统：在   sessionProjections、sessionProjectionCache  上实现⼯作记忆、长期记
忆与摘要折叠， Agent 的 " 记忆 " 变成可插拔的插件。
7. 浏览器双半插件：⼀个动态包同时携带宿主半与浏览器半，现场给  Web UI 注⼊⼀个⾯
板、⼀个监控视图，⽤完即卸，全程不提交代码。
8. ⼯作流即插件：在   workflowEngine  上注册新的编排范式（除  Ralph 循环、并⾏  fan-out
之外的⾃定义迭代模式），把 " 如何多  Agent 协作 " 本⾝变成可组合的插件。
这些⽅向的共同点是：它们都靠 " 插⼀个插件 " 实现，⽽不是靠 " 改框架 "，这正是  Cordis 的时
空可组合性在  DSH ⾥的兑现。
5. 论⽂说了什么：从 " 好⽤的框架 " 到 " 被证明的范式 "
Cordis 的配套论⽂《 A Programming Paradigm for Spatiotemporal Composability 》
（cordiverse/paper）由北京⼤学与  DeepSeek-AI 的研究者合著， 88 页预印本。它做的事不
是 " 给  Cordis 写说明书 " ，⽽是把  Cordis 的核⼼机制形式化，证明它们构成⼀种新的编程范
式。论⽂⾥没有⼀句 " 我们的框架很优秀 " ，有的是定义、定理与证明，以及⼀个贯穿始终的主
张：
5.1 论⽂要解决的问题：动态组合为什么难
软件⼯程的⼀切都建⽴在 " 组合 " 之上。但传统组合是静态的：函数调⽤、模块导⼊、类继承在
编译期就固定下来。⽽现代软件越来越需要动态组合，运⾏时加载、卸载、重配置组件。插件
动态组合（运⾏时装卸组件）缺乏形式基础； Cordis ⽤两个运⾏时机制把它补上了，并
证明了由此得到的性质。
````

## PDF 第 17 页

[原页](RAW.pdf#page=17)

````text
架构和⾃进化  Agent 都需要 " 运⾏时安全地增删功能 " ，可这类系统的理论基础，远不如静态组
合成熟。
论⽂把动态组合拆成两个正交维度：
时间维度（ temporal composability ）：组件被移除时，它对共享环境做的修改必须被完
整、安全地逆转。静态程序⾥这对应词法作⽤域（ RAII ：资源获取即初始化）；动态场景下
副作⽤可能是长⽣命周期的、没有词法边界的，难得多。
空间维度（ spatial composability ）：组件必须能声明、发现、解析相互依赖。静态程序
⾥这对应模块解析；动态场景下依赖会出现、消失、更换⾝份。
为什么这个问题被长期回避？因为操作系统和容器编排提供了⼀个粗粒度替代：进程粒度的时
间可组合性（进程死了状态全清）＋服务粒度的空间可组合性（依赖交给编排器）。但代价沉
重：每次重启丢弃全部进程内状态（缓存、连接、半成品计算），重建要花⼏秒到⼏分钟；跨
地址空间的依赖⽆法⽤函数调⽤表达，只能⾛⽹络。
论⽂⽤  VS Code 做反例，把痛点钉死：前  100 个热门扩展⾥  87 个含可执⾏代码，但扩展宿
主⽆法在运⾏时卸载单个扩展，禁⽤或卸载必须重启整个宿主；deactivate 钩⼦只在宿主进
程退出时调⽤，且把 " 创建效果 " 和 " 清理效果 " 分在两处，违背了关注点局部性。扩展间依赖机
制（extensionDependencies）只有  7 个扩展使⽤，因为依赖解析是⽆类型的   any，没有结构
契约。
这些局限不是  VS Code 独有的，⽽是插件系统的通病。 Cordis 的⽬标，就是把时间与空间两
个维度上的保证，做成结构性质。
5.2 理论⽀柱： eﬀect 与  coeﬀect
论⽂的两个⽀柱是编程语⾔理论⾥的两个经典概念：
eﬀect （效应）：描述 " 计算对环境做了什么 " ，写⽂件、分配内存、发消息。源⾃  Moggi 的
monad 理论， Haskell 的   IO、代数效应与处理器（ algebraic eﬀects ）都属于这条线。
coeﬀect （余效应）：描述 " 计算对环境要求什么 " ，需要读哪些配置、依赖哪些服务。源⾃
Petricek 等⼈  2013 年的⼯作，是  eﬀect 的对偶。
关键观察：这两个概念传统上都是编译期静态分析⼯具，类型系统在编译时检查 " 这段代码可
能产⽣什么副作⽤、需要什么上下⽂ " ，约束是词法作⽤域内固定的。 Cordis 的论⽂把它们提
升为运⾏时机制，让它们能在组件随时到达和离开的动态场景下⼯作。这是论⽂区别于既有⼯
作的出发点。
5.3 可逆副作⽤：把 " 撤销 " 做成结构保证
5.3.1 核⼼想法：每个变换都携带逆
时间维度的诉求是：卸载组件  = 恢复共享环境。论⽂把  eﬀect 建模为：
e : Γ → Γ × (Γ → Γ)
````

## PDF 第 18 页

[原页](RAW.pdf#page=18)

````text
⼀个  eﬀect 函数作⽤于当前上下⽂  Γ ，返回新上下⽂和⼀个逆函数（ undo 函数）。把逆交给运
⾏时， eﬀect 就可追踪；逆被运⾏时组合，恢复就成为结构保证，⽽不是 " 开发者记得清理 " 。
形式上，定义效应上下⽂∂Γ = (γ, φ)：γ  是当前状态，φ  是累加器，到⽬前为⽌所有  eﬀect
的逆的复合。于是：
track：执⾏  eﬀect 时，把新状态写⼊   γ，把它的逆复合进   φ；
recover：卸载时，把   φ  作⽤到当前状态，φ(γ)  就回到初始状态（论⽂称   φ(γ) = γ0  为
soundness invariant ，健全性不变量）；
逆按相反顺序累积（ twisted composition ）：先执⾏的  eﬀect 后撤销，天然  LIFO 。
Cordis 中所有上下⽂变更都归结为   ctx.effect  这⼀个原语，提供服务、挂载插件、注册监听
器全是它的特例。现在它有了证明。
5.3.2 关键性质  1 ：精确恢复
如果每个逆都在它⾃⼰应⽤时的状态上执⾏，恢复是精确的（ Theorem 7 、 16 ）：按  LIFO 撤
销时，每个逆⾯对的正是它当初执⾏时的上下⽂，因此⼀切状态都被还原。
但真实系统⾥，多个组件交错运⾏，撤销  A 时， A 之后还有  B 、 C 的  eﬀect 在执⾏。这时  A
的逆⾯对的是⼀个被 " 外来  eﬀect 移动过 " 的状态。
5.3.3 关键性质  2 ：独⽴性（ independence ）
论⽂定义两个  eﬀect 独⽴，当它们的所有变换互相可交换、且互不⼲扰对⽅产出的逆。对独⽴
的⼀族  eﬀect ，可以按任意顺序撤销（ Corollary 21 ），这正是 " 从交错运⾏的多个组件中单独
撤掉⼀个 " 的理论基础：
````

## PDF 第 19 页

[原页](RAW.pdf#page=19)

````text
实际上，独⽴性的条件⼤多⾃动成⽴：不同  key 上的操作天然独⽴（ Theorem 40 ，读写不同
依赖表条⽬的操作当然可交换）。这正是事件监听器、路由注册这类 " 注册表操作 " 可任意增删
的数学解释。⽽ " 有序链 " （⽐如中间件插⼊顺序影响请求）则不是独⽴的，需要靠别处维持顺
序，这就是为什么  Cordis 的   ctx.on(event, listener, { prepend }) 和  waterfall 事件需要显式顺序
语义。
5.3.4 关键性质  3 ：恢复是 " 观察等价 " ⽽⾮字⾯相等
⼀个细节：free  把内存块还给分配器，并不会恢复   malloc  之前堆的布局；⽣成式名字被丢
弃后，下次创建⼜是新名字。所以论⽂把恢复读作观察等价  ≃：两个状态相关，当没有观察者
能区分它们。观察者的观察⼿段就是  coeﬀect ，每个依赖键⾃带⼀个等价关系，状态的等价由
各键的等价组装⽽成（ Deﬁnition 33 ）。恢复的语义不是 " 回到过去 " ，⽽是 " 任何观察者都看不
出区别 "—— 这是让可逆性在真实系统⾥可成⽴的关键让步，也让独⽴性变得可达：两个操作
留下的值只要  ≃  等价，就算可交换。
5.4 响应式余效应：把 " 依赖 " 做成结构保证
5.4.1 依赖表也是类型化的
空间维度的诉求是：组件声明依赖，系统在运⾏时解析、提供、撤销依赖。论⽂把  IoC 容器
形式化为余效应上下⽂  Σ：⼀个类型化的部分函数，把依赖键   k  映射到类型   V_k 的值，每
个键都有静态类型，这是对 " 依赖查找是   any"的根治。
两个核⼼操作   get、set，其中   set(k, v) 的类型恰好是  5.3 的  eﬀect 函数，注册⼀个依赖本
⾝就是可逆  eﬀect ，撤销提供⽅时依赖⾃动消失。这就是两层机制协同的地⽅：coeﬀect 操作
是  eﬀect ，⽽  eﬀect 可逆。
5.4.2 规范与通知：激活、停⽤、⽆关
组件⽤规范（ speciﬁcation ）d ⊆  K  声明它需要的依赖集合；系统判定满⾜性   σ ⊨  d
（d  中每个键都在表⾥）。关键在于把每个上下⽂变化对照规范分类（ Deﬁnition 26 ）：
activating   ：之前不满⾜，现在满⾜了
deactivating ：之前满⾜，现在不满⾜了
neutral       ：与满⾜性⽆关
反应式不变量：activating 触发组件执⾏（带完整  eﬀect 追踪）， deactivating 触发组件恢复
（应⽤累加器）。由于所有变更都经  eﬀect 函数（可逆），满⾜性变化在每个  eﬀect 边界都可
被检测， " 每个依赖变化都会被观察到 " 是代数层⾯的保证，不是靠轮询。
这就是   inject 的数学形式：inject: ['greeter']  就是声明   d = {greeter}， ﬁber 保持  PENDING
直到   σ ⊨  d，提供⽅卸载时   d  失满⾜  →  deactivating →  依赖⽅⾃动卸载，提供⽅恢复  →
只要组件的  eﬀect 两两独⽴，任何⼀个组件都可以被单独卸载，它的贡献归零，周围组
件的状态不受影响。
````

## PDF 第 20 页

[原页](RAW.pdf#page=20)

````text
activating →  ⾃动重载。
5.4.3 隔离与拦截：调整 " 解析 " ⽽⾮ " 存储 "
论⽂还形式化了两个机制（对应   ctx.isolate  、   ctx.intercept）：
隔离（ coeﬀect isolation ）：引⼊  realm （域）表，get(k)  先解析   ρ(k) 得到  realm ，再
查  realm ⾥的值，同⼀个键在不同上下⽂解析到不同值。论⽂称这是 " 运⾏时  ad-hoc 多
态 " 。多租户、测试环境、组件沙箱都是它的直接应⽤。与  DI 的差别：isolate  是派⽣
（ derived ）实现，⽣成⼀个新上下⽂，不改共享表，回收时直接丢弃，⽆需逆。
拦截（ coeﬀect interception ）：给依赖访问附加元数据。get(k, μ)  实际调⽤   σ(k)(μ ⊕  ι
(k)，组件声明的元数据与上下⽂携带的元数据按各键的⼳半群语义合并（标量覆盖、集
合取并），右偏：外层上下⽂可以约束组件如何使⽤某个依赖，⽽不修改组件本⾝。⽐如沙
箱策略插件可以给   shell  键附加元数据，约束所有使⽤⽅。
5.5 统⼀上下⽂： Context 即范式
5.5.1 ⼀个⾃相似的递归类型
把两层机制统⼀，论⽂定义上下⽂类型：
Γ∞ = μ Γ. Γ × (Γ → Γ) × Σ
⾃相似的递归类型：当前状态（递归）、累加器（恢复本层  eﬀect ）、依赖表（ coeﬀect 信
息）。三个投影让 " 效果 " 与 " 余效应 " 两个⽅向收进同⼀个   ctx，每个操作都能归因到调⽤它的
具体上下⽂，进⽽归因到拥有该上下⽂的组件。由于  Σ 的值类型⽆约束， " 任何需要在组件间
共享的状态都可以编码成⼀个依赖 " ， Σ 不只是依赖表，它包含了⼀切共享可变状态。
````

## PDF 第 21 页

[原页](RAW.pdf#page=21)

````text
层次组合是递归结构的直接推论：加载组件  = 插电（执⾏其  eﬀect ），卸载  = 拔电（恢复其
eﬀect ），⽗上下⽂聚合⼦  eﬀect ，任意嵌套，这正是  Cordis 的插件树（见  2.2 ）。
5.5.2 观察等价供给独⽴性
5. 3 的独⽴性需要⼀个条件， 5.5 补上了它：在  coeﬀect 上定义观察等价，商掉（ quotient ）
之后，独⽴性变得可达，两个操作只要留下  ≃  等价的表，就算可交换（ Theorem 42 ）。论
⽂把这称为 " 把计算的可交换部分与对顺序敏感的部分分开 " ：可交换的部分交给  eﬀect
（任意顺序执⾏、任意顺序撤销，组件互不约束）；对顺序敏感的部分交给  coeﬀect （谁提
供、谁声明，由依赖关系强制顺序）。
5.5.3 范式定位：两端之间的第三极
论⽂专门⽤⼀节（ "Situating the Context Paradigm" ）论证这不是 " ⼜⼀个框架 " ，⽽是⼀个独
⽴的编程范式，定位在两⼤传统之间：
传统 代表 优点 代价
显式状态传递
（函数式）
State monad 、代
数效应
效果在类型中可
见、可等式推理
每个函数都要传递状态参数； monad 堆叠
样板爆炸
隐式变更（命
令式、 OOP ）
React useEffec
t、 Spring getBe
an
易⽤、⽆样板
eﬀect 靠调⽤顺序标识（藏在隐藏运⾏时状
态⾥）；依赖是全局注册表  + null 检查  + 类
型转换； "f() 改了什么依赖什么 " 要读实现才
能懂
Context 范式  = 函数式的可追踪性  + 命令式的易⽤性：所有  eﬀect 与依赖都通过显式   ctx 参
数中介，操作可归因；同时开发者不需要写  monad 样板，提供每个原⼦操作的逆、声明所需
依赖，其余全部⾃动：
Cordis 把 " 正确卸载、正确接线 " 从开发者要守的纪律，变成了定理。
" 对于可逆副作⽤，开发者提供每个原⼦操作的逆，任何复合的逆由组合⾃动得出，组件
的  teardown 是从它的  loading 推导出来的，⽽不是另写的；对于响应式余效应，组件只
声明所需依赖，运⾏时⾃动解析与重接线。两个⽅向上，原本依赖开发者纪律的正确性，
变成了范式的结构性质。 "
````

## PDF 第 22 页

[原页](RAW.pdf#page=22)

````text
5.6 动态组合演算与元理论：从局部保证到全局保证
5. 3–5.5 给出的是局部性质（单组件视⾓）。把它们带到整个交错系统，论⽂定义组件为三元
组   (d, p, e)，声明依赖  d 、声明提供  p 、带见证的  eﬀect 函数  e ； ﬁber 是⼀次实例化，携
带⾃⼰的⽣命周期状态、累加器与 " 已承诺视图 " （ committed view ，记录各依赖当时解析
到哪个提供⽅）。系统状态⾥的注册表是⼀棵  ﬁber 树，⽽  coeﬀect 上下⽂不是存储的，是
从所有活跃  ﬁber 的提供表联合推导出来的，每个键有且仅有⼀个提供⽅，由声明决定⽽
⾮由状态决定。
由此给出操作语义（激活、停⽤、重载、卸载、失败等迁移规则），并证明五条元理论性质：
性质 直觉 ⼯程意义
Preservation （保
型） 每个迁移保持系统良构 状态机不会⾛到⾮法状态
Temporal compos
ability （全局）
撤掉⼀个  ﬁber ，它的贡献归零，周围  ﬁber 原样
（ Corollary 62 ）
单个插件可热卸载，不影
响邻居
Spatial composa
bility （全局）
提供⽅离开前，依赖它的  ﬁber 先被停⽤（ Theore
m 63 ） 不需要⼿动编排卸载顺序
Progress （进展）
只要未达到  quiescent 就有规则可应⽤（⽆死锁）；
且⽬标视图翻转次数有限、步骤数有上界，必然终
⽌（ Theorem 66 ）
配置更新⼀定会收敛，不
会卡死
Conﬂuence （汇
合）
稳定状态只由最终配置决定，与加载、卸载的中间
顺序⽆关（ Theorem 73 ）
配置对账（ reconciliatio
n）可以增量、任意顺序
执⾏
其中  Progress 有个很实的前提：precedence 关系  ≺ （我提供你声明的键）必须⽆环，这正
是依赖图不能成环的数学表达，也是  Cordis 拒绝循环依赖的原因。⽽  Conﬂuence 是整篇论
⽂最直接的⼯程收益：因为它， Loader 可以对配置做增量对账⽽不⽤担⼼顺序，⽆论先装
谁、后卸谁，系统最后到达的状态都⼀样。
5.7 理论如何变成代码
论⽂的实现章节给出⼀张完整的理论→代码对照表（摘录）：
理论 实现
上下⽂  Γ∞ ctx
（⼀等上下⽂）
效应上下⽂  ∂Γ 、累
加器
ctx.effect
， ﬁber 的  accumulator
get(k)
  、  set(k, v)
ctx.get(key)
  、  ctx.set(key, value)
isolate(k, r)
  、  intercept
(k, ν)
ctx.isolate(key, realm)
  、  ctx.intercept(key, meta)
````

## PDF 第 23 页

[原页](RAW.pdf#page=23)

````text
理论 实现
组件实例（ ﬁber ）ﬁber ：uid  、  inject  、  provide  、  apply  、  parent  、  state  、  commit
ted  、  inertia（进⾏中迁移的句柄）
注册表 ctx.registry
恢复（ accumulato
r） fiber.dispose()
Loader 部分对应论⽂的声明式配置：
entry （配置条⽬） =  id（对账键）、url（ DSH 配置⾥写作   name）、isolate  、   interce
pt（注解）、config（绑定进   apply 的配置）、disabled（管理性关闭），与  DSH 的   cor
dis.yml  条⽬⼀⼀对应；
配置对账（ reconciliation ）：按字段差异选择最⼩操作，id/ url 变了重建，isolate 变
了重分配  realm ，intercept  原地更新（读取时才咨询），config  交给组件⾃⾏  diﬀ ，disa
bled  卸载、重载； group 条⽬的⼦列表按  id 做键控  diﬀ ，递归下探。对账之所以可以增
量、任意顺序，正是  5.6 的定理撑腰；
HMR 三阶段：①  依赖图不动点分类模块  accept/decline （被  accept 的导⼊  →  accept ；
所有导⼊都  decline →  decline ；陷⼊环的默认  decline ）→  ②  按  entry 的传递依赖树检测
过期条⽬  →  ③  事务性重载：备份模块缓存，逐个  dispose 旧  ﬁber 、挂载新  ﬁber ，任何⼀
步失败则恢复缓存、⽤旧模块重建，系统永远不会处于半重载状态。注意： Cordis 的
HMR 不需要开发者标注  accept 边界（对⽐  Webpack/Vite ），因为  ﬁber 本⾝就界定了组
件全部效果的边界，替换⼀个组件  = ⼀次  ﬁber 操作。
论⽂的讨论章节还展开了⼀些⼯程延伸：
系统边界（ system boundary ）：不是所有东西都可逆，可独占修改、可恢复的位置 " 在边
界内 " （⽂件、私有内存），会被外部程序读写的位置 " 在边界外 " （操作视为不可追踪）。ct
x.intercept  可以把⼀个外部位置  reify 成可逆操作：把它包装成⼀组⾃带逆的受限操作，边
界就向内移动。移动边界本⾝是权衡：换取可恢复性，付出每次访问的开销。
补偿（ compensation ）：对真正⽆法逆转的 " 发射 " （邮件已发出、款项已扣），⽤应⽤级
补偿动作（删⽂件、退款）替代，且补偿按  LIFO 顺序组合，删除的逆是再创建，退款的
逆是再扣款。
服务多路复⽤（ service multiplexing ）：独占绑定（⼀个接⼝同时只绑⼀个实现，切换要
短暂扰动所有消费⽅） vs 服务代理（ service broker ），⼀个常驻  broker 注⼊给提供⽅和
消费⽅，多个提供⽅共存、 broker 分发请求。消费⽅永远看到同⼀个依赖，提供⽅热更新
不触发任何重载。由此获得三个能⼒：负载均衡、滚动更新、跨进程调⽤。这正是  DSH
的   llm  适配器注册表与  pi-ai 多提供⽅机制的论⽂原型。
5.8 与既有系统的对⽐：特点的证明
把  Cordis 放进坐标⾥，它的位置才清晰。沿着 " 时间维（卸载）→  空间维（依赖） " 两个轴，
逐个对照⼋类系统。
````

## PDF 第 24 页

[原页](RAW.pdf#page=24)

````text
传统  DI 容器（ Spring 、 NestJS 、 InversifyJS ）
模型：容器负责创建与绑定（bind、getBean），对象图在启动时装配。
时间维：getBean  拿到的服务没有⽣命周期管理，容器不知道、也不负责 " 服务下线后谁
清理它的副作⽤ " 。 NestJS 的   OnModuleDestroy  是⼿动钩⼦，⽽且把 " 创建效果 " 与 " 清理
效果 " 写在两处，违背关注点局部性（论⽂在  VS Code 的   deactivate  上批评过同样的问
题）。
空间维：依赖是运⾏时查找，getBean 的返回值往往需要调⽤⽅⾃⼰断⾔类型（ Java ⾥
是类型转换，很多框架⾥⼲脆是   any）；依赖关系隐式、散落在代码各处。
差距：绑定即永久。容器的隐含假设是 " ⼀旦装配，对象图不再变化 " ，没有 " 服务消失  →
依赖⽅⾃动重建 " 的概念，与  Cordis 的假设（服务可随时出现、可随时消失）正好相反。
React Hooks
模型：useEffect(fn, deps)  把副作⽤挂到组件实例上。
时间维：清理函数是有的（ return 的  cleanup ），但  eﬀect 的 " ⽬标 " 是隐式的，它靠调⽤顺
序在隐藏的运⾏时状态⾥登记，函数组件卸载时按注册顺序清理。这套机制绑死在  React
的渲染模型上，⽆法推⼴为通⽤组件的装卸语义。
空间维：依赖数组是静态声明，deps  只在渲染时做值⽐较，没有运⾏时依赖解析，也没
有 " 依赖提供⽅被替换  →  依赖⽅⾃动重载 " 。
差距： React 的  eﬀect 是 " 组件内的回调 " ， Cordis 的  eﬀect 是 " 上下⽂上的可逆变换 " 。前
者服务于  UI 渲染⽣命周期，后者服务于任意组件的装卸。
OSGi
模型：模块化  Java 的经典⽅案，服务注册表  + provider 、 consumer ，是所有对照⾥最接
近  Cordis 的先驱。
时间维： bundle （模块）可以动态安装与卸载，服务注册、注销是动态的。
空间维： consumer 通过服务注册表绑定服务；但服务消失时， consumer 不会⾃动重连
或重载，它拿到的是已失效的引⽤，需要⾃⼰处理。
差距： OSGi 有 " 动态 " 的机制，却没有 " 响应式 " 的语义。 Cordis 的  reactive coeﬀects 把 " 依
赖变化  →  分类通知  →  激活、停⽤  →  ⾃动重载 " 做成了框架级⾏为，这正是论⽂  spatial
composability 定理的兑现。
VS Code 扩展宿主
模型：扩展在共享进程（ extension host ）⾥   activate，通过固定的扩展点
（ commands 、 views ）贡献能⼒。
时间维：⽆法在运⾏时卸载单个扩展，禁⽤、卸载必须重启整个宿主（实测数据见  5.1 ）；
deactivate 钩⼦只在进程退出时调⽤。
空间维：extensionDependencies  ⼏乎没⼈⽤；扩展间交互靠   vscode.extensions.getExtensio
n(...).exports，返回值是未检查的   any。
````

## PDF 第 25 页

[原页](RAW.pdf#page=25)

````text
差距： VS Code 的问题不是 " 实现得不好 " ，⽽是 " 架构上没有这条路径 " ，插件向固定扩展
点贡献能⼒，⽽不是向其他插件声明依赖。
微服务、容器（粗粒度替代）
模型：把时间可组合性下放给进程（重启即恢复），把空间可组合性下放给编排器（ K8s
服务发现）。
代价：每次重启丢弃全部进程内状态（缓存、连接、半成品计算），重建要花秒级到分钟
级；跨地址空间的依赖只能⽤⽹络表达，⽆法⽤函数调⽤；编排器也⽆法表达共享同⼀地
址空间的组件间依赖。
差距：粒度错配。现代系统在进程内、组件级进⾏组合，⽽容器提供的组合粒度在进程
外。
monadic eﬀect （ ZIO 、 Eﬀect-TS 、 fp-ts ）
模型：把副作⽤编码进类型系统，ZIO[R, E, A]  、   Effect<A, E, R>，其中   R  就是 " 这个
计算需要什么服务 " 。
时间维：追踪是monad 嵌⼊换来的，程序必须整个写进  eﬀect 类型，才能获得追踪；
Cordis 则是对普通宿主代码的覆盖式追踪（ctx.effect 包住任意代码）。
空间维：需求（R）由解释器（ interpreter ）在运⾏时装配；但服务被撤⾛时，已经通过
它执⾏的操作留在原地，没有逆，没有恢复。
差距：这正是论⽂  5.3 / 5.4 的对照： Cordis 把 " 追踪 " 从类型嵌⼊换成运⾏时逆追踪，
把 " 需求装配 " 从⼀次性解释换成持续重解析。
代数效应（ Eﬀekt 、 Koka ）
模型： eﬀect 操作对类型系统可见，⼀个操作可以有不同的  handler 语义。
时间维、空间维：静态类型层纪律，能⼒默认是  second-class 、限于词法作⽤域（ Eﬀekt
通过  boxing 提升为⼀等）。
差距：⽬的不同。代数效应让  eﬀect 可见是为了 " 模块化解释 " （⼀个操作多种语义）；
Cordis 让  eﬀect 可见是为了 " 追踪与逆转 " （每个变换配对逆）。论⽂  7.1 节明确点出了这
⼀区别。
Webpack / Vite HMR
模型：开发期的模块热替换。
时间维：需要开发者标注  accept 边界（module.hot.accept），漏标就退化为整页刷新，替
换边界由⼈⼯声明。
差距： Cordis 的  HMR 不需要  accept ， ﬁber 本⾝就界定了组件的全部效果边界，替换⼀
个组件  = ⼀次  ﬁber 操作（ dispose 旧的  + 挂载新的），且是事务性的（失败回滚，绝不进
⼊半重载状态）。
收束：⼀张表
````

## PDF 第 26 页

[原页](RAW.pdf#page=26)

````text
系统 时间维（卸载）空间维（依赖）差距
传统  DI （ Spri
ng ）
⽆：getBean  拿到的服务
没有⽣命周期管理
全局注册表，null  检查
+ 类型转换
绑定即永久；依赖关系
隐式、散落
React useEf
fect
eﬀect 可清理，但靠调⽤顺
序标识，⽬标隐式
hooks 依赖数组与  eﬀect
分离
卸载语义不随组件树⾃
动成⽴
OSGi 服务可卸载，但消费⽅不⾃
动重连
服务模型（ provider 、 con
sumer ）
有动态机制，⽆响应式
语义
VS Code ⽆法热卸载： 87% 热门扩
展需重启宿主
extensionDependenci
es
  ⼏乎没⼈⽤，export
s  是  any
只能整宿主重启
微服务、容器进程粒度重启，丢弃全部状
态
编排器粒度，⽆法表达共
享地址空间的依赖粒度错配
ZIO 、 Eﬀect-T
S
追踪靠  monad 嵌⼊，程序
必须写进  eﬀect 类型
需求靠解释器；服务撤⾛
时已执⾏的操作留在原地
不能对普通宿主代码做
覆盖式追踪
代数效应（ Eﬀ
ekt ）
静态类型层纪律，能⼒限于
词法作⽤域 静态解析
⽬的不同： Eﬀekt 为解
释， Cordis 为追踪与逆
转
Webpack 、 Vit
e HMR
需要开发者标注  accept  边
界 — 替换边界靠⼈⼯声明
Cordis
每个变换携带逆，恢复是定
理； HMR 不需要  accept 边
界
依赖是类型化表，变化被
分类通知，⾃动重连是定
理
时间与空间两维同时由
运⾏时承担
从  Agent 运⾏时的⾓度看，这个对⽐更直观：
需求 传统  DI 容器 Cordis
服务被替换、卸载后⾃动清理不负责，需⼿写或泄漏eﬀect ⾃动回滚
依赖提供⽅热替换后⾃动重建 做不到 依赖⽅⾃动卸载重载
配置决定组合，改配置即热重载配置通常启动时⼀次性cordis.yml
  即插件树
服务运⾏时消失 视为异常 视为常态，优雅降级
有序决策链（权限→审批→超时→执⾏）需⾃⾏搭建  middleware waterfall 事件原⽣⽀持
5.9 结论：点名⾃进化  Agent
论⽂结论明确把  self-evolving agent harnesses （⾃进化  Agent 运⾏时）  列为未来验证⽅
向： AI 在少有⼈监督的情况下持续⽣成并替换⾃⼰的组件，需要 " 快速替换下的完整恢复保
证 " （时间维）与 " 频繁拓扑变化下的依赖协调保证 " （空间维）。论⽂写作时这还只是展望，
⽽  DSH 的   cordis_define  、   cordis_run  正是这⼀⽅向的具体实现： Agent 现场⽣成动态插
件、沙箱运⾏、随时卸载，恰好是在压测  5.6 的时间与空间定理。
````

## PDF 第 27 页

[原页](RAW.pdf#page=27)

````text
理论在前，实践随后。 Cordis 最值得关注的地⽅不是它写得不错，⽽是它把 " 安全地动态装卸
组件 " 从纪律变成了定理 —— ⽽这恰恰是⾃进化软件唯⼀靠得住的地基。
6. ⽣态： Cordis 不⽌有  Koishi
6.1 Koishi ：第⼀个实战平台
论⽂的案例研究就是  Koishi ，并给出数据：四年间积累了  4000+ 社区插件。从  npm registry
核实了当前数字：
@koishijs 官⽅  scope ： 155 个包，其中插件  112 个、各平台适配器  19 个（ QQ 、
Discord 、 Telegram 、 Lark…… ）；
社区   koishi-plugin-\*  前缀：约  3951 个包。
只看插件数量，还低估了它的规模。另⼀组  2026 年  8 ⽉实测的数据：
npm 下载量：koishi  近⼀年约  34 万次下载，cordis  近⼀年约  51 万次（周均约  1 万）；
GitHub ：koishijs/koishi  约  5800 star ，cordiverse/cordis  约  2400 star ；
社区规模：官⽅  FAQ 称有数千位活跃搭建者，其中许多⼈的单个机器⼈就覆盖数万活跃⽤
户；
官⽅认可： Koishi 以组织⾝份出现在中科院软件所主办的 " 开源之夏 " （ Open Source
Promotion Plan ） 2025 的项⽬列表中。
论⽂还指出了⼀个设计上的验证： Koishi 的  Web 控制台是第⼆个独⽴的  Cordis 应⽤（浏览
器⾥运⾏着另⼀棵插件树）；适配器、数据库驱动与功能插件之间形成了真实的依赖拓扑，切
换存储后端或重连适配器时，只有依赖真正变化的那部分插件会被重新激活。这验证了 " 跨独
⽴作者协作 " 的场景：插件与其依赖通常由不同作者编写，双⽅只通过服务契约（ coeﬀect ）协
调。
````

## PDF 第 28 页

[原页](RAW.pdf#page=28)

````text
⼀个版本事实：Koishi ⽬前仍使⽤  Cordis 3.x（@koishijs/core  依赖   cordis: ^3.18.1），⽽论
⽂与  DSH 使⽤的是  4.x 。核⼼组合模型两代共享，但  4.x 重构了  eﬀect 、 coeﬀect 语义与
Loader 。
⼀个在  Koishi 圈写过⼏年插件的开发者视⾓：这套⽣态⾥的插件很少直接互相调⽤，⼤家靠
服务契约（inject）和事件协作。写插件的⼈通常只关⼼⾃⼰声明了什么依赖、注册了什么效
果，谁先启动、谁依赖谁、谁负责清理，是  Cordis 的事，不是作者的事。
6.2 @cordisjs：独⽴的通⽤⽣态
Koishi 之外， Cordis 还维持着⼀个独⽴的官⽅⽣态，@cordisjs scope 下现有  101 个包，覆
盖了⼀个通⽤应⽤框架所需的全部组件：
核⼼机制：loader、plugin-loader、plugin-include、plugin-hmr、plugin-group、plug
in-config、schema、timer、logger；
服务端：plugin-server（含   -acl、-proxy、-static、-temp、-webui）、plugin-htt
p；
数据：plugin-database  及  sqlite 、 mysql 、 postgres 、 mongo 、 memory 驱动；
业务基础设施：mail、sms（多家供应商）、sso（⼗⼏家登录⽅式）、webui  控制台、
market 插件市场、manager、insight（插件依赖关系图）、cli、client、component
s 、create-cordis（脚⼿架）。
这些包的存在说明： Cordis 不是 " 为  Koishi 定制的内核 " ，⽽是⼀个真正通⽤的应⽤框架，
Koishi 与  DSH 只是它的两个实例，⼀个在  IM 领域，⼀个在  Agent 领域。
6.3 ⽣态背后的⼏件事
1. ⼩且可审计：核⼼⼏千⾏  TypeScript ， DSH 整体  vendor 进仓库并做了约  18 处本地修改
（⽣命周期加固、配置加载事务化、表达式延迟求值等）。不依赖外部注册表、不怕上游
breaking change 、可按⾃⾝使⽤模式调优；
2. 实战验证： Cordis 在  Koishi ⽣态经历了上千插件的并发运⾏考验，插件框架最难的 " 注
册、注销边⾓问题 " ，已经被长期实战覆盖；
3. TypeScript-ﬁrst：声明合并让扩展点全链路类型安全； DSH 甚⾄从这些声明⾃动⽣成供
模型阅读的  API ⽬录，类型系统本⾝变成了  Agent 的操作⼿册。
7. 结语：⼼脏、引擎与定理
Cordis 是  Koishi 的⼼，⼏千⾏  TypeScript ，把 " 怎么安全地装卸组件 " 从开发者的⾃觉变成了
框架级承诺 ——ctx.effect  注册即回滚，inject  声明即等待，配置⽂件即应⽤。 DSH 把同⼀
个框架搬进  Agent 运⾏时，⼯具、模型、存储、界⾯全是插件，配置由  patch 层叠加，连  AI
都能通过   cordis_inspect  、   cordis_run  检查并改装⾃⼰运⾏的系统。论⽂⽤  88 页把这两件
事形式化，给出证明：卸载必然恢复、依赖⾃动重连、配置对账必然收敛。
Cordis 最值得关注的地⽅，不是它写得不错，⽽是它把 " 安全地动态装卸组件 " 从开发者纪律变
````

## PDF 第 29 页

[原页](RAW.pdf#page=29)

````text
成了定理 —— ⽽这恰恰是⾃进化软件唯⼀靠得住的地基。
如果还想继续深⼊，可以按这个顺序：
1. DSH 官⽅教程（七章，每个例⼦可运⾏）：cordis-tutorial
2. DSH 官⽅⼊门（五个核⼼概念浓缩版）：cordis-primer.zh.md
3. 上游仓库：cordiverse/cordis
4. 论⽂：A Programming Paradigm for Spatiotemporal Composability
5. Koishi ⽣态：koishi.chat
6. DeepSeek Harness ：deepseek-ai/deepseek-harness
参考资料
Cordis ⼊门（ DSH 官⽅⽂档）
Cordis 教程（ DSH 官⽅⽂档，七章）
cordiverse/paper （论⽂全⽂与  README ）
cordis - npm（版本时间线）
cordiverse/cordis （上游仓库）
Koishi 常见问题（ Koishi 由  Shigma 创⽴， 2020 年  1 ⽉发布⾸个正式版）
为什么⽤  Cordis 做  AI Agent 运⾏时：从  QQ 机器⼈框架到  DeepSeek Harness
Shigma 专访（腾讯媒体研究院， 2023-11-28 ）：QQ 机器⼈开发创业青年 Shigma 专访：⼈
类未来会被 AI 取代吗？； B 站搬运：BV1AQ4y157S8
影响⼒数据（ 2026-08 实测）： koishi 、 cordis 近⼀年  npm 下载量约  34 万、 51 万次
（ api.npmjs.org ）；koishijs/koishi  约  5800 star 、cordiverse/cordis  约  2400 star
（ github.com ）；社区规模与 " 单机器⼈覆盖数万活跃⽤户 " 见  Koishi 常见问题； Koishi 在
开源之夏  2025 项⽬列表中
⽂中截图（ 2026-08 ）： Shigma 的  GitHub 主页、Koishi 插件市场、 DeepSeek Harness
设置页插件清单；社区插件截图（ dsh-visualize 、 dsh-task-status 、 dsh-stock-market 、
dsh-web-ui ）均取⾃各⾃仓库  README ；⽰意图为本⽂⾃制  SVG
社区插件⽣态：awesome-dsh-plugin（ GitHub  #dsh-plugin， 2026-08 收录  174 个插件）
⽣态数据（ 2026-08 实测）：@koishijs scope 155 包、koishi-plugin-* 前缀  3951 包、
@cordisjs scope 101 包（ npm registry 枚举）；@koishijs/core 4.18.11 依赖   cordis: ^3.1
8.1
````

## PDF 第 30 页

[原页](RAW.pdf#page=30)

````text
阅读 2 . 9 万
腾讯技术官⽅号。腾讯技术创新、前沿领域发布解读平台。
687 篇原创内容
腾讯技术⼯程
公众号
留⾔
还没有留⾔，来写⾸评
写留⾔
````

## PDF 第 31 页

[原页](RAW.pdf#page=31)

````text
````

## 采集与转写核验记录（非原文）

以下说明由本次核验添加；上方逐页文本保持文本层原样，图片与布局以PDF为准。

- PDF物理页 30,31：PDF p.31为空白尾页；p.30为公众号账号与留言入口。
