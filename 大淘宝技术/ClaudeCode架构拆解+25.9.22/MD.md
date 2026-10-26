# Claude Code 深度拆解：一个顶级AI编程工具的核心架构

来源：[RAW.pdf](RAW.pdf)，capture-001。

这是PDF文本层按物理页码转写，不是AI总结。图片未嵌入；图内文字、截图、公式、表格及代码排版可能未提取或不可靠；源PDF中存在的右侧裁切不补写。实际复核范围详见META.json。

## PDF物理页 1

Claude Code 深度拆解：⼀ 个 顶级      AI编程⼯具的 核⼼架构

茂道 ⼤淘宝技术   2025年9⽉22⽇ 01:47浙江  32⼈













  ⽂章深度拆解了Anthropic开发的终端AI编程⼯具Clau de Code，包括其以交互层、执
  ⾏层、核⼼引擎为核⼼的系统架构，提交命令到渲染结果的执⾏流程，以及交互层的输
  ⼊处理与渲染、核⼼引擎的消息与查询管理、⼯具系统、上下⽂管理（含LRU 缓存等策
  略）和安全机制，还分享了Binary Feedback测试机制、M  CP⼯具分层管理等技术启
  发；同时介绍了⼼流团队基于Gemini CLI改造、融合Clau de Code特性的iFlow CLI
  2.0，包括其安装⽅式、功能特点（如多运⾏模式、Su bAgent功能等）、开放市场资
  源，以及CLI⼯具在项⽬开发、⽹站制作、D eepResearch等场景的应⽤，还给出了⻄欧
  亲⼦⾃驾游规划案例。






                      C  laude  C  ode介绍



Clau deCode是由Anthropic开发的全新终端AI编程⼯具，旨在通过⾃然语⾔指令帮助开发者
⾼效率地完成代码编写、调试和项⽬管理任务。它直接集成在开发者的⼯作环境（如终端）
中，⽆需依赖额外服务器或复杂配置即可运⾏。




在实际的使⽤过程中，Clau de Code是⼀个⽐较通⽤的智能体，他输出的代码也⽐cu rsor简
练很多，更像是⼀个熟悉整个项⽬的⾼级程序员，研究和学习这个框架对于开发⾃⼰的Agent
⾄关重要，本篇⽂章会详细介绍Clau de Code的设计模式和核⼼代码。





                         详细介绍



▐  2.1系统架构

## PDF物理页 2

▐  2.2执⾏流程

## PDF物理页 3

▐  2.3交互层




交互层是⽤户与 Clau de Code 的接触点，通常包括：
   REPL 界⾯：提供命令⾏交互体验；

   输⼊处理器：解析⽤户指令，⽀持多种输⼊模式（⾃然语⾔、命令、代码等）；
   输出渲染器：格式化并展示 AI 响应和⼯具执⾏结果；
在 Clau deX 中，这⼀层主要由REPL.tsx和PromptInpu t.tsx等组件实现，它们负责接收⽤户
输⼊并展示结果。




   2 .3 .1输⼊逻辑处理



输⼊逻辑处理


 1  function processUserInput(input: string, mode: InputMode): UserMessage
 2    if (input.startsWith('/')) {
 3      return handleSlashCommand(input);
 4    } elseif (input.startsWith('!')) {
 5      return handleBashCommand(input.slice(1));
 6    } else {
 7      return createUserMessage(input);
 8    }
 9  }






   2 .3 .2 渲染




   阶段
   ⼯具调⽤阶段（Assistant侧）：显示⼯具名称、参数和执⾏状态；
   ⼯具结果阶段（User侧）：显示执⾏结果；




   组件
   AssistantToolU seM  essage:渲染助⼿调⽤⼯具时的消息；
    显示⼯具名称（通过 tool.u serFacingName()）；
    显示参数（通过 tool.renderToolU seM  essage()）；
    使⽤ ToolU seLoader 显示执⾏状态动画；
   U serToolSu ccessM  essage:
    渲染⼯具执⾏成功后的结果；
    调⽤ tool.renderToolResu ltM  essage() 渲染具体内容；

## PDF物理页 4

   ⼯具接⼝定义
    u serFacingName() 显示给⽤户的⼯具名称；
    renderToolU seM  essage(inpu t, options) 渲染⼯具参数；
    renderToolResu ltM  essage(ou tpu t, options)渲染⼯具结果；
    renderToolU seRejectedM  essage() 渲染拒绝消息；




   U I渲染特性
    使⽤ Ink 框架的 Box 和 Text 组件构建终端U I；
    ⽀持主题系统（通过 getTheme()）；
    响应式布局（flexD irection, ju stifyContent）；
    详细/简洁模式切换（verbose 参数）；
    执⾏成本和时间显示（Cost 组件）；



▐  2.4核⼼引擎




核⼼引擎是 Clau de Code 的"⼤脑"，负责协调各个组件的⼯作：
   消息系统：管理⽤户输⼊、AI 响应和⼯具结果的消息流；
   查询引擎：与 AI 模型交互，发送请求并处理响应；
   ⼯具调度器：协调⼯具的调⽤和结果处理；
在 Clau deX 中，  qu ery.ts是核⼼引擎的关键组件，它实现了与 AI 模型交互的逻辑：

q  u e ry .ts



   1 // 简化的查询逻辑
  2  async function* query(
  3    messages: Message[],
  4    systemPrompt: string ,
  5    context: Context,
  6    canUseTool: CanUseToolFn,
  7    toolUseContext: ToolUseContext,
  8  ): AsyncGenerator<Message> {
  9    ## 1. 初始化⼤模型     prompt
  10   const fullSystemPrompt = formatSystemPromptWithContext(systemPrompt,
  11
  12   ## 2. 获取⼤模型返回
  13   const result =  await queryWithBinaryFeedback(
  14     toolUseContext,
  15     getAssistantResponse,
  16     getBinaryFeedbackResponse,
  17   )
  18

## PDF物理页 5

 19    ## 3. 处理模型返回的⼯具请求
 20    const toolUseMessages = assistantMessage.message.content.filter(
 21      _ => _.type === 'tool_use',
 22    )
 23
 24    ## 4. 并⾏ /串⾏执⾏⼯具
 25    if (
 26      toolUseMessages.every(msg =>
 27        toolUseContext.options.tools.find(t => t.name === msg.name)?.isR
 28      )
 29    ){
 30      for await (const message of runToolsConcurrently
 31    } else{
 32      for await (const message of runToolsSerially
 33    }
 34
 35    ## 5. 处理后续交互
 36    yield* await query()
 37  }




▐  2.5⼯具



⼯具系统是 Clau de Code 的"⼿脚"，使其能够与外部环境交互：
  ⽂件⼯具：读取、写⼊、搜索⽂件；
  执⾏⼯具：运⾏ shell 命令、执⾏代码；
  分析⼯具：代码分析、依赖检查等；
  元⼯具：复合⼯具，可以执⾏更复杂的任务；



每个⼯具都遵循统⼀的接⼝，包括名称、描述、参数模式和执⾏逻辑：



 1  interface Tool {
 2    name: string;
 3    description: string;
 4    inputSchema: z.ZodType;
 5    execute(params: any): Promise<ToolResult>;
 6  }



⼯具也是整个Clau de Code的核⼼资产，他这个cli效果这么好除了是因为强⼤的模型，也是
因为有很强⼤的⼯具，例如有⼀个特别强⼤的bash tool的⼯具，可以调⽤shell⾥⾯的所有命
令，也包含agent tool，可以发挥更强⼤的能⼒。我们会在后续的⽂章中对⼯具进⾏单独的分
析。

## PDF物理页 6

▐  2.6上下⽂管理




上下⽂管理是 Clau de Code 的"记忆"，负责收集和组织代码相关信息：
   项⽬结构：⽬录和⽂件结构
   代码内容：关键⽂件的内容
   版本控制：Git 历史和状态
   配置信息：项⽬配置和依赖




上下⽂管理的挑战在于如何在有限的上下⽂窗⼝内提供最相关的信息：
   LRU 缓存机制：对⽂件编码、⾏尾类型等信息实现缓存，减少重复操作。
⽂件缓存


  1  const fileEncodingCache = new LRUCache  <string,  BufferEncoding >({
  2    fetchMethod : path => detectFileEncodingDirect  (path),
  3    ttl: 5 * 60  * 1000,
  4    ttlAutopurge:  false,
  5    max: 1000,
  6  })
  7
  8  const lineEndingCache =  new  LRUCache<string , LineEndingType>({
  9    fetchMethod : path => detectLineEndingsDirect  (path),
 10    ttl: 5 * 60  * 1000,
  11   ttlAutopurge:  false,
 12    max: 1000,
 13  })



   按需加载策略：不会⼀次性加载整个代码库，⽽是根据查询需要智能加载相关⽂件 。

GlobTool.tsx


   1 async * call({ pattern, path }, { abortController }  ){
  2      const start =  Date. now()
  3      const { files, truncated } = await    glob(
  4        pattern,
  5        path ?? getCwd(),
  6        {  limit: 100, offset : 0 },
  7        abortController.signal,
  8      )
  9      const output:  Output = {
  10       filenames : files,
  11       durationMs : Date. now() - start,

## PDF物理页 7

  12       numFiles: files. length,
 13        truncated,
 14      }
  15     yield {
 16        type:  'result',
  17       resultForAssistant:  this .renderResultForAssistant(output),
 18        data: output,
 19      }
 20    },



   结果截断处理：对⼤量搜索结果实现智能截断，避免上下⽂溢出，同时提供清晰的截断提
   示 。

lsTool.tsx


  1 const MAX_LINES  = 4
 2  const MAX_FILES  = 1000
 3  const TRUNCATED_MESSAGE  = `There are more than ${MAX_FILES} files in th



   拼装上下⽂

上下⽂拼装


  1 async function getContext(): Context   {
 2    return {
 3      directoryStructure:  await getDirectoryStructure  (),
 4      gitStatus : await getGitStatus(),
 5      codeStyle : await getCodeStyle(),
 6      // 其他上下⽂    ...
 7    };
 8  }




▐  2.7安全




安全与权限是 Clau de Code 的"护栏"，确保⼯具使⽤的安全性：
   权限验证：⼯具执⾏前的权限检查；
   ⽤户确认：关键操作的⽤户确认机制。使⽤最⼩权限原则，只向⽤户索要完成任务的最⼩
   权限；
   安全边界：⽂件操作和命令执⾏的限制；
permission.ts


   1 exportconst hasPermissionsToUseTool

## PDF物理页 8

   2    // 跳过
   3    if (context.options.    dangerouslySkipPermissions) {
   4      return { result   : true }
   5    }
   6
   7    if (context.abortController.     signal.  aborted) {
   8      thrownew AbortError    ()
   9    }
  10
  11    // 允许每个⼯具单独配置，由⼯具声明安全性，因为                      cc的⼯具都是⾃⼰实现的，他可以⾃⼰保
  12    try {
  13      if (!tool.  needsPermissions   (input   as never )) {
  14        return   {  result:  true  }
  15      }
  16    } catch (e) {
  17      logError  (`Error checking permissions:       ${e}`)
  18      return { result   : false  , message:   'Error checking permissions'      }
  19    }
 20
  21  }






                                       ⼀  些启发



▐  3.1⽤于程序员测试          prompt  的  Binary Feedback   机制




q  u e ry .ts



   1 async   function  queryWithBinaryFeedback(
  2    toolUseContext: ToolUseContext,
  3    getAssistantResponse: () =>       Promise <AssistantMessage>,
  4    getBinaryFeedbackResponse?: (
  5      m1: AssistantMessage,
  6      m2: AssistantMessage,
   7   ) =>   Promise <BinaryFeedbackResult>,
  8  ):  Promise < BinaryFeedbackResult> {
  9     if (
  10     process.env   .USER_TYPE   !==  'ant' ||
  11     !getBinaryFeedbackResponse ||
  12     !(  await  shouldUseBinaryFeedback())
  13   ):
 14     const  [m1, m2] = await    Promise.  all([

## PDF物理页 9

 15     getAssistantResponse(),
 16     getAssistantResponse(),
 17   ])
 18 }



使⽤完全⼀模⼀样的请求两次，可能是为了观察同样的输⼊模型会不会给出两个输出，如果ai
返回了两个答案，就说明模型对于这次请求是犹豫的，考虑不清楚的，需要让⽤户去做选择。




这⾥对于输出的检测不是检测⽂本，⽽是去检测⽣成的tool u se是不是相同的。结构化数据输
出的稳定性要远远⼤于⽂本输出的稳定性。如果没有tool u se才会去⽐较⽂本。




同时看到这个代码只在程序员⾃⼰测试的时候才会⽣效，说明这样的测试逻辑对于开发⾃⼰的
agent还是⽐较有⽤的。出现这种情况就说明你需要去提⾼⾃⼰的prompt质量了。




▐  3.2MCP⼯具



整个Clau de Code⾃身只维护了⼀个tengu _mcp_server，同时⽀持⽤户添加M  CP Server，

Clau de Code通过三级分层的结构，来管理⽤户的M  CP ⼯具：
  global：全局配置的通⽤的M  CP
  M  CPrc：配置⽂件，可以共享
  project：项⽬级别，就是当前的代码库可以单独配置
下层结构的M  CP配置的可以覆盖上层的M  CP配置。


添加M  CP Server


  1  export function addMcpServer(
  2    name: McpName,
  3    server: McpServerConfig,
  4    scope: ConfigScope = 'project',
  5  ): void {
  6    if (scope === 'mcprc') {
  7      if (process.env.NODE_ENV === 'test') {
  8        addMcprcServerForTesting(name, server)
  9      } else {
 10        const mcprcPath = join(getCwd(), '.mcprc')
  11       let mcprcConfig: Record<string, McpServerConfig> = {}
 12
 13        // Read existing config if present
 14        if (existsSync(mcprcPath)) {
 15          try {

## PDF物理页 10

  16            const    mcprcContent =    readFileSync(mcprcPath, 'utf-8')
  17            const    existingConfig = safeParseJSON      (mcprcContent)
  18            if   (existingConfig && typeof      existingConfig === 'object') {
  19              mcprcConfig = existingConfig as Record          <string , McpServerCo
  20            }
  21          } catch    {
  22            // If we can't read/parse, start with empty config
  23          }
  24        }
  25
  26        // Add the server
  27        mcprcConfig[name] = server
  28
  29        // Write back to .mcprc
  30        try {
  31           writeFileSync(mcprcPath, JSON      .stringify(mcprcConfig,      null , 2),
  32        }  catch (error) {
  33          thrownew Error    (`Failed to write to .mcprc: ${error}`        )
  34        }
  35      }
  36    } elseif (scope ===     'global'  ) {
  37       const config =    getGlobalConfig  ()
  38       if (!config.mcpServers    ) {
  39        config.mcpServers     = {}
  40      }
  41      config.  mcpServers[name] = server
  42       saveGlobalConfig(config)
  43    }  else {
 44        const config =    getCurrentProjectConfig    ()
  45       if (!config.mcpServers    ) {
  46        config.mcpServers     = {}
  47      }
  48      config.  mcpServers[name] = server
  49       saveCurrentProjectConfig(config)
  50    }
  51  }





如何获取到多个M  CP Server的⼯具，请求所有的M  CP Server，获取到所有的tools，将
tools聚合，发送给⼤模型。

getM  CPTools


   1  exportconst getMCPTools = memoize(async        (): Promise  <Tool[]> => {
  2     const toolsList =    await requestAll<
  3       ListToolsResult,

## PDF物理页 11

  4      typeof ListToolsResultSchema
  5    >(
  6      {
  7        method : 'tools/list',
  8      },
  9      ListToolsResultSchema,
 10      'tools',
  11   )




▐  3.3通过  AI 来检测安全



利⽤AI做安全辅助。例如判断命令是否有被注⼊的可能性。
判断命令是否有被注⼊



   1 exportconst getCommandSubcommandPrefix = memoize(
  2    async  (
  3      command: string  ,
  4      abortSignal: AbortSignal,
  5    ): Promise<CommandSubcommandPrefixResult |      null > => {
  6       const subcommands = splitCommand(command)
   7
  8       ## 获取命令前缀来观察是否在安全执⾏列表
  9       const [fullCommandPrefix, ...subcommandPrefixesResults] = await Pr
  10       [
  11         getCommandPrefix(command, abortSignal),
  12         ...subcommands.map(   async subcommand => ({
  13           subcommand,
  14           prefix: await    getCommandPrefix(subcommand, abortSignal),
  15         })),
  16       ],
  17     )
  18
  19   },
 20    command => command, // memoize by command only
  21 )




▐  3.4上下⽂压缩处理



核⼼功能：清空对话历史但保留上下⽂摘要，解决了⻓对话导致的上下⽂窗⼝问题。

## PDF物理页 12

技术亮点：
1. 智能摘要⽣成：使⽤Sonnet模型⽣成对话摘要，保留关键信息供后续使⽤；
2. Fork机制应⽤：利⽤setForkConvoWithM  essagesOnTheNextRender创建新的对话分
  ⽀，摘要作为新对话的起点；
3. Token使⽤优化：将摘要的token使⽤量设为0，避免触发上下⽂窗⼝警告；
4. 缓存清理：清理getContext和getCodeStyle缓存，确保新对话环境⼲净；



核⼼代码流程：
1. 获取当前对话历史
2. 构造摘要请求并调⽤Sonnet模型
3. 提取并验证摘要内容
4. 清屏、清空消息历史
5. 创建包含摘要的新对话分⽀



▐  3.5简单任务交给⼩模型



Clau de内部会有好⼏个模型实例，如果是只判断对错或者是⼀些简单的任务，会交给haiku  模
型。
qu eryH  aiku



   1 ## 创建标题任务
  2  async function  generateTitle(description: string):  Promise<string> {
  3    const response = await queryHaiku({
  4      systemPrompt: [
  5        'Generate a concise issue title (max 80 chars) that captures the
  6      ],
  7      userPrompt: description,
  8    })
  9    const title =
  10     response.message.content[ 0]?.type === 'text'
  11       ? response.message.content[ 0].text
  12       : 'Bug Report'
  13   if (title.startsWith(API_ERROR_MESSAGE_PREFIX)) {
  14     return `Bug Report:  ${description.slice( 0, 60)}${description.lengt
  15   }
  16   return title
  17 }
  18
  19 ## 确认前缀的任务
 20  const getCommandPrefix = memoize(
  21   async (
 22      command: string,

## PDF物理页 13

 23      abortSignal: AbortSignal,
 24    ): Promise<CommandPrefixResult | null> => {
 25      const response = await queryHaiku({
 26        systemPrompt: [
 27          `Your task is to process Bash commands that an AI coding agent
 28
 29  This policy spec defines how to determine the prefix of a Bash command
 30        ],
 31
 32  Examples:
 33  - cat foo.txt => cat
 34  - cd src => cd
 35  - cd path/to/files/ => cd
 36  - find ./src -type f -name "*.ts" => find
 37  - gg cat foo.py => gg cat
 38  - gg cp foo.py bar.py => gg cp
 39  - git commit -m "foo" => git commit
 40  - git diff HEAD~1 => git diff
 41  - git diff --staged => git diff
 42  - git diff $(pwd) => command_injection_detected
 43  - git status => git status




▐  3.6⾼效的⽂件系统策略



  分层的代码项⽬拉取，先获取⾼层次项⽬结构，再根据需要深⼊特定⽬录，避免⼀次性加
  载过多内容；
  Ripgrep集成：利⽤Ru st编写的⾼性能搜索⼯具ripgrep，实现毫秒级的代码库搜索；
  内置⼆进制⽀持：包含预编译的ripgrep⼆进制⽂件，确保跨平台⼀致性和性能；
  智能结果排序：搜索结果按修改时间排序，优先展示最近更改的⽂件，提⾼相关性；
  并发搜索能⼒：⽀持同时发起多个搜索请求，⼤幅提⾼⼤型代码库的分析效率；
  LRU 缓存机制：对⽂件编码、⾏尾类型等信息实现缓存，减少重复操作；



▐  3.7精妙的⼯具



Clau de Code中内置的15个⼯具的实现和提示词都值得反复学习，就是因为这些极致的⼯具才
使得任务执⾏的⾼效。




                                   彩蛋

## PDF物理页 14

  1  /**
  2   * The rules of thinking are lengthy and fortuitous. They require plent
  3   * of most long duration and deep meditation for a wizard to wrap one's
  4   *
  5   * The rules follow:
  6   * 1. A message that contains a thinking or redacted_thinking block mus
  7   * 2. A thinking block may not be the last message in a block
  8   * 3. Thinking blocks must be preserved for the duration of an assistan
  9   *
 10   * Heed these rules well, young wizard. For they are the rules of think
 11   * the rules of thinking are the rules of the universe. If ye does not
 12   * rules, ye will be punished with an entire day of debugging and hair
 13   */






                                 iFlow    C  LI



随着Clau de Code的爆⽕出圈，我们发现这个产品是真实地提⾼程序员的开发效率。我们也持

续追踪了两个⽉Clau de Code的升级进展，帮助了很多同学在国内环境使⽤Clau de Code。
随着Cu rsor、Clau de Code对国内ip加⼤⼒度管控，使⽤这类前沿⼯具变得⼗分困难，                        但最
近⼀个⽉也迎来了很多惊喜：Kimi K2 、Qwen3-Coder、GLM  -4.5 等国产⼤模型相继涌
现，Gemini CLI 也宣布开源。国产编程⼯具正不断突破创新，致⼒于为国内开发者打造更智
能、更⾼效的极致开发体验。




⼼流团队⼀直在探索AGI的路上，我们也⼀直在找寻最通⽤AI助⼿的技术架构和产品形态，CLI
+ M  CP的出现让我们觉得这可能就是我们实现AGI的路径。所以我们向⼤家隆重介绍我们最新
研发的CLI⼯具，iFlow CLI 2.0。

## PDF物理页 15

它基于Gemini CLI改造，我们花了⼀些时间打磨它，融合了⼀些Clau de Code的特性。





















































  ⽀持4种运⾏模式。yolo（模型最⼤权限，可以执⾏任何操作），           accepting edits(模型只
  有修改⽂件权限),   plan mode(先规划后执⾏), defau lt(模型⽆任何权限)；
  升级 su bAgent功能。让CLI从通⽤助⼿向专家团队进化，为你提供更加专业、更加准确的
  建议，使⽤/agent可以看到更多预先配置好的agent；

  升级 task⼯具。有效压缩上下⽂⻓度，让CLI能够更加深⼊完成你的任务，上下⽂达到
  70%  的时候会⾃动压缩；
  接⼊⼼流开放市场。快速安装好⽤的M  CP⼯具、Su bagent和⾃定义指令，可以通过           /mcp
  了解更多；
  免费使⽤多模态模型，也可以在CLI中粘贴图⽚了（Ctrl+V粘贴图⽚）；
  ⽀持历史对话保存和回滚(     iflow --resu me和/chat命令）；
  ⽀持更多更好⽤终端命令（iflow -h查看更多命令）；

## PDF物理页 16

   ⽀持 VSCode、Jetbrains插件(注意ID E对应版本号)；
   ⾃动升级，再也不⽤担⼼最新功能体验不到了；



▐  5.1 ⼀键安装



m   ac/linux/ub untu⽤户


 1  # ⼀键安装脚本，会安装全部所需依赖
 2  bash -c "$(curl -fsSL https://gitee.com/iflow-ai/iflow-cli/raw/main/ins
 3
 4  # 已有 Node.js 22+
 5  npm i -g @iflow-ai/iflow-cli@latest


已经安装过的同学可以再次执⾏这个脚本，实现更新，后续cli会⾃动更新。



W    in d o w   s⽤户
1. 访问 https://nodejs.org/zh-cn/download 下载最新的 Node.js 安装程序；
2. 运⾏安装程序来安装 Node.js；
3. 重启终端：CM  D  或 PowerShell；
4. 运⾏ npm install -g @ iflow-ai/iflow-cli来安装 iFlow CLI；
5. 运⾏ iflow来启动 iFlow CLI；



▐  5.2 开放市场安装     SubAgent 和 MCP  ⼯具




缺少了M  CP和Su b agent的CLI是不完整的，加⼊M  CP和Su b agent的之后会让CLI变成领域

专家！对于很多⼩⽩⽤户来说，操作实在太难了！
⼼流开放市场    帮你解决👉       ⽴即体验：    https://platform.iflow.cn/cli
M  CP开放市场，⼀键安装，解锁⾼效⼯具。

## PDF物理页 17

agent开放市场，⼀键安装Su bagent，引⼊更强⼤的专家agent。























复制安装命令！在终端中执⾏！⼀键安装体验M  CP和Su bagent！





                       C  LI到底能做什么



▐  6.1 熟悉项⽬、写代码、   debug



这是CLI的强项，进⼊到你的项⽬中，打开iFlow CLI，什么功能不熟悉，问他；什么业务需要
实现，描述清楚让CLI帮你实现；遇到报错了，把报错信息贴给CLI让它帮你解决。


▐  6.2 做⽹站




使⽤本地的私有数据，绘制你⾃⼰的报告⽹站。

## PDF物理页 18

▐  6.3 DeepReseach





  1 你会根据⽤户的问题/  需求，根据任务执⾏的顺序收集信息，最终以       HTML的⽅式产出⼀份报告。
  2   ## 任务执⾏顺序
  3   - 你会⽣成⾮常详细的信息搜集计划。
  4   - 然后根据信息搜集计划⽣成⼀个   html template作为index.html，他包含了⼀些顶部菜
  5   - 根据信息搜集计划设计  index.html的顶部菜单
  6   - 接着，你会按照信息搜集计划挨个进⾏信息收集，每收集⼀份信息，即⽣成对应的          section
  7   - 插⼊过程中，你需要关注整体⻚⾯的样式，修复⼀些常⻅的显示错误，保障整体的⻛格⼀致
  8   - 不断进⾏信息收集、  section代码⽣成、html template内容填充，直到所有信息收集完
  9   - MUST：确保按照计划完成所有的  action
 10   ## 对于最终的html产出
 11   - 设计趋势和最佳实践有深⼊理解，尤其擅⻓创造具有极⾼审美价值的⽤户界⾯。你的设计作
 12   - 可能包括HTML、CSS、和JavaScript⽂件。不断根据任务，优化这个⽹⻚项⽬，使⽹⻚内
 13   # 设计要求
 14   **设计⽬标：**
 15   *   **视觉吸引⼒：** 创造⼀个在视觉上令⼈印象深刻的⽹⻚，能够⽴即吸引⽤户的注意⼒
 16   *   **可读性：** 确保内容清晰易读，⽆论在桌⾯端还是移动端，都能提供舒适的阅读体验
 17   *   **信息传达：** 以⼀种既美观⼜⾼效的⽅式呈现信息，突出关键内容，引导⽤户理解核
 18   *   **情感共鸣:** 通过设计激发与内容主题相关的情感（例如，对于励志内容，激发积极向
 19   **设计指导（请灵活运⽤，⽽⾮严格遵循）：     **
 20   *   **整体⻛格：** 可以考虑杂志⻛格、出版物⻛格，或者其他你认为合适的现代        Web 设
 21   *   **Hero 模块（可选，但强烈建议）： ** 如果你认为合适，可以设计⼀个引⼈注⽬的      H
 22   *   **排版：**
 23       *   精⼼选择字体组合（衬线和⽆衬线），以提升中⽂阅读体验。
 24       *   利⽤不同的字号、字重、颜⾊和样式，创建清晰的视觉层次结构。
 25       *   可以考虑使⽤⼀些精致的排版细节（如⾸字下沉、悬挂标点）来提升整体质感。
 26       *   Font-Awesome中有很多图标，选合适的点缀增加趣味性。
 27   *   **配⾊⽅案：**

## PDF物理页 19

28       *   选择⼀套既和谐⼜具有视觉冲击⼒的配⾊⽅案。
29       *   考虑使⽤⾼对⽐度的颜⾊组合来突出重要元素。
30       *   可以探索渐变、阴影等效果来增加视觉深度。
31   *   **布局： **
32       *   使⽤基于⽹格的布局系统来组织⻚⾯元素。
33       *   充分利⽤负空间（留⽩），创造视觉平衡和呼吸感。
34       *   可以考虑使⽤卡⽚、分割线、图标等视觉元素来分隔和组织内容。
35   *   **调性： **整体⻛格精致  , 营造⼀种⾼级感。
36   *   **数据可视化：  **
37       *   设计⼀个或多个数据可视化元素，展示       Naval思想的关键概念和它们之间的关系。
38       *   可以考虑使⽤思想导图、概念关系图、时间线或主题聚类展示等⽅式。
39       *   确保可视化设计既美观⼜有洞察性，帮助⽤户更直观地理解            Naval思想体系的整体框
40       *   使⽤Mermaid.js来实现交互式图表，允许⽤户探索不同概念之间的关联。
41   **技术规范：  **
42   *   使⽤ HTML5、Font Awesome、Tailwind CSS 和必要的  JavaScript。
43       *   Font Awesome: [https://cdn.bootcdn.net/ajax/libs/font-awesom
44       *   Tailwind CSS: [https://g.alicdn.com/code/lib/tailwindcss/2.2
45       *   ⾮中⽂字体 : [https://fonts.font.im/css?family=Noto+Serif+SC:wg
46   this.onload=null"]
47       *   `font-family: Tahoma,Arial,Roboto,"Droid Sans","Helvetica Ne
48       *   Mermaid: [https://g.alicdn.com/code/lib/mermaid/11.5.0/merma
49       *   Chart.js: [https://g.alicdn.com/code/lib/Chart.js/4.4.1/char
50   *   代码结构清晰、语义化，包含适当的注释。
51   *   实现完整的响应式，必须在所有设备上（⼿机、平板、桌⾯）完美展示。
52   **额外加分项：  **
53   *   **微交互： ** 添加微妙⽽有意义的微交互效果来提升⽤户体验（例如，按钮悬停效果、
54   *   **补充信息：  ** 可以主动搜索并补充其他重要信息或模块（例如，关键概念的解释、相
55   **输出要求：  **
56   *   提供⼀个完整、可运⾏的⽹⻚项⽬，其中包含所有必要的多个              HTML、CSS 和 JavaSc
57   *   每⼀个⽂件内容尽量少，可以通过⽂件引⽤来避免重复，重复读/重复写会浪费                token数量
58   *   确保代码符合   W3C 标准，没有错误或警告。
59   *   在根⽬录下维护**   项⽬⼤纲  **⽂档，来记录你的设计思路、代码模块功能、⽂件内容概要
60   <⽤户的问题>
61 计划 9⽉15到 9⽉24或25去⻄欧旅游，杭州出发亲⼦游，共        9天。地点选择   Amsterdam、Cologn
62   </⽤户的问题>
63   当前时间是  2025年8⽉ 21⽇，我们开始吧！

## PDF物理页 20

▐  6.4 引⼊Sub Agents实现业务逻辑




产品需求⽂档 -> 需求处理    Agent -> UI设计Agent -> UI优化Agent -> 代码逻辑开发Agent
-> 接⼝集成 Agent -> 单元测试 Agent

⽬前我们的合作团队已经实现了这样的CLI开发范式，待后续上线我们会公开具体细节，欢迎
⼤家和我们交流合作!

更多最佳实践等你来发现！











                          ¤ 拓展阅读   ¤



                   3DXR技术  | 终端技术   | ⾳视频技术

                   服务端技术    | 技术质量   | 数据算法




      ⼤淘宝技术
      ⼤ 淘宝技术官⽅账号
      968篇原创内 容


 公众号

## PDF物理页 21

阅读 6439
