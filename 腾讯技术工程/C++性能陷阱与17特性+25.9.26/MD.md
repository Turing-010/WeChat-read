# 微信开发工程师总结的20条C++性能陷阱与实用特性，读起来很过瘾

来源：[RAW.pdf](RAW.pdf)，capture-001。

这是PDF文本层按物理页码转写，不是AI总结。图片未嵌入；图内文字、截图、公式、表格及代码排版可能未提取或不可靠；源PDF中存在的右侧裁切不补写。实际复核范围详见META.json。

## PDF物理页 1

微信开发⼯程师总结的         20条 C++性能陷阱与实⽤特性，读起来很过
瘾

腾讯技术⼯程  2025年9⽉26⽇   02:36⼴东25⼈


















 作者：尚晋的思考

 ⽂章分为上下篇，上篇介绍10个C++性能陷阱，下篇介绍10个C++实⽤特性。



   如果你让每个 C++⼯程师列出他们喜欢 C++的原因，那“掌控⼒”绝对是排在前⼏的特性。与 go、
   java 等垃圾回收语⾔的⼤道⾄简、python 等解释语⾔的⼩快灵不同，C++最⼤的魅⼒就是给予⼯
   程师对代码完全的掌控，每个 C++程序员仿佛都是⼈形编译器，不⽌要看懂代码表⾯的逻辑，甚
   ⾄要知道每⾏代码对应的汇编指令。优化代码也成了 C++⼯程师⽇常必备活动，正所谓“⼀杯茶，
   ⼀包烟，⼀段代码，优化⼀天”。在经历过⽆数个性能优化的⽇⽇夜夜后，笔者也总结了10中过招
   的性能陷阱，与诸位分享。



 性能陷阱主要分为两⼤类：“有成本抽象”和“与编译器作对”。前者是指在使⽤ C++的功能/
 库时需要注意的隐形成本，后者则是⼀些 C++新⼿可能会写出不利于编译器优化的代码。
 另外本⽂的顺序是由基础到进阶，读者可以根据⽬录直接跳到⾃⼰想看的部分。

  有成本抽象

 C++“信徒”们常常⿎吹 C++的“零成本抽象（Zero Cost Abstraction）”。然⽽对于“零成本抽
 象”这个概念存在很多误解。⽐如有的新⼿会认为：“使⽤          C++的任何特性都没有成本   ”。
 那显然是⼤错特错的，⽐如使⽤模版就会导致编译时间变慢的编译期成本，⽽且我花了
 21 天时间精通 C++的时间成本也是成本啊（狗头）。有些经验的 C++程序员会解释为”使
 ⽤ C++的任何特性都没有   运⾏时  成本 “，这也是对   C++最常⻅的误解。  C++的创始⼈
 Bjarne Stroustrup 是这样解释“零成本抽象“的：

  1. 你不会为任何你没有使⽤的特性付出任何成本。
  2. 对于你使⽤的特性，你只会付出最⼩运⾏时成本。

 简单来说，就是    C++不会背着你偷偷⼲坏事（⽐如垃圾回收），⽽你指定         C++⼲的活，
 C++会尽量在编译期做，保证在运⾏期只会做       “最少”的⼯作。连⼩学⽣都应该知道，      “最
 少”并不等于  “零”，所以 “零成本抽象  ”其实是⼀种谎⾔，   Google 的 C++负责⼈ Chandler
 Carruth 就曾经在 CppCon 2019 说过：C++根本不存在”零成本抽象“。

## PDF物理页 2

显然， C++的很多特性是有性能成本的，⽽且，这些成本往往出现在你               “没有写 ”的代码
⾥，即 C++帮你添加的隐形代码。作为 C++⼯程师，我们就必须了解每个特性会带来的性
能损耗，在做代码设计时尽量选择损耗⼩的特性。

⽽下⽂介绍的很多坑点，C++语⾔服务器 clangd 可以帮你实时检测出来并⾃动修复。

（⼀）虚函数

⽼⽣常谈的性能损耗，这⾥只介绍⼀下虚函数调⽤带来的成本：

1. 会多⼀次寻址操作，去虚函数表查询函数的地址。
2. 可能会破坏 cpu 流⽔线，因为虚函数调⽤是⼀次间接调⽤，需要进⾏分⽀预测。
3. 阻碍了编译器内联，⼤部分情况下，虚函数是⽆法被内联的（与前两条相⽐，⽆法内联
  才是虚函数性能损耗的主要来源）。

然⽽在实际⽣产环境中，可能很多的运⾏时多态是⽆法避免的，毕竟这是                 OOP 的基础特
性，因此对于虚函数我们也只能了解背后的成本⽽已。某些情况下我们可以使⽤编译期多
态来替代虚函数，⽐如  CRTP(Curiously  Recurring Template  Pattern)、Tempated Visitor
Pattern、Policy Based Design 等等，我的下⼀篇⽂章《C++独有的设计模式》中会介绍这
些技巧，敬请期待。

（⼆）隐形的拷⻉

也是⼀个⽼⽣常谈的性能损耗，这⾥主要介绍⼏个容易被疏忽的场景：

Member Initialization 构造函数





 class C {

  public:
   C(A a, B b): a_(a), b_(b){}
 private:
   A a_;
   B b_;
 }


 int main() {
   A a;
   B b;
 C c(a, b);
 }


如果  A、B 是⾮平凡的类，会各被复制两次，在传⼊构造函数时⼀次，在构造时⼀次。                C
的构造函数应当改为：





   C(A a, B b): a_(std::move(a)), b_(std::move(b)){}

## PDF物理页 3

这种写法是      clang-tidy 推荐的https://clang.llvm.org/extra/clang-tidy/checks/modernize/pass-
by-value.html#pass-by-value-in-constructors ，相⽐传 const 引⽤进来，如果外⾯也是传右
值，则完全没有拷⻉。

For 循环





 std::vector<std::string> vec;

 for(std::string s: vec){

   // ...
 }


这⾥每个 string 会被复制⼀次，改为         for(const std::string& s: vec)即可.

Lambda 捕获




 A a;
 auto f = [a]{};


lambda 函数在值捕获时会将被捕获的对象拷⻉⼀次，可以根据需求考虑使⽤引⽤捕获aut
o f = [&a]{};或者⽤ std::move 捕获初始化    auto f = [a = std::move(a)]{};（仅限 C++14 以
后）。

隐式类型转换





 std::unordered_map<int, std::string> map;

 for(const std::pair<int, std::string>& p: map){

   // ...
 }


这是⼀个很容易被忽视的坑点，这段代码⽤了                   const 引⽤，但是因为类型错了，所以还是
会发⽣拷⻉，因为        unordered_map element 的类型是   std::pair<const int, std::string>，所以
在遍历时，推荐使⽤ const auto&，对于 map 类型，也可以使⽤结构化绑定。

（三）隐形的析构

在 C++代码中，我们⼏乎不会主动去调⽤类的析构函数，都是靠实例离开作⽤域后⾃动析
构。⽽“隐形”的析构调⽤，也会导致我们的程序运⾏变慢：

复杂类型的析构

我们的业务代码中有这样⼀种接⼝





 int Process(const Req& req, Resp* resp) {

   Context ctx = BuildContext(req); // ⾮常复杂的类型

## PDF物理页 4

    int ret = Compute(ctx, req, resp); // 主要的业务逻辑
    PrintTime();
    return ret;
  }


  int Api(const Req& req, Resp* resp) {

    int ret = Process(req, resp);
    PrintTime();
  }


在⽇志中，Process 函数内打印的时间和               PrintTime 打印的时间竟然差了          20 毫秒，⽽我们
当时接⼝的总耗时也不过⼏⼗毫秒，我当时百思不得其解，还是靠我⽼板 tomtang ⼀语道
破先机，原来是析构 Context ⾜⾜花了 20ms。后⾯我们实现了 Context 的池化，直接将接
⼝耗时降了 20%。

平凡析构类型

如何定义类的析构函数也⼤有讲究，看下下⾯这段代码：





  class A {

   public:

    int i;

    int j;
    ~A() {};
  };


  A get() {

    return A{41, 42};
  }


get函数对应的汇编代码是：





  get():                                # @get()
          movq    %rdi, %rax
          movabsq $180388626473, %rcx             # imm = 0x2A00000029
          movq    %rcx, (%rdi)
          retq


⽽如果我能把析构函数改⼀下：





  class A {

   public:

    int i;

    int j;

    ~A() = default; // 注意这⾥
  };

## PDF物理页 5

 A get() {

   return A{41, 42};
 }


对应的汇编代码则变成了：





 get():                                # @get()
         movabsq $180388626473, %rax             # imm = 0x2A00000029
         retq


前者多了两次赋值，也多⽤了两个寄存器，原因是前者给类定义了⼀个⾃定义的析构函数
（虽然啥也不⼲），会导致类为不可平凡析构类型                (std::is_trivially_destructible)和不可平
凡复制类型（    std::is_trivially_copyable），根据 C++的函数调⽤ ABI 规范，不能被直接放
在返回的寄存器中（%rax），只能间接赋值。除此之外，不可平凡复制类型也不能作为编
译器常量进⾏编译器运算。所以，如果你的类是平凡的（只有数值和数字，不涉及堆内存
分配），千万不要随⼿加上析构函数！

关于⾮平凡析构类型造成的性能损耗，后⽂还会多次提到。

（四）滥⽤ std::shared_ptr

C++核⼼指南是这样推荐智能指针的⽤法的：

1. ⽤ std::unique_ptr或 std::shared_ptr表达资源的所有权。
2. 不涉及所有权时，⽤裸指针。
3. 尽量使⽤  std::unique_ptr，只有当资源需要被共享所有权时，再⽤        std::shared_ptr。

但是在实际代码中，⽤       std::shared_ptr的场景⼤概就是以下⼏种：

1. ⼩部分是因为代码作者是写 python 或者 java 来的，不会写没有 gc 的代码（⽐如 apache
  arrow 项⽬，所有数据全⽤     std::shared_ptr，像是被 apache 的 Java 环境给荼毒了）。
2. 绝⼤部分是因为代码作者是会写 C++的，但是太懒了，不想梳理内存资源模型。不得不
  说，  std::shared_ptr确实是懒⼈的福⾳，既保证了资源的安全，又不⽤梳理资源的所有
  权模型。
3. 很⼩⼀部分是因为确实需要使⽤         std::shared_ptr的场景（不到 10%）。我能想到的必须
  ⽤ std::shared_ptr 的场景有：异步析构，缓存。除此之外想不出任何必须的场景，欢迎⼩
  伙伴们在评论区补充。

实际上，   std::shared_ptr的构造、复制和析构都是⾮常重的操作，因为涉及到原⼦操作，
std::shared_ptr是要⽐裸指针和 std::unique_ptr慢 10%～ 20%的。即使⽤了 std::shared_ptr
也要使⽤ std::move 和引⽤等等，尽量避免拷⻉。

std::shared_ptr还有个陷阱是⼀定要使⽤    std::make_shared<T>()⽽不是std::shared_ptr<T>(n
ew T)来构造，因为后者会分配两次内存，且原⼦计数和数据本身的内存是不挨着的，不
利于 cpu 缓存。

## PDF物理页 6

（五）类型擦除：std::function 和 std::any

std::function，顾名思义，可以封装任何可被调⽤的对象，包括常规函数、类的成员函数、
有 operator()定义的类、 lambda 函数等等，当我们需要存储函数时             std::function ⾮常好
⽤，但是 std::function 是有成本的：

1. std::function 要占⽤ 32 个字节，⽽函数指针只需要    8 个字节
2. std::function 本质上是⼀个虚函数调⽤，因此虚函数的问题 std::function 都有，⽐如⽆法
  内联
3. std::function 可能涉及堆内存分配，⽐如 lambda 捕获了⼤量值时，⽤ std::function 封装会
  需要在堆上分配内存

因此我们只应在必须时才使⽤           std::function，⽐如需要存储⼀个不确定类型的函数。⽽在
只需要多态调⽤的，完全可以⽤模版静态派发：





 template <typename Func>

 void Run(Func&& f){
   f();
 }


std::any 同理，⽤类型擦除的机制可以存储任何类型，但是也不推荐使⽤。

（六）std::variant 和 std::optional

我在我的另⼀篇⽂章《         C++17 在业务代码中最好⽤的⼗个特性              》⼤肆吹捧了⼀波
std::variant 和  std::optional，但是说实话，C++的实现还是有些性能开销的，这⾥以
std::optional 为例介绍：

1. 必须的多余内存开销：简单来说，std::optional有两个成员变量，类型分别为 bool 和 T，
  由于内存对齐的原因，        sizeof(std::optional)会是 sizeof(T)+alignof(T)，对于简单的类型，
  sizeof(std::optional)甚⾄会是 sizeof(T)的两倍。相⽐之下， rust 语⾔的 option 实现则有
  null pointer optimization，即如果⼀个类的合法内存表⽰⼀定不会全部字节为零，⽐如
  std::reference_wrapper，那就可以零开销地表⽰ std::optional，⽽ C++由于需要兼容 C 的
  内存对齐，不可能实现这项优化
2. c++标准要求如果 T 是可平凡析构的（见上⽂析构的部分），std::optional            也必须是平凡
  析构的，但是 gcc 在 8.0.0 之前的实现是有 bug 的，所有 std::optional都被设置为了⾮平
  凡类型，所以⽤      std::optional 作为⼯⼚函数的返回值是由额外性能开销的。
3. 对 NRVO（返回值优化）不友好，见下⽂           NRVO 的部分。

（七）std::async

std::async 是⼀个很好⽤的异步执⾏抽象，但是在使⽤的时候可能⼀不⼩⼼，你的代码就
变成了同步调⽤：

不指定 policy

std::async 的接⼝是：

## PDF物理页 7

  template< class Function, class... Args >

  std::future<std::invoke_result_t<std::decay_t<Function>, std::decay_t<Args>...>>

      async( Function&& f, Args&&... args );


  template< class Function, class... Args >

  std::future<std::invoke_result_t<std::decay_t<Function>, std::decay_t<Args>...>>

      async( std::launch policy, Function&& f, Args&&... args );


其中   std::launch 类型包括两种：std::launch::async异步执⾏和           std::launch::deferred懒惰执
⾏，如果你使⽤第⼀种接⼝不指定                  policy，那么编译器可能会⾃⼰帮你选择懒惰执⾏，也
就是在调⽤ future.get()的时候才同步执⾏。

不保存返回值

这是 c++的 std::async 的⼀个⼤坑点，⾮常容易踩坑，⽐如这段代码：





  void func1() {

  // ...
  }


  void func2() {

  // ...
  }


  int main() {

  std::async(std::launch::async, func1);

  std::async(std::launch::async, func2);
  }


在这段代码⾥，        func1 和  func2 其实是串⾏的！因为 std::async 会返回⼀个               std::future，⽽
这个   std::future 在析构时，会同步等待函数返回结果才析构结束。这也是上⽂                              “隐形的析
构”的另外⼀种表现。正确的代码应当⻓这样：





  auto future1 = std::async(std::launch::async, func1);

  auto future2 = std::async(std::launch::async, func2);


更  奇  葩  的  是  ，  只  有     std::async 返  回  的    std::future 在  析 构时  会  同  步  等  待  ，
std::packaged_task，std::promise 构造的   std::future 都不会同步等待，实在是让⼈⽆⼒吐
槽。

关于   std::async 等等  C++多线程⼯具，在我之后的⽂章《现代                     C++并发编程指南》会介
绍，敬请期待。

## PDF物理页 8

 与编译器作对

众所周知，现代编译器是⾮常强⼤的。⽑主席曾经说过：要团结⼀切可以团结的⼒量。⾯
对如此强⼤的编译器，我们应该争取做编译器的朋友，⽽不是与编译器为敌。做编译器的
朋友，就是要充分利⽤编译器的优化。⽽很多优化是有条件的，因此我们要争取写出优化
友好的代码，把剩下的⼯作交给编译器，⽽不是⾃⼰胡搞蛮搞。

（⼋）返回值优化 NRVO（Named Return Value Optimization)

当⼀个函数的返回值是当前函数内的⼀个局部变量，且该局部变量的类型和返回值⼀致
时，编译器会将该变量直接在函数的返回值接收处构造，不会发⽣拷⻉和移动，⽐如：





 #include <iostream>


 struct Noisy {

   Noisy() { std::cout << "constructed at " << this << '\n'; }

   Noisy(const Noisy&) { std::cout << "copy-constructed\n"; }

   Noisy(Noisy&&) { std::cout << "move-constructed\n"; }

   ~Noisy() { std::cout << "destructed at " << this << '\n'; }
 };


 Noisy f() {
   Noisy v = Noisy();
 return v;
 }
 void g(Noisy arg) { std::cout << "&arg = " << &arg << '\n'; }


 int main() {
   Noisy v = f();
   g(f());
 }


这段代码中，函数 f()满⾜ NRVO 的条件，所以             Noisy 既不会拷⻉，也不会 move，只会被
构造和析构两次，程序的输出：





 constructed at 0x7fff880300ae

 constructed at 0x7fff880300af

 &arg = 0x7fff880300af

 destructed at 0x7fff880300af

 destructed at 0x7fff880300ae


滥⽤ std::move

⾃从  C++11 加⼊ std::move 语义之后，有些      “⾃以为是”的程序员会到处添加            move。在这
些情况下，std::move 是根本没⽤的：

1. 被 move 的对象是平凡类型。

## PDF物理页 9

2. 被 move 的对象是⼀个常量引⽤。

⽽在某些情况下，move 反⽽会导致负优化，⽐如阻碍了 NRVO：





  Noisy f() {
    Noisy v = Noisy();
    return std::move(v);
  }


还是上⾯的代码，只不过返回值被改成                     move ⾛，结果就多了两次 move             构造和两次析
构，反⽽得不偿失：





  constructed at 0x7ffc54006cdf
  move-constructed
  destructed at 0x7ffc54006cdf

  constructed at 0x7ffc54006cdf
  move-constructed
  destructed at 0x7ffc54006cdf

  &arg = 0x7ffc54006d0f

  destructed at 0x7ffc54006d0f

  destructed at 0x7ffc54006d0e


⼯⼚返回 std::optional

同样的，使⽤ std::optional 也可能会阻碍 NRVO 优化：





  std::optional<Noisy> f() {
    Noisy v = Noisy();
    return v;
  }


因为返回值类型不对应，因此应当改为





  std::optional<Noisy> f() {

    std::optional<Noisy> v;
    v = Noisy();
    return v;
  }


为了性能牺牲了部分可读性。

（九）尾递归优化

## PDF物理页 10

尾递归优化是函数式语⾔常⽤的⼀种优化，如果某个函数的最后⼀步操作是调⽤⾃身，那
么编译器完全可以不⽤调⽤的指令(call)，⽽是⽤跳转(jmp)回当前函数的开头，省略了新开
调⽤栈的开销。然⽽由于 C++的各种隐形操作，尾递归优化不是那么好实现。我曾经在知
乎上看到这样⼀个问题：https://www.zhihu.com/question/552352098。题主的函数⻓这样：





 unsigned btd_tail(std::string input, int v) {

     if (input.empty()) {

         return v;

     } else {

         v = v * 2 + (input.front() - '0');

         return btd_tail(input.substr(1), v);
     }
 }


直接 return ⾃身的调⽤，如果在函数式语⾔就是⼀个标准的尾递归，然⽽，实际执⾏的代
码是：





 unsigned btd_tail(std::string input, int v) {

     if (input.empty()) {

         return v;

     } else {

         v = v * 2 + (input.front() - '0');

         auto temp = btd_tail(input.substr(1), v);

         input.~string(); // 注意这⾥

         return temp;
     }
 }


由于在 return 前 C++有隐形的析构操作，所以这段代码并不是尾递归。⽽需要析构的本质
原因是    std::string 不是可平凡析构的对象，解决办法也很简单，换成                    std::string_view 就好
了





 unsigned btd_tail(std::string_view input, int v) {

     if (input.empty()) {

         return v;

     } else {

         v = v * 2 + (input.front() - '0');

         return btd_tail(input.substr(1), v);
     }
 }

## PDF物理页 11

std::string_view 是可平凡析构的，所以编译器根本不需要调⽤析构函数，这也是上⽂推荐
尽量选⽤可平凡析构对象的另⼀个理由。我的下⼀篇⽂章《C++函数式编程指南》会介绍
C++函数式编程，敬请期待。

（⼗）⾃动向量化优化

现代   CPU ⼤部分都⽀持⼀些向量化指令集如 SSE                、 AVX 等，向量化指的是          SIMD 操作，
即⼀个指令，多条数据。在某些条件下，编译器会⾃动将循环优化为向量化操作：

1. 循环内部访问的是连续内存
2. 循环内部没有函数调⽤，没有              if 分⽀
3. 循环之间没有依赖

举个例⼦，下⽅的代码⾮常的向量化不友好：





  enum Type { kAdd, kMul };

  int add(int a, int b) { return a + b; }

  int mul(int a, int b) { return a * b; }


  std::vector<int> func(std::vector<int> a, std::vector<int> b, Type t) {

  std::vector<int> c(a.size());

  for (int i = 0; i < a.size(); ++i) {

      if (t == kAdd) {
        c[i] = add(a[i], b[i]);
      } else {
        c[i] = mul(a[i], b[i]);
      }
    }
  return c;
  }


既有 if，⼜有函数调⽤，⽽如果我们通过模版 if 和内联函数，这两条都可以规避：





  enum Type { kAdd, kMul };

  inline __attribute__((always_inline)) int add(int a, int b) { return a + b; }

  inline __attribute__((always_inline)) int mul(int a, int b) { return a * b; }


  template <Type t>

  std::vector<int> func(std::vector<int> a, std::vector<int> b) {

  std::vector<int> c(a.size());

  for (int i = 0; i < a.size(); ++i) {

      if constexpr (t == kAdd) {
        c[i] = add(a[i], b[i]);
      } else {
        c[i] = mul(a[i], b[i]);
      }

## PDF物理页 12

   }
 return c;
 }


这样就变成了向量化友好的代码。我们团队正在基于                apache arrow 做⼀些向量化计算的
⼯作，后续也会有⽂章分享关于向量化优化的详细介绍。










下篇介绍10个C++在业务代码中最好⽤的特性。



  ⾃从步⼊现代    C++时代开始， C++语⾔标准形成了三年⼀个版本的惯例：         C++11 标志着现代
  C++的开端，C++14 在 11 的基础上查缺补漏，并未加⼊许多新特性，⽽         C++17 作为 C++11 后
  的第⼀个⼤版本，标志着现代 C++逐渐⾛向成熟。WXG 编译器升级到 gcc7.5 已有⼀段时间，笔
  者所在项⽬组也已经将全部代码升级到          C++17。在使⽤了  C++17 ⼀年多之后，笔者总结了
  C++17 在业务代码中最好⽤的⼗个特性。



注 1：本⽂只包含 wxg 的 gcc7.5 ⽀持的特性，Execution Policy, File System等暂不⽀持的
特性不包含在内。

注  2： 本 ⽂ 只 包 含 应 ⽤ 于 业 务 逻 辑 的 特性， Fold  Expression, Mathematical  Special
Functions等适⽤于元编程和科学计算的特性并不包含。

笔者将这些特性⼤体上分为三类：语法糖、性能提升和类型系统。



 语法糖

这⾥所说的语法糖，并不是严格意义上编程语⾔级别的语法糖，还包括⼀些能让代码更简
洁更具有可读性的函数和库：

结构化绑定

c++17 最便利的语法糖当属结构化绑定。结构化绑定是指将 array、            tuple 或 struct 的成员
绑定到⼀组变量*上的语法，最常⽤的场景是在遍历              map/unordered_map 时不⽤再声明⼀
个中间变量了:





 // pre c++17

 for(constauto& kv: map){

 constauto& key = kv.first;

 constauto& value = kv.second;

 // ...

## PDF物理页 13

 }


 // c++17

 for(constauto& [key, value]: map){

 // ...
 }


*: 严格来说，结构化绑定的结果并不是变量，c++标准称之为名字/别名，这也导致它们不
允许被    lambda 捕获，但是     gcc 并没有遵循      c++标准，所以以下代码在           gcc 可以编译，
clang 则编译不过





 for(const auto& [key, value]: map){
     [&key, &value]{
         std::cout << key << ": " << value << std::endl;
     }();
 }


在 clang 环境下，可以在 lambda 表达式捕获时显式引⼊⼀个引⽤变量通过编译





 for(const auto& [key, value]: map){
     [&key = key, &value = value]{
         std::cout << key << ": " << value << std::endl;
     }();
 }


另外这条限制在        c++20 中已经被删除，所以在          c++20 标准中    gcc 和 clang 都可以捕获结
构化绑定的对象了。

std::tuple 的隐式推导

在 c++17 以前，构造      std::pair/std::tuple时必须指定数据类型或使⽤       std::make_pair/std::mak
e_tuple函数，c++17 为   std::pair/std::tuple新增了推导规则，可以不再显示指定类型。





 // pre c++17

 std::pair<int, std::string> p1{3.14, "pi"s};

 auto p1 = std::make_pair(3.14, "pi"s);


 // c++17

 std::pair p3{3.14, "pi"s};


if constexpr

if constexpr 语句是编译期的     if 判断语句，在 C++17 以前做编译期的条件判断往往通过复
杂SFINAE机制或模版重载实现，甚⾄嫌麻烦的时候直接放到运⾏时⽤                             if 判断，造成性能

## PDF物理页 14

损耗，if constexpr ⼤⼤缓解了这个问题。⽐如我想实现⼀个函数将不同类型的输⼊转化为
字符串，在 c++17 之前需要写三个函数去实现，⽽ c++17 只需要⼀个函数。





  // pre c++17

  template <typename T>

  std::string convert(T input){

      return std::to_string(input);
  }


  // const char*和string进⾏特殊处理

  std::string convert(const char* input){

      return input;
  }
  std::string convert(std::string input){

      return input;
  }






  // c++17

  template <typename T>

  std::string convert(T input) {

      if constexpr (std::is_same_v<T, const char*> ||

                    std::is_same_v<T, std::string>) {

          return input;

      } else {

          return std::to_string(input);
      }
  }

if 初始化语句

c++17 ⽀持在 if 的判断语句之前增加⼀个初始化语句，将仅⽤于 if 语句内部的变量声明在
if 内，有助于提升代码的可读性。且对于                      lock/iterator 等涉及并发    /RAII 的类型更容易保证
程序的正确性。





  // c++ 17

  std::map<int, std::string> m;

  std::mutex mx;

  externbool shared_flag; // guarded by mx


  int demo()
  {
      if (auto it = m.find(10); it != m.end()) { return it->second.size(); }

      if (char buf[10]; std::fgets(buf, 10, stdin)) { m[0] += buf; }

      if (std::lock_guard lock(mx); shared_flag) { unsafe_ping(); shared_flag = false; }

## PDF物理页 15

      if (int s; int count = ReadBytesWithSignal(&s)) { publish(count); raise(s); }

      if (constauto keywords = {"if", "for", "while"};

          std::ranges::any_of(keywords, [&tok](constchar* kw) { return tok == kw; }))
      {
          std::cerr << "Token must not be a keyword\n";
      }
  }

  性能提升

std::shared_mutex

shared_mutex  是 c++的原⽣读写锁实现，有共享和独占两种锁模式，适⽤于并发⾼的读场
景下，通过        reader 之前共享锁来提升性能。在 c++17 之前，只能⾃⼰通过独占锁和条件
变量⾃⼰实现读写锁或使⽤ c++14 加⼊的性能较差的                              std::shared_timed_mutex 。以下是通
过  shared_mutex  实现的线程安全计数器：





  // c++17

  class ThreadSafeCounter {

  public:

    ThreadSafeCounter() = default;


  // Multiple threads/readers can read the counter's value at the same time.

  unsigned int get() const {

      std::shared_lock lock(mutex_);

      return value_;
    }


  // Only one thread/writer can increment/write the counter's value.

  unsigned int increment() {

      std::unique_lock lock(mutex_);

      return ++value_;
    }


  // Only one thread/writer can reset/write the counter's value.

  void reset() {

      std::unique_lock lock(mutex_);

      value_ = 0;
    }


  private:

  mutablestd::shared_mutex mutex_;

  unsignedint value_ = 0;
  };

std::string_view

## PDF物理页 16

std::string_view顾名思义是字符串的        “视图”，类成员变量包含两个部分：字符串指针和字
符串⻓度，std::string_view 涵盖了 std::string 的所有只读接⼝。std::string_view 对字符串不
具有所有权，且兼容 std::string 和 const char*两种类型。

c++17 之前，我们处理只读字符串往往使⽤                  const std::string&，std::string有两点性能优
势:

1. 兼容两种字符串类型，减少类型转换和内存分配。如果传⼊的是明⽂字符串                                    const char
   *, const std::string&需要进⾏⼀次内存分配，将字符串拷贝到堆上，⽽                    std::string_view
   则可以避免。
2. 在处理⼦串时，        std::string::substr也需要进⾏拷贝和分配内存，⽽           std::string_view::subst
   r则不需要，在处理⼤⽂件解析时，性能优势⾮常明显。





  // from https://stackoverflow.com/a/40129046

  // author: Pavel Davydov


  // string_view的remove_prefix⽐const std::string&的快了15倍

  string remove_prefix(const string &str) {

  return str.substr(3);
  }
  string_view remove_prefix(string_view str) {

    str.remove_prefix(3);

  return str;
  }


  static void BM_remove_prefix_string(benchmark::State& state) {

  std::string example{"asfaghdfgsghasfasg3423rfgasdg"};

  while (state.KeepRunning()) {

      auto res = remove_prefix(example);

      // auto res = remove_prefix(string_view(example)); for string_view

      if (res != "aghdfgsghasfasg3423rfgasdg") {

        throwstd::runtime_error("bad op");
      }
    }
  }

std::map/unordered_map try_emplace

在向std::map/unordered_map 中插⼊元素时，我们往往使⽤                emplace，  emplace 的操作是
如果元素 key 不存在，则插⼊该元素，否则不插⼊。但是在元素已存在时，                                emplace 仍会
构造⼀次待插⼊的元素，在判断不需要插⼊后，⽴即将该元素析构，因此进⾏了⼀次多余
构造和析构操作。        c++17 加⼊了     try_emplace，避免了这个问题。同时             try_emplace 在参
数列表中将 key 和 value 分开，因此进⾏原地构造的语法⽐emplace                     更加简洁





  std::map<std::string, std::string> m;

  // emplace的原地构造需要使⽤std::piecewise_construct，因为是直接插⼊std::pair<key, value>

## PDF物理页 17

 m.emplace(std::piecewise_construct,

            std::forward_as_tuple("c"),

            std::forward_as_tuple(10, 'c'));


 // try_emplace可以直接原地构造，因为参数列表中key和value是分开的

 m.try_emplace("c", 10, 'c')


同时，  c++17 还给  std::map/unordered_map加⼊了insert_or_assign函数，可以更⽅便地实
现插⼊或修改语义。



 类型系统

c++17 进⼀步完备了 c++的类型系统，终于加⼊了众望所归的类型擦除容器(Type Erasure)
和代数数据类型(Algebraic Data Type)

std::any

std::any是⼀个可以存储任何可拷⻉类型的容器，             C 语⾔中通常使⽤      void*实现类似的功
能，与  void*相⽐，   std::any具有两点优势：

1. std::any更安全：在类型 T 被转换成      void*时，T 的类型信息就已经丢失了，在转换回
  具体类型时程序⽆法判断当前的            void*的类型是否真的是 T，容易带来安全隐患。⽽              st
  d::any会存储类型信息，      std::any_cast是⼀个安全的类型转换。
2. std::any管理了对象的⽣命周期，在        std::any析构时，会将存储的对象析构，⽽           void*
  则需要⼿动管理内存。

std::any应当很少是程序员的第⼀选择，在已知类型的情况下，                  std::optional, std::variant
和继承都是⽐它更⾼效、更合理的选择。只有当对类型完全未知的情况下，才应当使⽤                              st
d::any，⽐如动态类型⽂本的解析或者业务逻辑的中间层信息传递。

std::optional

std::optional<T>代表⼀个可能存在的 T 值，对应 Haskell 中的     Maybe 和 Rust/OCaml 中的
option，实际上是⼀种     Sum Type。常⽤于可能失败的函数的返回值中，⽐如⼯⼚函数。
在 C++17 之前，往往使⽤      T* 作为返回值，如果为        nullptr则代表函数失败，否则T*        指
向了真正的返回值。但是这种写法模糊了所有权，函数的调⽤⽅⽆法确定是否应该接管                              T
*的内存管理，⽽且T*       可能为空的假设，如果忘记检查则会有 SegFault 的⻛险。





 // pre c++17

 ReturnType* func(const std::string& in) {

     ReturnType* ret = new ReturnType;

     if (in.size() == 0)

         returnnullptr;

     // ...

     return ret;

## PDF物理页 18

 }


 // c++17 更安全和直观

 std::optional<ReturnType> func(const string& in) {
     ReturnType ret;
     if (in.size() == 0)

         return nullopt;

     // ...

     return ret;
 }

std::variant

std::variant<T, U, ...>代表⼀个多类型的容器，容器中的值是制定类型的⼀种，是通⽤的
Sum Type，对应 Rust 的  enum。是⼀种类型安全的         union，所以也叫做      tagged union。与
union相⽐有两点优势：

1. 可以存储复杂类型，⽽ union 只能直接存储基础的 POD 类型，对于如                   std::vector和std::
  string就等复杂类型则需要⽤户⼿动管理内存。
2. 类型安全，variant 存储了内部的类型信息，所以可以进⾏安全的类型转换，c++17 之前
  往往通过    union+ enum 来实现相同功能。

通过使⽤    std::variant<T, Err>，⽤户可以实现类似    Rust 的std::result，即在函数执⾏成功
时返回结果，在失败时返回错误信息，上⽂的例⼦则可以改成:





 std::variant<ReturnType, Err> func(const string& in) {
     ReturnType ret;
     if (in.size() == 0)

         return Err{"input is empty"};

     // ...

     return {ret};
 }


需要注意的是，c++17 只提供了⼀个库级别的 variant 实现，没有对应的                   模式匹配(Pattern
Matching)机制，⽽最接近的      std::visit⼜缺少编译器的优化⽀持，所以在 c++17 中           std::var
iant并不好⽤，跟     Rust 和函数式语⾔中出神⼊化的          Sum Type 还相去甚远，但是已经有许
多围绕   std::variant的提案被提交给 c++委员会探讨，包括模式匹配，              std::expected等等。

总结⼀下，c++17 新增的三种类型给 c++带来了更现代更安全的类型系统，它们对应的使
⽤场景是：

   std::any适⽤于之前使⽤     void*作为通⽤类型的场景。
   std::optional适⽤于之前使⽤   nullptr代表失败状态的场景。
   std::variant适⽤于之前使⽤   union的场景。


 总结

## PDF物理页 19

 以上是笔者在⽣产环境中最常⽤的         c++17 特性，除了本⽂描述的⼗个特性外，      c++17 还
 添加了如lambda 值捕获*this, 钳夹函数 std::clamp(), 强制检查返回值[[nodiscard]]等⾮常易
 ⽤的特性，本⽂篇幅有限不做赘述，欢迎有兴趣的读者⾃⾏探索。



























        腾讯技术⼯程
        腾讯技术官⽅号。腾讯技术创新、前沿领域发布解读平台。
        690篇原创内容


   公众号



















阅读 5736





留⾔


写留⾔

## PDF物理页 20

还没有留⾔，来写⾸评
