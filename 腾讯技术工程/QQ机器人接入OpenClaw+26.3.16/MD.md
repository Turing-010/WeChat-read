# 原文逐页转写

文本来自本次 PDF 文本层；不补写图片、截断内容或代码。图片和布局请打开每页 PDF 链接核对。AI 解释另见学习笔记。

## PDF 第 1 页

[原页](RAW.pdf#page=1)

````text
重磅！腾讯 QQ 机器⼈接⼊ OpenClaw ，官⽅“养虾”指南来了
腾讯程序员 2026 年 3 ⽉ 16 ⽇ 02 : 36⼴东原创 腾讯技术⼯程 54 ⼈
作者：腾讯QQ 机器⼈团队
快速注册⼀个  QQBot
QQ 机器⼈开放平台提供了快捷创建  QQ 机器⼈
的通道，三步即可创建⼀个可⽤的  QQBot ，⽤于接⼊  OpenClaw 。
1. PC 端打开：https://q.qq.com/qqbot/openclaw/login.html， QQ 扫码登录。
2. 点击创建机器⼈。点击后会⽴刻成功，此时  BOT 会给你  QQ 发⼀条成功消息，头像昵称
可按⽤户喜好⾃定义编辑。
3. 复制  AppID 和  AppSecret 到  🦞  部署地配置即可，配置成功后，即可通过  QQ 使唤你的
🦞 。
````

## PDF 第 2 页

[原页](RAW.pdf#page=2)

````text
机器⼈创建成功后，此时你的  BOT 还没有 “ 灵魂 ” ，需要接⼊到你⾃⼰的  OpenClaw 运⾏环
境，这⾥也推荐使⽤腾讯云的  Lighthouse 接⼊。
“ 云上养虾 ” 教程：🔥 玩转  OpenClaw ｜云上  OpenClaw(Clawdbot) 快速接⼊  QQ 指南
OpenClaw 官⽅安装教程：OpenClaw — Personal AI Assistant
其实也并不复杂，在终端执⾏个命令，按部就班配置⼀些  model 、 skills 、 channel 即可。
QQ 作为  OpenClaw 的通讯渠道，需要在  OpenClaw 安装配置  QQBot 插件，才能与  QQBot
通信。多数云平台（如腾讯云）帮你简化了该步骤，⽤户仅需复制粘贴相关密钥到云上的管理
端页⾯即可。以下内容讲述如何⼿动安装  QQBot 插件与更新。
QQ Bot 插件消息收发能⼒总览：
在原⽣  OpenClaw 中安装  QQBot 插件
本⽂介绍在原⽣  OpenClaw 环境中安装或升级  QQBot 插件的⼏种常见⽅式。你可以根据⾃⼰
的使⽤习惯，选择远程⼀键执⾏、本地脚本执⾏，或⼿动安装
QQBot 插件官⽅仓库：
https://github.com/tencent-connect/openclaw-qqbot  
这个  BOT 仅创建⼈可⽤，暂时不⽀持将  BOT 拉⼊ QQ 群内。
````

## PDF 第 3 页

[原页](RAW.pdf#page=3)

````text
欢迎⼤家前往查看最新代码与更新说明，也欢迎通过  Issue 和  PR 提出问题反馈与改进建议，
共同完善插件能⼒与接⼊体验。。
⽅式⼀：远程⼀键安装升级（推荐）
适合希望快速完成安装或升级的场景，⽆需⼿动  clone 仓库。
⾸次安装时，需提供  QQBot 通道凭证：
curl -fsSL https://raw.githubusercontent.com/tencent-connect/openclaw-qqbot/main/scripts/
  | bash -s -- --appid YOUR_APPID --secret YOUR_SECRET
该命令会⾃动完成以下步骤：
下载安装脚本
清理旧插件
安装新插件
配置  QQBot 通道
启动或重启  OpenClaw 服务
完成后即可打开  QQ 开始使⽤。
如果此前已经完成过通道配置，后续升级可直接执⾏：
curl -fsSL https://raw.githubusercontent.com/tencent-connect/openclaw-qqbot/main/scripts/
说明：如果想要升级 QQBot 官⽅插件版本，也可以执⾏该脚本，这个脚本是带升级能⼒的，
⽽且默认⾏为是升级到  npm 上的  latest 版本。如果是想安装指定版本，后⾯可以跟--versio
n命令：
curl -fsSL https://raw.githubusercontent.com/tencent-connect/openclaw-qqbot/main/scripts/
常⽤参数如下：
参数 说明
--appid <id> --secret <secret>配置通道。⾸次安装必填，或在更换凭证时使⽤
--version < 版本号 > 安装指定版本
--self-version 升级到当前仓库  package.json ⾥声明的版本
-h
 / --help 查看完整帮助信息
````

## PDF 第 4 页

[原页](RAW.pdf#page=4)

````text
⽅式⼆：源码安装升级
适合希望先查看仓库内容、在本地执⾏脚本，或希望更灵活控制安装流程的场景。
先拉取仓库：
git clone https://github.com/tencent-connect/openclaw-qqbot.git
cd openclaw-qqbot
通过本地脚本进⾏源码安装或升级（该脚本同样具有升级到最新版本的能⼒）：
bash ./scripts/upgrade-via-source.sh --appid YOUR_APPID --secret YOUR_SECRET
说明：脚本执⾏到后⾯会让选择   是否后台重启  openclaw ⽹关服务？ [Y/n]，⼀般选择   Y。
如果后台启动正常，会执⾏   openclaw logs --follow  持续输出  OpenClaw 运⾏⽇志。后⾯看到
有⽇志持续输出代表已经正常启动了，不代表还没升级完，可以   Ctrl+C  关掉前台⽇志。
正常执⾏脚本到最后会输出⽇志：
⽅式三： npm ⽅式⼿动安装升级
适合希望完全⼿动控制安装步骤，或需要排查安装问题的场景。
安装命令：
# （⾸次安装可跳过）卸载 qqbot 旧插件，卸载 openclaw-qqbot 旧版本插件
openclaw plugins uninstall qqbot
openclaw plugins uninstall openclaw-qqbot
# 安装 openclaw-qqbot 最新版本
openclaw plugins install @tencent-connect/openclaw-qqbot@latest
````

## PDF 第 5 页

[原页](RAW.pdf#page=5)

````text
# 配置通道（⾸次安装必做）
openclaw channels add --channel qqbot --token "AppID:AppSecret"
# 启动  / 重启服务
openclaw gateway restart
已安装官⽅ openclaw-qqbot ，升级版本命令：
# 通过 npm 包升级（适⽤于之前插件本身就是通过可更新来源安装的情况： openclaw plugins install @tencen
openclaw plugins update openclaw-qqbot
# 启动  / 重启服务
openclaw gateway restart
安装选择建议
想快速安装：优先使⽤⽅式⼀：远程⼀键安装升级
想先查看脚本再执⾏：使⽤⽅式⼆：本地源码安装升级
想⾃⾏控制每⼀步：使⽤⽅式三： npm ⽅式⼿动安装升级
安装结果检查
QQBot 插件是否正常加载
安装完成后，可通过以下命令检查插件是否已成功加载：
openclaw plugins list | grep openclaw-qqbot
如果输出中存在对应插件条⽬，且状态为   loaded，说明  QQBot 插件已经安装好了，⽽且已
经被  OpenClaw 成功加载。但并不能说明通道⼀定连上了。
QQBot 通道是否正常连通
执⾏以下命令查看通道状态：
openclaw channels status
openclaw channels status  中  QQ Bot 通道显⽰为   enabled, configured, running，且机器⼈实际
可以正常收发消息或   in/out  时间持续更新时，可认为 QQBot 通道已正常连通。
````

## PDF 第 6 页

[原页](RAW.pdf#page=6)

````text
这⾥的   in:2m ago, out:2m ago  说明：
in:2m ago： 2 分钟前还有⼊站消息
out:2m ago： 2 分钟前还有出站消息
插件的能⼒及消息⽰例
OpenClaw QQBot 插件提供了富媒体收发⽀持，覆盖图⽚、语⾳、视频、⽂件的双向交互。
需要声明的是， QQ Bot 插件仅作为消息通道使⽤ —— 负责在  QQ 与  OpenClaw 之间中转消
息。诸如图像理解、语⾳转录、绘图等功能，取决于您所配置的  AI 模型以及  OpenClaw 内部
已安装的技能，⽽⾮本插件本⾝。
AI 能接收什么
除了接收⽇常的⽂本消息以外， QQBot 通道还⽀持接收多种媒体消息。
接收语⾳配置⽰例
````

## PDF 第 7 页

[原页](RAW.pdf#page=7)

````text
其中语⾳消息（ STT ）需要单独配置模型能⼒，⽤于语⾳转⽂字后交给⽂本⼤模型处理，配置
⽅式如下：
STT ⽀持两级配置，按优先级查找：channels.qqbot.stt（插件专属） ->  tools.media.audio.mod
els[0]（框架级回退）。以框架级配置为例：
{
  "tools": {
    "media": {
      "audio": {
        "models": [
          { "provider": "xxx", "model": " 模型名称 " }
        ]
      }
    }
  }
}
这⾥的   provider  引⽤   models.providers  中的  key ，⾃动继承   baseUrl  和   apiKey，⽀持任
何  OpenAI 兼容的  STT 接⼝，也可在条⽬中直接写   baseUrl /  apiKey  覆盖。
另外，插件版本 1.5.6 已经⽀持当  STT 未配置或转写失败时，使⽤  QQ 平台内置  ASR ⽂本作
为低置信度兜底结果，⽅便没有 STT 模型的⽤户可以使⽤ QQ 机器⼈平台侧提供的语⾳转⽂本
结果。
AI 能发送什么
除了常⽤的  markdown 消息、⽂本消息以外， QQBot 插件通道⽀持发送语⾳、⽂件、图⽚、
视频等常⽤的多媒体消息。
发送语⾳配置⽰例
语⾳（ TTS ）需要单独配置模型能⼒，把⽂字转成语⾳通过  QQ 发给你。配置  TTS 后， AI 可
以把⽂字变成语⾳消息发出来。⽐如让它讲个笑话，回复直接就是⼀条语⾳。
TTS 同样⽀持两级配置：channels.qqbot.tts（插件专属） ->  messages.tts（框架级回退）。以
插件专属配置为例：
````

## PDF 第 8 页

[原页](RAW.pdf#page=8)

````text
{
  "channels": {
    "qqbot": {
      "tts": {
        "provider": "xxx",
        "model": " 模型名称 ",
        "voice": " 模型名称 : ⾳⾊名称 "
      }
    }
  }
}
provider  引⽤   models.providers  中的  key ，⾃动继承   baseUrl  和   apiKey。可通过   voic
e  选择⾳⾊，设置   enabled: false  可禁⽤。
另外如果没有现成可使⽤的  TTS 模型，也可以使⽤  TTS/Edge （ OpenClaw 原⽣⽀持的⼀种
TTS provider ），配置如下（在messages⾥增加tts的配置）：
{
  "messages": {
    "tts": {
      "auto": "inbound",
      "provider": "edge",
      "edge": {
        "enabled": true,
        "voice": "zh-CN-XiaoxiaoNeural",
        "lang": "zh-CN"
      }
    }
  }
}
验证通道发送图⽚或者⽂件正常
可以⽤以下⽅式验证  QQ Bot 通道发送图⽚ / ⽂件能⼒是否正常：发给模型⼀张图⽚，让模型
把这张图回给你。如果能正常回复，说明通道能⼒正常。注意，⽣成图⽚或者对⽂件进⾏理解
等都是  OpenClaw ⾃⼰的能⼒，需要配置对应的模型或者  Skills ， QQ Bot 插件只负责传输。
````

## PDF 第 9 页

[原页](RAW.pdf#page=9)

````text
体验演⽰场景
以下是⼏个可以直接复现的玩法：
如何配置  Skills
在腾讯云  Lighthouse 安装  clawhub 的  Skills
在  Lighthouse 实例的应⽤管理页⾯上可以直接安装  skills ，如图：
````

## PDF 第 10 页

[原页](RAW.pdf#page=10)

````text
点击页⾯上【获取更多  skills 】的链接跳到开源社区  ClawHub 的官⽹，选择你需要的  skills 。
注意这⾥  skills 的名字，就是点击跳转某个  skills 的页⾯链接  URL 最后的内容：
确定名字后，直接在  Lighthouse 应⽤管理页⾯上点击【安装技能】即可。
⼿动安装  clawhub 的  Skills
如果想⼿动安装  ClawHub 上的  skills ，具体步骤如下：
# 1. 安装  clawhub cli
npm i -g clawhub
# 2. 装完确定下是否可⽤：
clawhub --help
# 3. 进⼊  OpenClaw workspace
cd ~/.openclaw/workspace
# 4. 搜索  skill
clawhub search " 你想要的功能关键词 "
# 5. 安装  skill
clawhub install <skill-slug>
````

## PDF 第 11 页

[原页](RAW.pdf#page=11)

````text
# 6. 检查是否识别到
openclaw skills list
openclaw skills check
# 7. 如需配置  API Key ，则编辑配置⽂件
vi ~/.openclaw/openclaw.json
# 8. 重启  gateway
openclaw gateway restart
# 9. 看⽇志
openclaw logs --follow
# 10. 检查⽬前已经安装了哪些  skills
openclaw skills list --eligible
openclaw skills info < 这⾥填  list ⾥显示的某个  skills 的名字 >
如果完成以上安装后， agent 提⽰仍找不到对应  skills ，可以通过和  agent 对话的⽅式让
OpenClaw 分析问题并完成安装：
````

## PDF 第 12 页

[原页](RAW.pdf#page=12)

````text
````

## PDF 第 13 页

[原页](RAW.pdf#page=13)

````text
也推荐⼤家遇到各种包括  skills 安装在内的问题时，尝试习惯通过和  agent 交流，让它帮你分
析并解决问题。
⼿动安装⾃⼰写的  Skills
安装⾃⼰写的  skills ，最主要的就是把你的  skills 建⼀个⽂件夹放在   ~/.openclaw/workspace/skil
ls/  ⽬录下。
这⾥提供了⼀个安装   my-demo-skill 的简单⽰例：
# 1. 创建  skills ⽬录，假设这⾥的  skills 叫  my-demo-skill
mkdir -p ~/.openclaw/workspace/skills/my-demo-skill
# 2. 写⼊  skills ，或者把已经写好的  skills 放在对应⽬录下
cat > ~/.openclaw/workspace/skills/my-demo-skill/SKILL.md <<'SKILL_EOF'
---
name: my_demo_skill
description: A simple custom skill for testing.
---
# My Demo Skill
当⽤户要求测试⾃定义  skill 时，优先遵循这⾥的说明。
触发示例：
- “ 调⽤  my demo skill”
⾏为：
- 回复： “ 已命中  my_demo_skill”
SKILL_EOF
# 3. 让  OpenClaw 重新发现这个  skill ，可以通过对话让  agent “refresh skills” ，或者直接重启  gateway
openclaw gateway restart
openclaw skills list
openclaw skills info my_demo_skill
通过对话验证   my-demo-skill 触发成功：
````

## PDF 第 14 页

[原页](RAW.pdf#page=14)

````text
FAQ （持续更新）
Q ：为什么⼀直输出 “ 你好，我不能提供相关信息 ” ？
A：模型输⼊输出内容会进⾏安全审查，可以尝试以下⽅法：
通过   /new  开启新对话
更换模型后再试
Q ：为什么设置好  QQ 机器⼈信息后，与机器⼈对话时⼩灰条提⽰ “ 我的灵魂不在线 ” 等错误？
A1 ：如果是第⼀次配置， OpenClaw 与机器⼈建⽴联系可能需要⼀点时间，可以尝试重启⼏
次   openclaw gateway restart
A2 ：如果原来已经有机器⼈，⼜重新更换配置了新的 APPID ，如果机器⼈⽆法回复：
● 解决⽅式 1 ：删除    ~/.openclaw/qqbot/sessions/session-default.json  然后重启
● 解决⽅式 2 ：更新  QQBot 插件（见前⽂插件更新教程）
A3 ：如果⼀直提⽰此错误，是因为机器⼈没有在线，检查机器⼈ APPID 和密钥配置是否正
常。
Q ：机器⼈提⽰已经被注销怎么办？
A：解决⽅案：检查是否删除了机器⼈，如果删除了 7 天内可以前往  QQ 开放平台  进⾏恢复。
Q ：为什么在群⾥⾯ @ 机器⼈，遇到提⽰： " 该机器⼈当前服务状态异常，暂时⽆法回复消
息 " ？创建的 openclaw 机器⼈是否⽀持加群？
A：因为 openclaw 机器⼈暂不⽀持加群，仅⽀持个⼈⽤户私聊使⽤。如果有下⼀步⽀持计划，
会及时更新⽂档通知⼤家。
Q ：快速创建的 openclaw 机器⼈是否⽀持在开放平台修改信息？
````

## PDF 第 15 页

[原页](RAW.pdf#page=15)

````text
A：⽀持，⽅式如下：
Q ：机器⼈为什么回复 “401 not authorized” ？
A：模型配置没有成功，请注意检查下模型  api key 配置，注意并不是  qqbot 的  secret 哦。
Q ：机器⼈为什么回复 “API rate limit reached. Please try again later.”
A：模型调⽤频率太快了，请检查模型使⽤情况或更换模型。
Q ：如何联系官⽅⼈员？
A：可加⼊讨论群、讨论频道或添加机器⼈进⾏反馈，见⽂本最后的⼆维码。
Q ：如何查询⽇志？
A：请登录 openclaw 运⾏的机器，使⽤终端输⼊ “openclaw logs --follow” 以显⽰实时⽇志。
Q ：为什么 openclaw 机器⼈发不出图⽚？
A：可以发⼀张图⽚让机器⼈原样会给你，验证下是通道的问题，还是模型没有画图 skills ⼯
具。如果是需要画图能⼒，需要⾃⼰配置画图 skills ，⼀般需要⾃⼰购买⽣图模型获得⽣图的
api key 。
Q ：如果我从其他渠道的  qqbot 插件想升级到官⽅插件  @tencent-connect/openclaw-qqbot，
应该怎么操作？
A：升级⽅式参考本⽂⾥的【原⽣  OpenClaw 安装插件  QQBot 插件】这部分内容。
交流与反馈
````

## PDF 第 16 页

[原页](RAW.pdf#page=16)

````text
阅读 1 . 3 万
如果 QQ 交流群已经满员，可前往  PC 管理端扫码添加最新群聊：
https://q.qq.com/qqbot/openclaw/login.html
最后， QQBot 官⽅接⼊指南仍在持续更新，欢迎访问在线⽂档  《 QQ 机器⼈接⼊  OpenClaw
的官⽅ “ 养虾 ” 指南》  查看最新内容。如果你在养虾过程中遇到问题，或有任何建议与反馈，
也欢迎随时交流。我们会持续补充和完善⽂档内容，陪⼤家⼀起把虾养得更轻松、更顺⼿。
腾讯技术官⽅号。腾讯技术创新、前沿领域发布解读平台。
688 篇原创内容
腾讯技术⼯程
公众号
留⾔
写留⾔
````

## PDF 第 17 页

[原页](RAW.pdf#page=17)

````text
还没有留⾔，来写⾸评
````

## 采集与转写核验记录（非原文）

以下说明由本次核验添加；上方逐页文本保持文本层原样，图片与布局以PDF为准。

- PDF物理页 3：p.3远程安装命令右侧裁切，未补造URL
