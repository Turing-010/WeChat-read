# 代码染色&无效代码清理：PDF文本转写

> 这是原始PDF文本层转写，不是学习摘要。页码为PDF物理页序；图表、代码版面和图片文字不能完整表达在此文本层。已查看图像的内容和质量问题见AI学习笔记及META.json。

[原文PDF](RAW.pdf) · [AI学习笔记](AI_代码染色与无效代码清理.md) · [处理与质量记录](META.json)

## PDF 第1页

[查看原页](RAW.pdf#page=1)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
代码染色&无效代码清理
原创
首页&信息流工程 2025年11月21日 01:44 浙江
大淘宝技术 314人
D是我们团队的服务端应用，其代码库历史悠久，最早可以追溯到淘宝APP无线端迁移，
应用中许多代码已无线上流量，但代码并未随业务的下线被清理。越来越多的代码“沉淀”
下来，既增加了团队新人学习门槛，也增加日常开
发维护成本。但实际做代码下线并非容
易，仅凭业务逻辑决策代码清理费时费力，还容易误删在使用的业务代码，因此非常需要
工具来辅助做代码的清理，这就是基于代码执
行染色和覆盖分析做代码下线
方
案的背景。
代码执
行染色&执
行
覆盖率分析，使用JVM agent的扩展能力实现代码的插桩和在线
色，再通过解析采样的数据可得到代码的执
行情况，清理代码就“有理有据”；仅靠原始分
析出的数据清理依然低效，为此我们将数据采集、
覆盖率可视化通过IDEA插件集成，实现
清理无效代码过程又准又快。
染
代码覆盖率采集
▐ 1.1 JVM Agent 概述
在 Java 中，插桩(Instrumentati
on) 是一个非常重要的接口，它为开
发
者提供了在 JVM 运
行
时动态修改类字节码的能力。这个功能是 Java 提供的 Java Agent 机制
的核心组成部分，
常用于性能监控、AOP（面向切面编程）、代码覆盖率分析、热部署等场景。
Instrumentati
on
接口位 于java.lang.instrument包中， 由 JVM 在加 载 Java Agent 时自
动提供一个实例，通过预定义
的方法传递给 Agent。
主要用途包括：
动态修改类的字节码（Class File）
获取 JVM 中已加载的所有类
添加类文件转换器（ClassFileTransformer）
重新定义类（redefineClasses）
重置类的字节码（reset class definiti
ons）
```

## PDF 第2页

[查看原页](RAW.pdf#page=2)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
对在线代码的插桩须通过 Java Agent 机制在 JVM 启动时或运
行
时介入类加载过程，它可以
对 JVM 进
行
一些操作，如修改类字节码、监控 JVM 状态等。Agent 可以通过 -javaagent
参数在启动时加载，也可以通过 Attach API 在运
行
时动态加载。
类别 依
赖重启
长
期采集资源占用
agent 是 稳定 共用jvm
attach 否 重启失效 独立jvm
使用agent方式是在jvm启动参数指定 -javaagent 来加载agent jar包，agent需要实现
AgentMain接口。
使用attach的方式会创建独立JVM，占用独立内存资源，使用attach的方式将插桩jar包作
用于目标jvm，插桩jar包需要实现PreMain的接口，代码示例：
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
String jarFile = args[0];
String pid = getPid(args);
logger.info("Attaching agent to PID: " + pid);
VirtualMachine vm = null;
try {
vm = VirtualMachine.attach(pid);
vm.loadAgent(jarFile);
logger.info("Agent attached successfully");
} catch (IOException ioException) {
logger.critical("load agent jar fail: " + jarFile);
} catch (AttachNotSupportedException attachNotSupportedException) {
logger.critical("attach to jvm fail: " + pid);
} catch (AgentLoadException | AgentInitializationException agentExcepti
logger.critical("jvm load agent or agent init fail: " + pid);
} finally {
if (vm!=null) {
vm.detach();
}
}
两
种方式因使用方式
不同，适用场景会有差异，后续会做对比
介绍。
▐ 1.2 代码执
覆盖
行
统计代码执
染色我们主要讨论
行情况可以基于覆盖率，有
覆盖率、分支覆盖、
行
行
覆盖率，知道指定package和类的
行
方法覆盖等概念。针对腐朽代码
覆盖率就大概可以知道治理的方向。
```

## PDF 第3页

[查看原页](RAW.pdf#page=3)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
1.2.1 自定义
方
案
自 定义 插桩 主 要 基 于1.1中agent或者 attach的方 式， 通 过 1.2中的接口和ASM实 现 代 码 的插
桩，实际插桩可以按
执
，也可以按
行
行
方法插桩，示例可以参考1.2.3中。自定义
的方式对理解
和实
践插桩过程很有帮助，比
较方便自定义
的方式处理采集的数据，但存在问题：
执
行
效率低，尤其是按
行
插桩，侵入性太大；
并发情况下存在锁竞争风险，虽然实际结果对统计代码执
覆盖没影响；
行
执
行结果使用上不便于集成IDEA，对代码覆盖的可视化支持难度大；
1.2.2 JaCoCo方
案
JaCoCo (Java Code Coverage)通过在类加载时修改字节码来插入探针（probes），这些
探 针 会 在 代 码 执
行
时 记 录 哪 些 代 码行 被 访 问过 ， 当 类 被 加 载 时 ， JaCoCo 的
ClassFileTransformer 会被调用，会修改类的字节码，插入探针来记录代码的执
行情况。
JaCoCo 使用 的 探 针 为 $jacocoInit[boolean] 数组 ， 数组
长 度 为 类 的 探 针 数 量， 由
CFG(Control Flow Graph， 控制流图)分析得到，将代码划分为代码块，$jacocoInit的每
个位置代码一个代码块入口，$jacocoInit[n]=true则表示整个代码块都被执
。
行
1
2
3
4
5
6
7
8
9
public void exampleMethod(int a, int b) {
// do some thing 代码块0
if(a > 0){
// do some thing 代码块1
}else if(b > 0){
// do some thing 代码块2
}
// do some thing 代码块3
}
上图代码示例中，有多个代码块，在CFG中为一个节点，CFG的边为代码块执
图代码插桩
后的探针如下图:
流转关系，上
行
```

## PDF 第4页

[查看原页](RAW.pdf#page=4)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
通过按代码块的插桩模式，比
逐
行
记录代码执
行情况高效很多，并且使用布尔数组
代 码 是否 执
行
也非 常高 效 (如果 使用 数值 变 量累 加 会存在锁 的问题， 对代 码 执
的方式判断
性能 影响 较
行
大)。JaCoCo提供了agent和cli工具，使用方式可参考：JaCoCo agent和JaCoCo cli。
▐ 1.3 采集方
对比
案
1.3.1 自研插桩 vs JaCoCo工具
高效将探针插入到代码中，不
对正常业务代码造成太大影响，是保障线上代码正常采集结果的
前提，如前所述，自己实现插桩自定义空间大，方
案设计灵活，缺点是效率和开
发成本高；使
用JaCoCo工具可以快速集成、性能高效。
优点缺点
自研插桩 灵活性高
、数据处理方便 开
发成本、
稳定性验证
JaCoCo工具 稳定高效、快速集成
数据 格式固 定 ， 采 集 数据 需
二次加工
考虑到目标应用D对稳定性和采集性能要求高，使用JaCoCo的方
案更加满足我们的需求。
1.3.2 agent vs attach
在1.1中有
介绍两者的区别，各有优势，对比
如下:
使用方式 性能影响 重启影响卸载插桩
agent方式 jvm启 动参 数增加
agent参数
随 jvm一起启 动，
业务无感，平
均cp
u会上涨
重启
效
不 失
重新发布
```

## PDF 第5页

[查看原页](RAW.pdf#page=5)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
attach方式 独立 jvm attach
到业务jvm
attach的时候 触 发
代 码 插桩 会导 致 jv
m飙 升 ， 之 后 下降
后稳定
重启失效无需重启
通过对比可知，agent的方式对代码有一定入侵，适合长
期稳定采集代码覆盖数据；attach的
方式则更加灵活，适合临时做单机的代码采样分析，参考arthas做在线分析的方式。
1.3.3 在线vs离线
针对包含热部署的场景，还会涉及到在线和离线插桩
的选
择
。在jvm启动后做代码字节增强的
算是在线插桩，而离线插桩指在代码编译打包且尚未部署阶段，通过maven插件的方式对代码
做修改。具体而言，就是在mvn build的时候引入JaCoCo的插件，直接在build阶段将字节码
插桩，这样部署的时候就已经是插桩
的代码。
如上图，在线插桩在部署和运
行
阶段，离线插桩在构建阶段。以使用JaCoCo做离线插桩为
例 ，还 需 要 在 部 署 时 引入 JaCoCo 的 依
赖
java.lang.TypeNotPresentExcepti
on，表示在类初始化时找不到依
赖
， 否 则 会 出 现
类，需要引入下面这
个依
：
赖
1
2
3
4
5
<!-- https://mvnrepository.com/artifact/org.jacoco/org.jacoco.agent -->
<dependency>
<groupId>org.jacoco</groupId>
<artifactId>org.jacoco.agent</artifactId>
<version>0.8.12</version>
```

## PDF 第6页

[查看原页](RAW.pdf#page=6)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
6
7
8
<scope>runtime</scope>
<classfier>runtime</classfier>
</dependency>
注意必须用<classfier>标签，生效的包是org.jacoco.agent-0.8.12-runtime.jar，而不是
org.jacoco.agent-0.8.12.jar，包含runtime的包包含完整的依
。
赖
这种方式适合热部署的插桩，对插桩
的包选
择
性部署。离线
方
案的缺点在于，考虑到插桩代码
运
行
存在性能损耗，如果不是所有在线机器
都部署采集，每次部署就需要至少打出两份部署
包：插桩版本的包和不做插桩
的包，将插桩包部署到需要采集的机器，非插桩包部署到其它机
器，这种分别部署的方式增加了部署调度的复杂性。
▐ 1.4 方
案选
择
D应用的代码治理是长
期持续的过程，我们需要长
期周期性持续采集在线代码执
行数据，同时
要考虑稳定性和效率，最终选
择
以agent的方式落地。我们复用了JaCoCo的采集染色方
案，
这一方
案成熟可靠，对系
统运
行
时影响较低。通过在docker file集成JaCoCo依
，在环境脚
赖
本中为jvm指定agent参数，并选
择
性采集安全生产环境，实现了对在线代码执
行数据的采样采
集。
落地方
案
核心工作链路如下：
```

## PDF 第7页

[查看原页](RAW.pdf#page=7)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
整个采集
+治理流程：
1. 代码插桩：在线或者离线
方式对业务代码完成探针插入；
2. 覆盖采集：业务代码跑起来，让每个QPS的请求渗透到每
行
代码，完成代码染色；
3. 周期dump：代码经过充分运
行
后，周期将最新的代码覆盖数据dump到对象存储OSS中；
4. 覆盖率计算：覆盖率包含
行、分支、类覆盖等，依
赖
代码.class文件和dump的采集数据，
输出xml覆盖报告；
5. 插件加载：每次打开IDEA项目代码时，加载最新的覆盖报告数据；
6. 代码治理：形成治理闭环，根据最新的报告清理或者重构代码，提升代码健康度。
▐ 2.1 整体设计
代码覆盖率主要针对日常开
执
行情况的检查。
从功能上应具备以下功能：
发代码链路检查、为代码重构、代码清理提供可靠依据，方便代码
代码采集：支持应用代码执
行
基于agent的方式，持续周期性采集；
支持长
期数据文档采集，合并多天数据；
覆盖率采集(主要为.exec文件)，不影响原有业务逻辑；
数据合并：代码执
盖=.exec文件
行情况的采集数据与最新代码版本生成完整代码覆盖情况;（最终代码覆
.class文件）
+
IDEA插件：代码执
行情况可视化，IDEA插件支持目标应用代码执
IDEA目标项目检测，非
目标项目提醒；
目标项目打开自动下载oss覆盖数据，也可配置第一次使用时下载；
支持多天数据采集下载和采集结果合并，提高代码采集覆盖准确性；
行情况的可视化
```

## PDF 第8页

[查看原页](RAW.pdf#page=8)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
打开代码执
隐藏代码执
示；
行
行
覆盖情况，展示package、class执
覆盖情况，关
闭package、class执
行
行
覆盖率和代码行
覆盖率和代码行
支持采集数据的缓存和刷新，无需重复下载oss数据；
右键和工具栏支均支持打开&关
闭展示、工具栏和配置页支持插件相关
级执
级执
行情况；
行情况的展
的配置；
▐ 2.2 代码采集
2.2.1 热部署的影响
在应用D之上基于自研热部署方
案部署了R和B应用，其关系
是这样的：
D应用就像个容器，里面主要定义了基础的流程；业务通常以插件的方式在R和B中做单独开
迭代，这样就可以将业务逻辑抽到上层，方便业务的快速发布和迭代。这样的架构对代码插桩
染色是否有影响呢？看下D中
实例化容器加载R的classLoader的实现：
发
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
private void initClassLoader(ClassLoader parentClassLoader, File appPat
try {
File[] extFile = appPath.listFiles((dir, name1) -> "ext"
.equals
AppExtClassLoader extClassLoader = null;
if (extFile != null && extFile.length > 0) {
File[] extJars = extFile[0].listFiles((dir, name1) -> name1
extClassLoader = new AppExtClassLoader(parentClassLoader, e
}
File unzipFile = Paths.get(path, appName).toFile();
ZipFileUtils.unzip(new ZipFile(appJar), unzipFile);
this.classLoader = new AppClassLoader(unzipFile, extClassLoader
} catch (Throwable e) {
throw new ContainerException("container constructor error init
```

## PDF 第9页

[查看原页](RAW.pdf#page=9)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
14
15
}
}
R和B是按 照
jar包 部 署 的， 初始 化 classLoader时分 别按
ext目录 和解 压后 应用目录创建
YardAppClassLoader ， 其父 classloader 就 是 D 使用 的 pandora 加 载 业 务 代 码 的
LaunchedURLClassLoader，也就是说通过自定义类加载的路径，使其在加载热部署代码时
按照
jar包解压的路径加载代码；不同的部署版本解压出来路径不一样，做到了代码隔离。对于
使用agent插桩，不管是D代码还是R
、B的热部署代码，生效逻辑并没有差别。实际插桩效果
也验证了这样的结论：
D插桩代码反编译：
R插桩代码反编译：
```

## PDF 第10页

[查看原页](RAW.pdf#page=10)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
2.2.2 代码改造
D采用 agent方 式， 在应用启 动时同 步启 动jvm agent并 常驻内存。主 要 改动docker file文
件：
step1: 在基 础 镜像
runtime.jar下:
中下 载 JaCoCo agent的文 件 ， 并 放 到 /home/admin/app/jacoco-
1 wget -c -O /home/admin/app/jacoco-runtime.jar "https://repo1.maven.org/m
step2: 在环境配置脚
本中
配置jvm启动参数：将JaCoCo agent参数放到-javaagent中，主
要核心参数包括agent的路径和插桩范围的白名单。这里将应用D
R和B代码相关
的类路径都
放进去，非白名单文件
不会被插桩，这能控制插桩范围，降
低插桩
对应用运
行
时的影响。这里
我们限制了预发和安全生产环境，通过采集分组隔离避免影响正式分组。
、
step3: 数据dump。在应用部署后JaCoCo
采集的数据到boolean[] jacoco
Data数组
据从内存采集下来分析，还需要定时dump数据。
已经对代码做插桩处理，类代码执
行
时会自动记录
中，数据会一直保存到下次重启，为了周期性将数
```

## PDF 第11页

[查看原页](RAW.pdf#page=11)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
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
/**
* 使用jacoco的数据结构做dump，返回dump是否成功
*
* @param filePath dump的位置
* @return 是否执
成功
行
*/
boolean jacocoDump(String filePath) throws IOException {
Agent iAgent = Agent.getInstance();
if (iAgent == null) {
DosaLogUtil.warnNew("Jacoco agent not found!");
return false;
}
AgentOptions agentOptions = buildOptions(filePath);
FileOutput fileOutput = new FileOutput();
fileOutput.startup(agentOptions, iAgent.getData());
fileOutput.writeExecutionData(true);
return true;
}
上述代码复用了JaCoCo的FileOutput类，JaCoCo也是依
赖
这个类的writeExecuti
onData()
实现采集数据写磁盘。采集的数据dump后上传到oss，按照日期做了归档。dump的周期是每
天凌晨，这样保证对dump数据做分析时代码是最新部署的。
至此我们实现了插桩并采集了应用D的安全生产环境的代码执
况，下面介绍采集后数据的使用。
行情况，考虑了自定义
部署的情
▐ 2.3 数据合并
```

## PDF 第12页

[查看原页](RAW.pdf#page=12)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
JaCoCo采集的是类的boolean[] jacoo
Data数据，一般用.exec后缀的文件保存。正如前面
介绍，jacoo
Data是按代码块标识的数组，并没有类信息，也就是说直接从JaCoCo采集的数
据无法计算类代码覆盖率，必须配合类的.class文件使用，因此就有：
详细执
覆盖率(.xml) = 类插桩执
行
行
文件(.exec) +
类原始编译文件(.class)
IDEA支持多种覆盖率数据，这里选
择
xml文件来记录代码详细执
行情况。想要获取
详细覆盖率
数据，我们要：
step1: 从oss下载采集的插桩代码执
文件；
行
step2: git下载最新master代码，编译生产.class文件；
step3: 使用JaCoCo的report功能，实现项目覆盖率的生成和导出；
step4: 上传覆盖率数据到oss，并清理代码缓存。
上述步骤中
oss上传和下载不再赘述，主要介绍代码git、maven编译和覆盖率report的方
案。
2.3.1 jGit代码到本地
java版本的git客户端jGit能实现代码的克隆，而我们这里使用了库token的方式，其优势是不
使用个人账号，不支持代码推送，满足我们对代码.class文件的提取需求。
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
/**
* 克隆代码仓库
*
* @param config 应用配置
* @return 本地仓库路径，失败返回null
*/
public String cloneRepository(CodeProfilerAppConfigDO config) {
String appName = config.getAppName();
String localRepoPath = buildLocalRepoPath(appName);
try {
String ciToken = kcUtil.decrypt(config.getCiToken());
GitCloneRequest cloneRequest = new GitCloneRequest()
.setRepoUrl(config.getGitUrl())
.setBranch(config.getDefaultBranch())
.setTargetDir(localRepoPath)
.setCiToken(ciToken);
GitHelper.clone(cloneRequest);
return localRepoPath;
} catch (Exception exception) {
LOGGER.error("cloneRepository:clone failed for app: " + appName, ex
return null;
}
}
```

## PDF 第13页

[查看原页](RAW.pdf#page=13)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
库token配置是应用维度的，具体配置加密存在配置中间价，使用时再拿出来解码使用，避免
泄漏。
2.3.2 本地跑maven
对已经下载的代码库，可以使用ProcessBuilder实现maven编译，但前提是服务器安装
配置
了maven。在base docker file中添加maven和maven settings.xml的下载，这样就可以在
服务器上用命令
的方式执
行
行
maven命令。
实际使用时使用了java.lang.ProcessBuilder，其提供了使用java执
心代码：
行
shell命令的能力，核
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
private static final String MAVEN
_
CMD = "/opt/apache-maven-3.9.11/bin/
private static final String MAVEN
_
COMPILE = "compile";
private static final String MAVEN
SKIP
_
_
TESTS = "
-DskipTests=true";
private static final String MAVEN
TEST
_
_
SKIP = "
-Dmaven.test.skip=true"
private static final String MAVEN
AUTO
CONFIG
_
_
_
INTERACTIVE = "
-Dautocon
private static final String MAVEN
PROJECT
BUILD
SOURCE
_
_
_
_
ENCODING = "
-Dp
/**
* Maven编译项目
*
* @param config 应用配置
* @param localRepoPath 本地仓库路径
* @return 成功返回true，失败返回false
*/
public boolean compileProject(CodeProfilerAppConfigDO config, String l
String appName = config.getAppName();
String[] commands = new String[] {
MAVEN
_
CMD, MAVEN
_
COMPILE, MAVEN
SKIP
_
_
TESTS, MAVEN
TEST
_
_
SKIP, MAVEN
_
MAVEN
PROJECT
BUILD
SOURCE
ENCODING
_
_
_
_
};
try {
int exitCode = MavenHelper.execute(commands, localRepoPath);
if (exitCode == 0) {
LOGGER.info("maven build succeeded for app: " + appName);
return true;
} else {
LOGGER.error("maven build failed with exit code:" + exitCode);
return false;
}
```

## PDF 第14页

[查看原页](RAW.pdf#page=14)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
29
30
31
32
33
} catch (IOException | InterruptedException exception) {
LOGGER.error("compileProject:maven build failed for app:" + appNam
return false;
}
}
经过maven编译，编译的class文件默认会放在target/classes；如果是多模块代码，则代码
会放在各自module下的target/classes，这时需要把各个模块的.class文件拷贝到一个目录
下，方便后续JaCoCo做report操作。
2.3.3 覆盖率报告生成
拿到了.exec采集数据和代码编译.class文件，最后一步就是将两者合并交给JaCoCo来生成详
细的代码覆盖率文件的report操作。
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
/**
* 创建XML格式的覆盖率报告
*
* @param execFileLoader 执
行数据加载器
* @param bundleCoverage 覆盖率分析结果
* @param xmlPath XML报告文件路径
* @throws Exception 创建失败
*/
private void createXmlReport(ExecFileLoader execFileLoader, IBundleCove
throws Exception {
final List<IReportVisitor> visitors = new ArrayList<>();
final XMLFormatter formatter = new XMLFormatter();
visitors.add(formatter.createVisitor(Files.newOutputStream(Paths.get
IReportVisitor reportVisitor = new MultiReportVisitor(visitors);
reportVisitor.visitInfo(execFileLoader.getSessionInfoStore().getInfos
execFileLoader.getExecutionDataStore().getCon
reportVisitor.visitBundle(bundleCoverage, null);
reportVisitor.visitEnd();
}
这里IReportVisitor接收采集的数据和类文件，在visitBundle()时生成代码覆盖率数据，最终
在指定文件目录下生成xml版本的报告。
xml的报告按应用维度生成，最后通过oss保存在各自应用目录下，使用日期作为报告名称。
```

## PDF 第15页

[查看原页](RAW.pdf#page=15)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
覆盖率详细数据按天生成，可以用这些数据直接导入IDEA中查看代码执
行情况，但这样还是太
繁琐
低效，接下来介绍如何将这些数据集成到IDEA插件中，直接在IDEA中查看采集的数据。
▐ 2.4 插件设计
IDEA插件的开
发
有一定门槛，涉及到很多intellij platform的概念，这里只做简单介绍，主要
还 是介 绍 插 件 功能 的设 计 。涉 及 到 的IDEA插 件 的概 念 是： Acti
on、projectService、
applicati
onConfigurable扩展点，详细可参考：IDEA插件开
发。
acti
on: 用于在IDEA内交互的
为处理，比
行
如显示代码覆盖数据/隐藏代码覆盖率数据；
projectService: 主要的插件处理逻辑，可将产品功能封装到进来；
applicati
onConfigurable: 插件配置面板，支持插件配置的修改和持久化；
这些插件概念在代码覆盖率插件开
发
中
有
都
涉及到，在实现部分会有具体介绍。
2.4.1 插件功能
插件要实现的功能包括：
打开&关
闭代码执
行
覆盖展示：手动打开或者关
闭代码的覆盖率数据展示；
数据自动/手动下载：在覆盖率数据展示时，自动下载oss的数据到本地(如果本地没有
数据)；
插件配置：支持配置插件相关
的参数，例如oss的配置、下载最近N天数据、缓存周期
载超时等；
数据缓存：支持将下载的数据缓存在本地，只要缓存未过期，优先使用本地数据。
缓存
、下
2.4.2 插件
实现
```

## PDF 第16页

[查看原页](RAW.pdf#page=16)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
插件交互逻辑主要实现以Action为主，正如前面介绍，AnAction是用户
主要实现了以下功能：
为处理的功能。插件
行
这 些 action、 service 和 configure 需 在 插 件 配 置中 注 册生 效 。 projectService 和
applicationConfigurable为IDEA的扩展点：
Action放在Actions标签下注册：
```

## PDF 第17页

[查看原页](RAW.pdf#page=17)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
2.4.3 插件效果
在打开的代码编辑器右键(mac
OS双指单击)，展示注册的action按
【隐藏刷新率】和【刷新率覆盖】三个功能按
钮。
钮，具备【显示刷新率】、
```

## PDF 第18页

[查看原页](RAW.pdf#page=18)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
在项目视图展示的是按
package统计的代码覆盖率数据，可以快速导航到覆盖率低的路径做代
码清理；中间编辑器
，红色标识未执
的左边框展示了代码行
的执
行情况，针对每
可执
行
行
的部分，绿色标识代
码有执
行
行
过，黄色标识部分覆盖，这里可用来判断线上代码实际执
的分
行
支；右侧是Coverage面板，详细展示了类、
方法、
行
和分支覆盖率数据，可快速筛选指定包路
径。
在顶部Tools下可以找到更多代码覆盖率的action，例如刷新数据、打开插件配置和展示覆盖率
数据信息等。以下为配置面板：
在面板上可以配置下载数据的oss配置，缓存有
效期
、用于分析的文件数等。以上即为插件的
核心功能，通过插件极大加速了无效代码的清理，使得代码清理准而快。
治理效果
基于代码执
行
的数据和可视化插件，代码清理工作
非常高效，列举批量代码清理工作的过程。
R代码清理：
```

## PDF 第19页

[查看原页](RAW.pdf#page=19)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
B代码清理：
通过类似上述的代码清理过程，对业务域内的主要的应用做无效代码清理的效果：
应用 代码基线 清理代码降
低
比例
B 21.5w 15.4w 71%
R 43.1w 18.7w 43%
D 25.2w 2.1w 8.3%
```

## PDF 第20页

[查看原页](RAW.pdf#page=20)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
其中B应用清理的效果最佳，因其与R应用存在较多代码冗余；R应用其次，目前主要的业务高
频迭代在R应用，代码量也是最大的，还
有一定清理空间；而D应用代码因被B应用和R应用所
依
赖
，所以最后清理，这部分工作
还在进
中。
行
收获与反思
通过代码插桩染色和执
行情况的采集，较好对D应用代码做了治理，中间过程有收获也走了弯
路。
过程收获：
探索了JaCoCo工作原理，学习其优秀
的代码设计(主要基于访问者模式，结合asm类代码
修改)，最终借鉴其框架实现了代码执
覆盖的采集；
行
D应用代码历史悠久，通过对执
行数据的分析和代码业务的判断，实现了对D应用无效代码
的规模化清理，整体过程对业务无感；
学习了IDEA插件开
发框架，完成自己第一个IDEA插件的开
发，过程中有各种探索，为了探
索IDEA的工作原理，debug过IDEA源码，感兴趣的可以去IDEA社区版git仓库查看（下文
附链接）。
走的弯路：
前期没有
深
入了解热部署类加载原理和版本管理，导致对部署代码的覆盖采集问题出现偏
差，误导了问题的定位方向；
对使用AI agent完整开
发IDEA组
件前期期望过高，利用AI从设计到代码开
发做完整插件
实
现，存在一些问题：
前期设计的方
案后续每做一次需求
调整，AI的修改都
有可能让代码设计更加复杂，这
种情况因token限制导致下次对话上下文丢失更加严重；
IDEA平台内部的代码实现代码对AI偏黑盒，经常在代码库检索不到，想让AI复用IDEA
内部接口功能较难实现；
对IDEA插件领域模型不熟悉的话，agent生成的代码逻辑自己都
不一定搞懂原理，更
别说后续做问题定位和插件升级
。
而最终版插件的实现方
案，还是人工通过调试IDEA社区版源码让IDEA的Coverage插
件逻辑白盒化，使用原生代码覆盖率的接口实现了插件核心逻辑，而像
bug的定位&修
复等工作使用AI确实
反而高效，算是“锦上添花”了。
采集数据基于安全生产环境，结合业务功能清理代码，基本不会影响线上核心链路，自是
采集过程没有完全覆盖线上请求，诸如冷链路、大促链路、老版本逻辑让人防不胜防，清
理过程也有遇到清理的类仍有少量流量的情况。
```

## PDF 第21页

[查看原页](RAW.pdf#page=21)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
刚来团队时就发现D应用代码有很多历史悠久的代码，当时就有做无效代码清理的想法，直到
我逐渐加深
对D代码和技术框架的原理，才真正着手做这件事。前期有
调研相关
产品，最终基
于D的情况做了技术方
案设计和代码的开
发，确实下线清理了
不少代码，也将在后续继续做治
理优化。虽然当前方
案只支持了D应用代码治理，也并非所有应用都需要做代码治理，但这套
方
案可以迁移到需要的其它业务，尤其是历史代码包袱重且难以重构的，希望能给需要的同学
提供一种可
方
案。
行
参考资料
JaCoCo agent：https://www.eclemma.org/jacoco/trunk/doc/agent.html
JaCoCo cli：https://www.eclemma.org/jacoco/trunk/doc/cli.html
Acti
on：https://plugins.jetbrains.com/docs/intellij/plugin-acti
ons.html?
from=DevkitPluginXmlInspecti
on
projectService：https://plugins.jetbrains.com/docs/intellij/plugin-
services.html?from=DevkitPluginXmlInspecti
on
applicati
onConfigurable：https://plugins.jetbrains.com/docs/intellij/plugin-
extensi
ons.html?from=DevkitPluginXmlInspecti
on#exploring-available-
extensi
ons
IDEA插件开
发：https://plugins.jetbrains.com/docs/intellij/plugins-quick-
start.html?from=DevkitPluginXmlInspecti
on
git仓库：https://github.com/JetBrains/intellij-
community/tree/pycharm/233.15619.17?tab=readme-ov-file#readme
团队介绍
本文作者星言，来自淘天集团-首页&信息流工程团队。团队负责淘宝首页和信息流的工程技
术。我们的目标是为数亿用户构建一个体验极致、
高并发、
高可用、
高效能的在线系
统；通过
工程架构和数据链路的升级，优化系
统性能、提升迭代效率、突破算法模型天花板；通过大模
型技术在用户理解、推荐算法、产品创
新的
深度应用，提升用户体验和流量效率。
巨大的用户流量、深度的商业思维、前沿的算法工程、核心的
迎你的加入！
系
统架构，种种挑战和机会也欢
```

## PDF 第22页

[查看原页](RAW.pdf#page=22)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
¤ 拓展阅读 ¤
3DXR技术 | 终端技术 | 音视频技术
服务端技术 | 技术质量 | 数据算法
大淘宝技术
大淘宝技术官方账号
967篇原创内容
公众号
阅读 1.7万
留言
写留言
还没有
留言，来写首评
```
