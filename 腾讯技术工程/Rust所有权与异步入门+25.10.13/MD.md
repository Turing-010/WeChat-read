# 24小时快速入门大热语言Rust！学不会来找我

来源：[RAW.pdf](RAW.pdf)，capture-001。

这是PDF文本层按物理页码转写，不是AI总结。图片未嵌入；图内文字、截图、公式、表格及代码排版可能未提取或不可靠；源PDF中存在的右侧裁切不补写。实际复核范围详见META.json。

## PDF物理页 1

24⼩时快速⼊⻔⼤热语⾔            Rust！学不会来找我


原创 腾讯程序员    腾讯技术⼯程    2025年10⽉13⽇   02:36⼴东  1460⼈
















作者： richardyao



  最近⼏年，Rust在业界的使⽤越来越多，本篇⽂章从Rust核⼼语法等基础知识⼊⼿，进⽽
  详细的介绍Rust语⾔不同于其它语⾔的思维⽅式，最后通过⼀个实战的项⽬，带⼤家快速
  ⼊⻔Rust编程语⾔。



最近⼏年 ，  Rust在 业界的 使⽤越来越多。  在  Windows内 核中  (win32kbase_rs.sys)、Linux内
核中  、Chromium浏览器中都有   Rust的 身影， AWS S3也使⽤  rust重构了他们的 核⼼存储服
务ShardStore，Azure的CTO甚⾄说 "Speaking of languages, it's time to halt starting
any new projects in C/C++ and use Rust for those scenarios where a non-GC
language is required."。 从下⾯的Google Trends也可以看的 出来 ，Rust的 热度正在 上升，
并且增⻓很快，可以说现在  是  学习Rust最好的  时  机  。

## PDF物理页 2

本篇⽂章从   Rust核⼼语法等基础知识⼊⼿，进⽽详细的 介绍              Rust语⾔不同于 其它语⾔的思维
⽅式，最后通过⼀  个 实战的 项⽬，带⼤ 家快速⼊⻔           Rust编程语⾔。

有C++、  Golang、Python这 些语⾔基础的话，⼤ 部分知识都可以迁移过去，再加上⼤ 模型
的 辅助，  24⼩时 快速⼊⻔，是  有 可能达成的  。


       腾讯技术⼯程
       腾讯技术官⽅号。 腾讯技术创新、 前沿领域发 布解读平台。
       690篇原创内 容


 公众号



⼀、基础篇

1.1 Rust的安装与基本⼯具的使⽤

Rust的 安装直接参考官⽹的 ⽂档，这  ⾥ 不做更具体的 介绍了：

https://www.rust-lang.org/tools/install

在  国  内 使⽤Rust的话，可以通过     https://rsproxy.cn/ ⽹站提供的 镜像，更⽅便快捷的 安装
Rust以及下载相关的     crate等。

Rust对 应的 编译器是   rustc，但是  这  个  ⼤ 家平时 使⽤的 并不多，更多的  是 通过包管理⼯具
cargo等来 管理、构建项⽬。      cargo常⽤命令如下：





 cargo build
 cargo build --release
 cargo clippy
 cargo run
 cargo run -- --help
 cargo clean
 cargo check
 cargo doc
 cargo expand      # 需要使⽤cargo install cargo-expand先安装


Rust⽇常开发 可以使⽤    vscode + rust-analyzer插件。

1.2 通过greplite⼩程序熟悉Rust的语⾔特点

在  这  ⾥ ，我们使⽤⼀  个 简单greplite程序来 介绍  Rust语⾔的 特点。

先使⽤  cargo new greplite 命令创建⼀  个   binary的crate，然后在   main.rs中 输⼊下⾯的
代码：





 use std::env;

 use std::fs::File;

## PDF物理页 3

  use std::io::{self , BufRead, BufReader};


  fn main() -> io:: Result <()> {

      let args = env::args().collect::<   Vec<_>>();

      if args.len() <   3 {

          eprintln!( "Usage: greplite <search_string> <file_path>");

          std::process::exit(1);
      }


      let search_string = &args[1];

      let file_path = &args[2];


      run(search_string, file_path)
  }


  fn run(search_string: &  str, file_path: & str) -> io::  Result<()> {

      let file = File::open(file_path)?;

      let reader = BufReader::new(file);


      for line in  reader.lines() {

          let line = line?;

          if line.contains(search_string) {

              println!  ("{line}");
          }
      }


      Ok(())
  }


这  个 程序 的  第 ⼀  个  参 数  是  要搜索 的 字符串，第⼆ 个  参 数  是  搜索 的  ⽂件，⽐如说要搜索
src/main.rs⽂件中 包含       main函数  的 ⾏，可以如下执⾏：





  $ cargo run -- main src/main.rs
      Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.00s
       Running `target/debug/greplite main src/main.rs`
  fn main() -> io::Result<()> {


这  个 ⼩程序⼀ 共就       30⾏代码，但是 知识点还挺多的 ，先整体介绍⼀ 下：

a)、 use类似于     C++中  的  include，⽤来引⽤        std标准库⾥ ⾯的        module；

b)、 fn⽤来 定义⼀  个 函数 ，        main函数  是 整个程序的⼊⼝；

c)、 -> 表示函数  的 返回值，          io::Result<()>      表示返回的  是  个       Result  ，通过⽂档，或者
vscode   代    码    跳    转     的     ⽅  式，    可    以    看    到std::io::Result<T>      是     基     于
std::result::Result<T, std::io::Error>定义的  ⼀  个 新类型

https://doc.rust-lang.org/   std/ io/type.Result.html

## PDF物理页 4

 pub type Result<T> = std::result::Result<T, std::io::Error>;


同时  std::result::Result     是  ⼀  个 枚举：





 pub enum Result<T, E> {

     Ok(T),

     Err(E),
 }


Result表示的 值，可以是 表示成功的            Ok，也可以是 表示失败的          Err。

上⾯  pub type Result<T> = std::result::Result<T, std::io::Error>;                  只
是   把std::io::Result     的   错  误  类  型  固  定  成std::io::Error   ，  表  示  只  会   返  回
std::io::Error   类型的 错误。

d)、 io::Result<()>    中  的() ，表示的  是  ⼀  个   tuple，这  个 tuple没有 任何元素，也称为
unit；

e)、 关于  main函数  的 返回类型：

https://doc.rust-lang.org/reference/crates-and-source-files.html?highlight=main#main-
functions

f)、let args = env::args().collect::<Vec<_>>();            中  的env::args()返回的 值，
实现了   Iterator这  个trait，关于  Rust中  的 迭代器，后⾯还会 重点来 讲，这  个             collect是 把迭代
器的列表收集起来 ，构造成⼀  个            Vec。

这  个 语句还有 下⾯⼏种写法，都是 可以的 ：





 let args = env::args().collect::<Vec<_>>();

 let args = env::args().collect::<Vec<String>>();

 let args: Vec<String> = env::args().collect();

 let args: Vec<_> = env::args().collect();


Rust的 类型推断是 ⾮常强⼤  的 ，如果后⾯对              args的 使⽤能确定     args的 类型的话，也可以完全
写成：





 let args = env::args().collect();


⽐如说如果 有  函 数      fn print_args(args: &Vec<String>) {}           ， 同 时  后 ⾯调⽤ 了
print_args(&args)的话，       args的 定义就完全不需要类型注解了。

## PDF物理页 5

另外，通过     let定义的 变量，默认是 不可变的  (         immutable)，如果要修改的话，需要显示的 使
⽤ let mut args = env::args().collect();

这  ⾥ 还有  ⼀  个 知识点，我们在 前⾯并没有 通过           use语句引⼊Vec，那为 什么不报错呢？

https://doc.rust-lang.org/std/prelude/index.html

Rust编译器预先已经包含了          std中 部分常⽤的 组件，这样代码会 更简洁⼀ 些。

g) 、  args.len()   中      的len() 是 Vec<String>   的    成   员   函    数       https://doc.rust-
lang.org/std/vec/struct.Vec.html#method.len；

h)、 let search_string = &args[1];       和 let file_path = &args[2];      这  ⾥ 定义
了两个引⽤，是  对      Vec<String>中  对 应元素的 不可变的 借⽤；

args[1]下标操作，在 运⾏时  会         check下标是 否越界，但是 由于 前⾯判断了⻓ 度，因此这  ⾥
的 运⾏时  的越界检查，编译器通常会 优化掉。

i)、 下⾯是调⽤     run函数 ，另外这  ⾥  是  ⼀  个  expression， expression的 值作为 整个     main函数
的 返回值；

j)、 第19⾏ let file = File::open(file_path)?;        打开⼀  个 ⽂件，这  个 语句中  的       ?是
⼀  个 语法糖，这 条语句等价于 ：





     let file = match File::open(file_path) {

         Ok(f) => f,

         Err(err) => return Err(From::from(err)),
     };


https://doc.rust-lang.org/reference/expressions/operator-expr.html?highlight=question#the-
question-mark-operator

h)、 第 20⾏  let reader = BufReader::new(file);file实现了          Read这  个  trait，然后
BufReader是  在 Read这  个 trait的 基础上，做了⼀ 层封装，实现了带缓存的读，并在 此基础
上，提供了     lines()等便捷的 ⽅法。

https://doc.rust-lang.org/std/fs/struct.File.html#impl-Read-for-File

BufReader实现了    BufRead这  个 trait，因此在    use std::io::BufRead;     之后，可以调⽤
这  个trait对 应的 lines()等⽅法。

https://doc.rust-lang.org/std/io/struct.BufReader.html#impl-BufRead-for-BufReader

i)、 第22⾏  for line in reader.lines() {       lines()函数 返回了⼀  个 迭代器，然后          for
line in的 ⽅式来 遍历这  个 迭代器，这  个 迭代器对 应的          Item为

## PDF物理页 6

 type Item = Result<String, Error>


https://doc.rust-lang.org/std/io/struct.Lines.html#associatedtype.Item

这  个 被称为 trait的Associated type。

j)、  这  个 迭代器的Item是  ⼀  个Result，因此第   23⾏使⽤?运算符把其转换成了普通的               String;

k)、 第24⾏ if line.contains(search_string) {判断line是 否包含要搜索的 ⼦串；

l)、 第25⾏ println!("{line}");    打印输出，和     println!("{}", line);    等价，前⾯
这 种⽅式被称为     named parameters：

https://doc.rust-lang.org/std/fmt/index.html#named-parameters

另外 println!包括前⾯的    eprintln!最后的  这  个  !，表示这  是  ⼀  个 宏。

Rust中 ，函数 不⽀持可变参数 ，通过宏的 ⽅式来 实现可变参数  。

m)、 最后第   29⾏，  Ok(())这  个expression作为 整个 函数  的 返回值表示成功。

n)、 同时 我们注意到      search_string和file_path都是  &String类型的 ，  run函数  的 参数  &str是
什么⻤？

类⽐于   C++中  的 string和string_view，同时  string到 string_view可以通过   string的 operator
string_view进⾏隐式转换：

https://en.cppreference.com/w/cpp/string/basic_string/operator_basic_string_view.html

在rust中 ， String到&str也可以进⾏隐式转换：

https://doc.rust-lang.org/std/string/struct.String.html#impl-Deref-for-String

https://doc.rust-lang.org/std/ops/trait.Deref.html#deref-coercion



  思考题：    1、在上⾯的     30⾏代码中，⼀共涉及到哪些             trait？Read、 BufRead、 Iterator、
  FromIterator、From、 Deref、Termination、Drop2、在上⾯的     30⾏代码中，⼀共有哪些迭
  代器iterator？std::env::Args、std::io::Lines



从上⾯的  这  个 ⼩例⼦中 ，我们也能⼀ 窥         Rust程序的 特点：

1、 代码⻛格，下划线⼩写命名的 形式；

2、 倾向于 使⽤   trait，使⽤组合的 ⽅式来 实现程序的功能；

3、 迭代器   iterator功能挺强⼤  的 ；

4、 Rust学习曲线确实很陡峭，         30⾏代码竟然涉及这么多语法。

## PDF物理页 7

1.3 Rust中组织数据的            3种⽅式

在 Rust中 ，我们可以使⽤            struct来 组织数 据。





  struct Person {

      first_name:   String ,

      last_name:   String ,

      age: i32,
  }


也可以使⽤       tuple( Rust中  的  tuple和  python中  的   tuple概念是  ⼀ 致的  )：





  let person_info = (  "Harry", "Potter"   , 18);

  let first_name = person_info.0;

  let (first_name, _, _) = person_info;


Rust中  的  enum表示的 可以是  ⼀  个 集合类型中  的 任意⼀ 种：





  enum WebEvent {

      // An enum variant without any data.
      PageLoad,
      // An enum variant with a string slice.

      KeyPress(char  ),

      // An enum variant with a struct.

      Click { x:   i32, y:  i32 },

      // An enum variant with an owned String.

      Paste(String  ),
  }


  impl WebEvent {

      fn describe  (&self ) {

          matchself   {

              WebEvent::PageLoad =>     println!("Page loaded"   ),

              WebEvent::KeyPress(c) =>      println!("Key pressed: {}", c),

              WebEvent::Click { x, y } => println!(       "Clicked at: ({}, {})"   , x, y),

              WebEvent::Paste(s) =>     println!("Pasted: {}"   , s),
          }
      }
  }


enum通常配合        match在  ⼀起使⽤。

1.4 Rust中的     Ownership

## PDF物理页 8

Rust中  的 ownership规则：





  1. Each value in Rust has an owner.
  2. There can only be one owner at a time.
  3. When the owner goes out of scope, the value will be dropped.


通过  ownership的  机  制 实现  RAII，当变量离开作⽤域的  时 候，会 被释放或者                    drop掉。

Rust在 默认的 情况下，是         move语义的 ，⽐如说：





  let a = vec![1, 2, 3];

  let b = a;

  println!("{:?}", a);

  println!("{:?}", b);   // error[E0382]: borrow of moved value: `a`


但是如果对 应的 类型实现了            Copy这  个  trait的话，默认就会 ⾛        copy的 语义：





  let a = 1;

  let b = a;

  println!("{:?}", a);

  println!("{:?}", b);


https://doc.rust-lang.org/std/marker/trait.Copy.html

Rust中  为很多简单类型都⾃动 实现了              Copy这  个  trait。

Copy和  Clone的 区别：





  #[derive(Copy, Clone)]

  struct Point {

     x: i32,

     y: i32,
  }


在 上⾯  Point的 定义中 ，由于       i32同时 实现了     Copy和  Clone这 两个   trait，因此他们组合在  ⼀起，
Point也能实现这 两个      Trait。





  #[derive(Clone)]

  struct PointList {

      points: Vec<Point>,
  }

## PDF物理页 9

⽽PointList中 ，由于Vec只实现了Clone这 两个    trait，因此 PointList也只能实现Clone这 个  trait，
不能实现Copy。   Copy和 Clone的 区别，就类似于 浅拷⻉和 深拷⻉的 区别，上⾯Point的 定义，两
个 变量都是 分配在 栈上的 ，浅拷⻉和 深拷⻉没有 区别，因此              Point可以同时 实现Copy和   Clone这
两个 trait；⽽下⾯PointList的 定义中 ， Vec在 栈上只记录了元信息(       pointer, capacity, length)，
Vec的元素是存放在 堆上的 ，只能深拷⻉，因此只实现了Clone这 个               trait。

1.5 Rust中的引⽤和借⽤




 1. At any given time, you can have either one mutable reference or any number of immut
 2. References must always be valid.


由于 Rust中 默认是   move语义的 ，在  有  的 场景下，我并不想转移         ownership，这 种情况下，
可以通过引⽤来 借⽤。

引⽤分为 两种，⼀ 种是      immutable引⽤，⼀ 种是   mutable的引⽤。

通过 immutable的引⽤，借⽤者不能修改；通过            mutable的引⽤，借⽤者可以对  这  个 变量做
任何的修改，⽐如说赋值、         swap等，唯⼀  的  ⼀  个 限制 就是 要保证这  个 变量的完整性。

Rust的 安全机  制 要求引⽤在 任何时 候都必须有  有 效；同时 ，限制            mutable引⽤和  immutable
引⽤不能同时存在 ：你可以有 多个          immutable的引⽤；也可以有  ⼀  个     mutable的引⽤；但是
不允许有 多个   mutable的引⽤，也不允许mutable的引⽤和          immutable的引⽤同时存在  。

思考：为 什么对 同⼀  个 变量的      mutable引⽤和  immutable引⽤不能同时存在 ？思考下⾯的例
⼦：





 fn main() {

     let mut v = vec![1, 2, 3, 4];

     let first = &v[0];

     v.push(5);   // error[E0502]: cannot borrow `v` as mutable because it is also borr

     println!("first element: {}", first);
 }

1.6 trait

Rust中  的trait类似于golang中  的interface，Rust中 通过trait定义共同的 ⾏为  。⽐如说咱们定
义Shape形状这样的     trait，所有  的 形状都有 ⾯积：





 trait Shape {

     fn area(&self) -> f64;
 }


圆和  ⻓ ⽅形都能实现    Shape形状这  个 Trait：

## PDF物理页 10

  struct Circle {

      radius: f64  ,
  }


  impl  Shape for  Circle {

       fn area(&self  ) -> f64 {

          std::f64  ::consts::PI * self   .radius * self.radius
      }
  }


  struct Rectangle   {

      width: f64  ,

      height: f64  ,
  }


  impl  Shape for  Rectangle {

       fn area(&self  ) -> f64 {

          self.width *    self.height
      }
  }


有 了这 些定义之后，就可以实现编译时  的 类型约束：





  fn print_area1<S: Shape>(shape: &S) {

       println!("The area is: {}", shape.area());
  }


  fn print_area2(shape: &   impl Shape) {

       println!("The area is: {}", shape.area());
  }


上⾯这 两种实现的 ⽅式是 等价的 ，                  impl只是  ⼀  个 语法糖：

https://doc.rust-lang.org/stable/reference/types/impl-trait.html

也可以实现运⾏时  的 多态：





  fn print_area3(shapes: &[&dyn Shape]) {

       for shape in  shapes {

          println!  ( "The area is: {}"  , shape.area());
      }
  }


调⽤上⾯⼏个 ⽅法的例⼦：

## PDF物理页 11

  fn main() {

      let circle = Circle { radius:    5.0 };

      let rectangle = Rectangle {

          width:  10.0 ,

          height:  4.0 ,
      };


      print_area1(&circle);
      print_area2(&rectangle);


      let shapes:  Vec <&dyn Shape> =  vec![&circle, &rectangle];
      print_area3(&shapes);
  }

1.7 迭代器

Rust中  的 迭代器由      Iterator这  个 trait来 表示，表示会 产⽣⼀  个 序列的 值：

https://doc.rust-lang.org/std/iter/trait.Iterator.html

这  个trait只有  ⼀  个 Required的 ⽅法     next，当    next返回   None的  时 候，表示序列结束：





  // Required method

  fn next(&mut self ) ->  Option<Self::Item>;


可以直接调⽤         next⽅法来  ⼀  个  ⼀  个  的获取值，但是 更多的 场景下是 使⽤标准库中提供的
adapter和  consume⽅法。

rust中  的 迭代器有 以下特点：

a)、 laziness

https://doc.rust-lang.org/std/iter/index.html#laziness

b)、 infinity

https://doc.rust-lang.org/std/iter/index.html#infinity

c)、 ⾼效，性能很⾼，和 ⼿写              for循环性能是  ⼀ 致的  。





  struct Fibonacci  {

      current: u64 ,

      next: u64,
  }


  impl Fibonacci {

      fn new() -> Fibonacci {

          Fibonacci { current: 0, next:    1 }

## PDF物理页 12

      }
  }


  implIteratorfor Fibonacci {

      type Item = u64;


      fn next(&mutself) -> Option<Self::Item> {

          let next_number = self.current + self.next;

          self.current = self.next;

          self.next = next_number;

          Some(self.current)
      }
  }


  fn main() {

      let fib_iterator = Fibonacci::new();


      println!("The first 10 Fibonacci numbers are:"  );

      for number in fib_iterator.take( 10) {

          println!("{}", number);
      }


      let fib_vec: Vec<u64 > = Fibonacci::new().take(15 ).collect();

      println!("\nThe first 15 numbers collected into a vector:");

      println!("{:?}", fib_vec);
  }

1.8 闭包

Rust中  的 闭包能够     capture环境中  的 值，根据        capture的 ⽅式不同，闭包也分别实现了不同的
trait，如果是 普通的        borrow来   capture的话，实现了         Fn，如果是      mut  borrow来   capture的
话，实现了      FnMut，如果是      move consume了变量的话，实现              FnOnce，看下⾯的例⼦：





  fn main() {

      let s = String::from("hello");

      let f1 = || &s;

      println!("{}", f1());

      println!("{}", f1());
  }


如上⾯的 代码       f1是  ⼀  个 闭包，  capture了变量s的引⽤，编译器⾃动 帮这  个 闭包实现了                         Fn的
trait， 这  个  闭包可以调⽤多次。  我们也可以看到                    rust标准库 中     Fn这  个  trait的  定义 是   fn
call(&self, args: Args) -> Self::Output;，传递的  是     self的引⽤，因此才可以调⽤多次。





  fn main() {

      let mut s = String ::from("hello");

## PDF物理页 13

     let mut f2 = || s += "world";
     f2();
     //println!("{}", s);
     f2();
     println!("{}", s);
 }


如上⾯的 代码，       f2也是  ⼀  个 闭包，    mut borrow了  s，因此编译器⾃动 帮这  个 闭包实现了
FnMut这   个 trait， 注 意 ， 上 ⾯  的  代 码  中  ，如果 注释掉  中  间  的       println!的 话，  会  报
error[E0502]:  cannot  borrow  s  as  immutable  because  it  is  also
borrowed as mutable     错误，   f2是 变量s的  ⼀  个   mut引⽤，要满⾜        s引⽤的 限制规则。
FnMut在  标准库 中   是   这 样定 义 的  ：    fn call_mut(&mut self, args: Args) ->
Self::Output;，可以看到第⼀  个 参数  是  &mut self。





 fn main() {

     let s = String::from("hello");

     let f3 = || s;

     println!("{}", f3());

     //println!("{}", f3());  // error[E0382]: use of moved value: `f3`
 }


上⾯的 代码中     f3成为 了  s的  owner，实现了     FnOnce这  个 trait，f3只能调⽤⼀次，第⼆次调⽤
的 话会   报  use  of moved   value的   错  误  信  息  。FnOnce在   标 准库  中    的   定  义  ：fn
call_once(self, args: Args) -> Self::Output;           ，  self是 move的  这  种调⽤⽅
式，因此只能调⽤⼀次。

同时 ，编译器为 实现了         Fn的 闭包，也同时 实现了         FnMut和  FnOnce；实现了      FnMut的 闭包也
同时 实现了    FnOnce。

https://doc.rust-lang.org/std/ops/trait.Fn.html

https://doc.rust-lang.org/std/ops/trait.FnMut.html

https://doc.rust-lang.org/std/ops/trait.FnOnce.html

1.9 Sync & Send

Rust中  的 并发 安全，是 通过      Sync和 Send这 两个    trait来 体现的  。 Send表示的 含义是 ，变量可
以跨越线程的 边界进⾏传递；            Sync表示的 含义是 ，变量可以多线程同时 访问。

这  ⾥ 通过⼀  个 简单的例⼦，演示下          Sync & Send如何保证并发 安全的 ：





 use std::sync::Arc;

 use std::sync::Mutex;

 use std::thread;

## PDF物理页 14

fn test1() {

    letmut   a =  vec!  [1, 2, 3];


    let handler = std::thread::spawn(move || {

        a.push(   4 );
    });


    handler.join().unwrap();
}


fn test2() {

    letmut   a =  vec!  [1, 2, 3];


    thread::scope(|s| {
        s.spawn(|| {
               println!("hello from the first scoped thread");


            a.push(4);
        });
    });


    a.push(  5 );
}


fn test3() {

    let a1 = Arc::new(vec![1       , 2 , 3]);

    let a2 = a1.clone();


    let handler = thread::spawn(        move || {

        println!    ("a1 {:?}", a1);
    });


    println!   ("a2 {:?}", a2);


    handler.join().unwrap();
}


fn test4() {

    let a1 = Arc::new(Mutex::new(        vec![1, 2, 3]));

    let a2 = a1.clone();

    let a3 = a1.clone();


    let handler1 = thread::spawn(        move || {

        let  mut  lock_guard = a1.lock().unwrap();

        lock_guard.push(4);
    });


    let handler2 = thread::spawn(        move || {

        let  mut  lock_guard = a2.lock().unwrap();

        lock_guard.push(4);
    });


    handler1.join().unwrap();

## PDF物理页 15

      handler2.join().unwrap();
      println!("a3 {:?}"   , a3.lock().unwrap());
  }


  fn main() {
      test1();
      test2();
      test3();
      test4();
  }

1.10 async & await

Rust的 异步编程，被称为 ⽆栈协程，先看⼀  个 简单的例⼦：





  use anyhow::Result  ;

  use serde::Deserialize;


  #[derive(Deserialize, Debug)]

  struct Joke {

      joke: String  ,
  }


  #[tokio::main]

  asyncfn main() ->   Result <()> {

      let res = reqwest::get("https://geek-jokes.sameerkumar.website/api?format=json"          ). a

      let joke = res.json::<Joke>().    await ?;

      println!("{}"  , joke.joke);

      Ok(())
  }


使⽤  cargo expand命令，上⾯的 代码，                main⼤ 概展开成下⾯的样⼦：





  fn main() -> Result  <()> {
      tokio::runtime::Builder::new_multi_thread()
          .enable_all()
          .build()
          .expect(  "Failed building the Runtime")

          .block_on(  async {

              let   res = reqwest::get(  "https://geek-jokes.sameerkumar.website/api?format=

              let   joke = res.json::<Joke>().await?;

              println!  ("{}", joke.joke);

              Ok(())
          })
  }


从上⾯的 代码可以看到，代码中 ⾸先构建了⼀  个                              tokio的  runtime，然后       block_on在 某个

## PDF物理页 16

async块上进⾏执⾏。

async/await把 Rust程序分割成了两个 世界，在              async/ await的 上下⽂⾥ ，不能调⽤阻塞的
函数 ，不然会 卡住异步运⾏时            tokio的执⾏和调度。

为 了弄清楚    async/ await到底⼲了啥，咱们⾸先看下上⾯代码中  的 其中  ⼀ ⾏代码：





 let res = reqwest::get("https://geek-jokes.sameerkumar.website/api?format=json").await


这 ⾏代码可以拆成两⾏：





 let res_future = reqwest::get("https://geek-jokes.sameerkumar.website/api?format=json"

 let res = res_future.await?;


在 vscode⾥ ⾯，把⿏标悬停在         res_future上，可以看到       vscode给出的 类型注解是 ：





 let res_future: impl Future<Output = Result<Response, Error>>


可以看到    res_future实现了    Future这  个trait，但是   res_future具体的 类型不知道，只知道他
实现了   Future这  个trait。

async只是  ⼀  个 语法糖：





 async fn test() {

     println!("This is a test function.");
 }


 fn test2() -> impl Future<Output = ()> {

     async {

         println!("This is a test function.");
     }
 }


async  的     本  质，    实    际    上     是     编    译    器    把reqwest::get("https://geek-
jokes.sameerkumar.website/api?format=json")           编译成了⼀  个 状态机 ，然后这  个
状态机 实现了      Future这  个 trait，所以这  ⾥   get返回的  时 候，实际上并没有  发 出任何http请
求，只是 返回了⼀  个 状态机 ，这  个 状态机 实现了              Future这  个 trait，仅此⽽已。 理论上来 说，
也可以⼿写⼀  个     struct，实现同样的 状态机 ，只是  这  个 过程会 特别的复杂，编译器直接帮忙
咱们做了：

https://doc.rust-lang.org/stable/reference/items/functions.html#r-items.fn.async

## PDF物理页 17

⼀ 些⼿动 实现    Future的例⼦：

https://docs.rs/futures-util/latest/futures_util/future/struct.Select.html#impl-Future-for-
Select

https://docs.rs/tokio/latest/tokio/time/struct.Timeout.html#impl-Future-for-Timeout

await的 本质，实际上是  “不停的  ”调⽤上⾯状态机  的               poll⽅法，驱动 状态机 不停的往前⾛，
直到  Ready为 ⽌。

https://doc.rust-lang.org/stable/reference/expressions/await-expr.html?highlight=await#r-
expr.await.effects

rust异步编程的 核⼼，就是         Future这  个trait：





 pub trait Future {

     type Output;


     // Required method

     fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output>;
 }


 pub enum Poll<T> {
     Ready(T),
     Pending,
 }


上⾯  Future这  个trait的 定义中 ，   poll函数  的 第⼀  个 参数  是  个Pin<&mut Self>    的 类型，什么
是 Pin，为 什么需要     Pin呢？

还   是   要  从  上  ⾯async⽣  成   的   状  态   机   说 起，reqwest::get("https://geek-
jokes.sameerkumar.website/api?format=json")           这  个 函数  会 返回⼀  个  对 象，这  个
对 象实现了     Future trait，这  个  对 象是  ⼀  个 状态机 ，内 部维护这  个 请求的执⾏状态，然后
await的  时 候，会  “不停”的    poll，驱动 状态机往前⾛，这  个 状态机  内 部会 维护很多的 状态，
⽐如说   tcp socket收发  的  buffer，以及   buffer已经使⽤的  ⼤ ⼩等。换句话说，这  个 状态机  是
⼀  个 ⾃引⽤的  对 象，状态机  内 部有  ⼀ 些       buffer，然后状态机  内 部有  ⼀ 些指针指向这 些           buffer
的 某些位置等。 状态机  是 ⾃引⽤的 ，就要求这  个 状态机 不能在  内存中 随意的 移动 ，如果移动
的话，⾃引⽤指针的 指向就错了，指向了别的 位置。                         Rust对  这  个问题的 解法就是 加⼀ 层
Pin，对  这  个 状态机  的 所有  的 访问，都是 通过        Pin这  个 智能指针来 访问的 ，       Pin限制 了这  个 状
态机 不能移动  和复制  。

异步任务 的  取消：不 .await了，不           poll了，异步 的  请求也就取消了，⽐如说前⾯提到
的   https://docs.rs/futures-util/latest/futures_util/future/struct.Select.html 当其 中  的  ⼀  个 已
经 Ready之后，另外⼀  个 就⾃动  的 取消了。


        腾讯技术⼯程
        腾讯技术官⽅号。 腾讯技术创新、 前沿领域发 布解读平台。

## PDF物理页 18

        690篇原创内 容


  公众号



⼆、思维篇

每个 语⾔都有 ⾃⼰的 特点，⽐如说              Golang推崇通过消息的 ⽅式共享内存，                 Python语⾔中  的
list comprehensions是  ⼀ 种强⼤且简洁的创建列表的 ⽅法等，这  ⾥ 介绍下                     Rust语⾔的思维
⽅式。

2.1 expression

在 Rust中 ，推崇简洁，表达式可以作为 值进⾏赋值，或者作为 返回值：





  fn foo(x: usize) -> usize {
      x
  }


表达式可以赋值：





  let x = if 3 > 2 {

   1

  } else {

   2
  };


前⾯的   greplite的 main函数 ，也可以写成：





  fn main() -> io::Result<()> {

      let mut args = env::args().skip(1);


      let (search_string, file_path) = match (args.next(), args.next(), args.next()) {

          (Some(s), Some(f), None) => (s, f),
          _ => {
              eprintln!("Usage: greplite <search_string> <file_path>");

              std::process::exit(1)
          }
      };


      run(&search_string, &file_path)
  }

2.2 split

## PDF物理页 19

由于  Rust中 ownership及引⽤规则的 限制 ，有 些对 象会  有          split的 操作，⽐如说      Vec， split成
两个 ，每个 只修改Vec的  ⼀ 部分元素，这样整体还是 安全的  。

再⽐如说    socket，可以   split成⼀  个 只收数 据的   socket，⼀  个 只发  数 据的  socket，这样可以实
现在  ⼀  个 线程中 只收数 据，在  ⼀  个 线程中 只发  数 据。

https://docs.rs/tokio/latest/tokio/net/struct.TcpStream.html#method.into_split

2.3 ⽆处不在的      Option和  Result

就像在   golang中 ， if err != nil {}和if someData != nil {}⽆处不在  ⼀样，在  Rust中 ， Option
和 Result也是 随处可⻅；      Option和 Result都是  enum，如果都⽤       match来 进⾏判断的话，代
码的 递进深度会⽐较深，另外代码也看起来  会很冗余。

为 此 Rust为 Option和 Result提供了很多便利的 操作。

a)、question mark operator

https://doc.rust-lang.org/reference/expressions/operator-expr.html#r-expr.try

b)、is_some()、 is_none()、 is_ok()、is_err()便捷函数

c)、let else赋值操作





 let a = Some(1);

 let Some(b) = a else {

   return;
 };


d)、  和 迭代器的 互操作等

https://doc.rust-lang.org/std/option/#method-overview

https://doc.rust-lang.org/std/result/#method-overview

熟练掌握上⾯的 ⽅法，会让代码更简洁。

2.4 match的不仅仅是       enum

在 Rust中 ， match通常⽤来 作⽤在      enum上，然后每个 分⽀判断enum的每个 变体。

但是  match不仅仅可以⽤在       enum上，在 其它的 场景中 ，        match也能发 挥⼤ 作⽤。

另外，   match是 exhaustive的 ，需要写出所有  的 可能的 分⽀。

https://github.com/yaozongyou/rust-24-hour-crash-
course/blob/bdf5bc30a67fe6b5649a8fff7cc25e2e0d19a0e6/mini-redis/src/connection.rs#L112

https://doc.rust-lang.org/rust-by-example/flow_control/match.html

## PDF物理页 20

2.5 宏强⼤的超乎想象

宏的 3种场景：

a)、 类似于 println!

本质是 编译器⼀ 些规则的 替换

https://doc.rust-lang.org/stable/reference/macros-by-example.html?
highlight=hygiene#hygiene

b)、 类似于 前⾯例⼦中  的   #[tokio::main]

本质是  在 编译期，把对 应注解的 函数  的      Token Stream给到这  个 宏，然后这  个 宏，在 编译期
⽣成新的 代码。

⼀  个 简单这 种宏的例⼦，可以参考下⾯的  这 篇⽂章:

乐学 Rust：100⾏代码实现简易集成测试框架

c)、 类似于 Debug宏

https://doc.rust-lang.org/std/fmt/derive.Debug.html

本质是  在 编译期，把对 应注解的  对 应的      struct的Token Stream给到这  个 宏，然后这  个 宏，在
编译期⽣成新的 代码。

2.6 通过传递消息的⽅式共享内存

在Golang中 ，推崇通过消息的 ⽅式共享内存。 同样，在            Rust中 ，也⽀持这 种编程的 模式。

考虑对 象从⼀  个存储桶搬迁到另外的存储桶这 种场景：

## PDF物理页 21

⼀ 种操作流程的 组织形式可能类似于 上图，左边的           routine，调⽤ list objects的 接⼝，或者
从⽂件列表中获取所有  的  对 象列表，然后再把这 些对 象，放⼊到⼀  个          channel中 ；然后右边
的copy的routine，具体执⾏  copy每个  对 象的  动 作。

list操作和 具体的 copy操作在 流程上做了分离，代码简洁清晰。

上⾯这  个 流程有  ⼀  个 ⼩问题就是 ，当遇到⼤  对 象的  时 候，⼤  对 象可能会 成为  ⻓ 尾的 瓶颈，因
为每个  对 象都是单routine拷⻉的  。 流程上可以优化如下：


















如上图，再加⼀ 层，真正的      copy操作只在   worker中 进⾏处理，在  copy这  ⼀ 层，把每个  对 象
的copy任务，拆分成多个     task，如果对 象⽐较⼩的话，对 应⼀  个    task，对 象⽐较⼤  的话，采
⽤分块上传的 ⽅式，拆分成多个        task。 上图中  的 第⼆个channel⾥ ⾯的 消息就是每个   task任
务，同时每个    task任务中  会 包含另外⼀  个channel，这  个worker通过这  个channel告知copy
的routine对 应的task的完成情况。

通知这 种流程的 组织形式，解决了⼤  对 象⻓ 尾的问题。 流程依然清晰简洁。

在Rust中 同样可以实现上⾯的  这 种流程模式。

不过对⽐Rust和  Golang中channel和select的 体验，由于 Rust不是像golang那样，在 语⾔本
身⽀持 channel和select，因此体感上，   Rust稍微差了⼀ 丢丢。

2.7 和C++⼀致的内存模型

Rust采⽤和 C++⼀ 致的  内存模型，都是 通过    atomic原⼦操作来 体现的 ，  C++上的 经验可以直
接迁移到  Rust上。

⽐如说，考虑配置热加载的 场景，⼀ 种可能的 实现是  这样的 ，⼀  个           atomic的pointer指向当
前的 配置，然后有  ⼀  个 线程从本地或者通过      sdk周期性从外部取最新的 配置，然后再atomic
的 更新pointer指向最新的 配置。

这  ⾥  有  个问题是 ，原来  的 配置何时释放的问题(   safe memory reclamation)，在C++中 ，通
常使⽤ hazard pointer来 解决，在Rust中 也类似，也有  hazard pointer。

不过最新的  这 种问题的 解决⽅式，建议使⽤《          Concurrent Deferred Reference Counting
with Constant-Time Overhead》这 篇paper介绍的 ⽅法，使⽤更⽅便：

https://github.com/cmuparlay/concurrent_deferred_rc

## PDF物理页 22

对 应 Rust的 crate:

https://github.com/aarc-rs/aarc

关于  Rust内存模型的 书籍推荐。

https://marabos.nl/atomics/

2.8 Interior Mutability Pattern

由于  Rust的 ownership以及引⽤规则的 限制 ，在 写代码的  时 候，要想好各种数 据结构，是 否
会 跨多线程访问，如果跨多线程访问的话，可能要使⽤                          interior mutability pattern，所有  的
struct的 函数都是  &self，⽽不是  &mut self。

参考例⼦：

https://github.com/yaozongyou/rust-24-hour-crash-
course/blob/bdf5bc30a67fe6b5649a8fff7cc25e2e0d19a0e6/mini-redis/src/store.rs#L45

2.9 build.rs在编译期执⾏各种操作

crate有  个build.rs脚本，可以获取代码仓库的            git信息，编译     c/ c++程序等：

https://doc.rust-lang.org/cargo/reference/build-scripts.html

https://github.com/yaozongyou/rust-24-hour-crash-
course/blob/bdf5bc30a67fe6b5649a8fff7cc25e2e0d19a0e6/mini-redis/build.rs

2.10 迭代器真的很好⽤

在 Rust中  ， 适 当 的  使 ⽤ 迭 代 器 会 让代 码 更 简 洁 。  各 种         collection(Vec、  HashMap、
BTreeMap等)都能通过迭代器来 遍历，              Result和 Option等也都能和 迭代器相互转换等，迭代
器也有 特别多的      adapter。

从 C++转到   Rust的话，可以尝试多使⽤下迭代器。

https://doc.rust-lang.org/std/iter/

之前  greplite程序，可以改下成：





  fn run(search_string: &str, file_path: &str) -> io::Result<()> {

      let file = File::open(file_path)?;

      let reader = BufReader::new(file);


      reader.lines().try_for_each(|line| {
          let line = line?;

          if line.contains(search_string) {

              println!("{}", line);
          }

## PDF物理页 23

          Ok::<(), _>(())
      })
  }


或者





  fn run(search_string: & str, file_path: & str) -> io::Result <()> {

      let file = File::open(file_path)?;

      let reader = BufReader::new(file);


      reader
          .lines()
          .collect::<io::Result<Vec <_>>>()?
          .into_iter()
          .filter(|line| line.contains(search_string))
          .for_each(|line| println! ("{}" , line));


      Ok(())
  }

2.11 想定义个全局变量真不容易

关于 全局变量，下⾯这 篇⽂章总结的 ⾮常好:

https://www.sitepoint.com/rust-global-variables/


















另外，上⾯这 篇⽂章写的⽐较久了，上图中  的                      lazy_static or once_cell，在 当前最新的         Rust
的版本中 ，可以使⽤           OnceLock 或者      LazyLock  来 替代，这样就不需要依赖第三⽅的                     crate
了。



三、实战篇

使⽤  Rust实现⼀  个    mini-redis：

https://github.com/yaozongyou/rust-24-hour-crash-
course/tree/bdf5bc30a67fe6b5649a8fff7cc25e2e0d19a0e6/mini-redis

## PDF物理页 24

Rust学习建议

1、  The Book通读⼀ 遍

2、  https://rustlings.rust-lang.org/

rustlings上⾯的 练习全部⾛⼀ 遍。

3、 不要尝试写链表、 不要尝试写链表、 不要尝试写链表。



参考资料

 1. Using lightweight formal methods to validate a key-value storage node in Amazon S3

 2. https://rsproxy.cn/

 3. The Rust Programming Language

 4. This Week in Rust

 5. https://doc.rust-lang.org/nomicon/intro.html

 6. https://doc.rust-lang.org/stable/reference/introduction.html

 7. Rust Atomics and Locks

 8. https://rustlings.rust-lang.org/

 9. https://doc.rust-lang.org/rust-by-example/index.html

10. https://github.com/yaozongyou/rust-24-hour-crash-course



























           腾讯技术⼯程
           腾讯技术官⽅号。 腾讯技术创新、 前沿领域发 布解读平台。
           690篇原创内 容

## PDF物理页 25

 公众号



阅读 3.3万
