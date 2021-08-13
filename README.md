# SCons使用

[官网](https://scons.org/)

[简单入门](https://www.jianshu.com/p/e4bd3ab9e5d6)

[SCons使用](https://www.jianshu.com/p/c28609d9e559)

[TOC]

---

## 0. 安装
`ubuntu`环境中直接使用命令：`sudo apt-get install scons`

## 1. `hello world`

`hello.c`
```c
#include <stdio.h>

int main(int argc, char* argv[])
{
    printf("Hello World!\n");
    for(int i = 0; i < argc ; i++) {
        printf("argv[%d] = %s\n", i, argv[i]);
    }

    return 0;
}
```

`SConstruct`
```python
Program("hello.c")
```
除了使用`SConstruct`作为配置文件，还可以使用`Sconstruct`、`sconstruct`、`SConscript`。

`Program`是`Scons`中的一个编译方法（build_method），用来告诉`Scons`想要把`hello.c`编译成一个可执行文件。

也可以使用`Program(target_name, "hello.c")`来指定可执行文件的名字。

执行命令：`scons`
```log
scons: Reading SConscript files ...
scons: done reading SConscript files.
scons: Building targets ...
gcc -o hello.o -c hello.c
gcc -o hello hello.o
scons: done building targets.
```

会生成`.o`和可执行文件
```log
.
├── hello
├── hello.c
├── hello.o
└── SConstruct
```

其他操作：
> `scons -c`：clean
>
> `scons -Q`：只显示编译信息，去除多余的打印
>
> `scons -Q`
>
>    --implicit-cache hello 保存依赖关系
>
>    --implicit-deps-changed   强制更新依赖关系
>
>    --implicit-deps-unchanged  强制使用原先的依赖关系，即使已经改变

提供的函数：
> `Program()`：执行编译操作，生成可执行文件
> 
> `Library()`：执行编译操作，生成静态库
> 
> `StaticLibrary()`：执行编译操作，生成静态库
> 
> `SharedLibrary()`：执行编译操作，生成动态库
> 
> `Environment()`：编译环境

提供的编译参数：
> `target`，生成的执行文件名字
> 
> `source`，编译文件
> 
> `LIBS`，依赖库
> 
> `LIBPATH`，依赖库路径，有环境变量的可不添加，针对用户库或第三方库
> 
> `CPPPATH`，头文件路径
> 
> `CCFLAGS`，编译参数

其他函数：
> `Split()`：将字符串分隔为列表
> 
> `Glob('*.cpp')`：加入所有文件

# 1.1 编译多个文件
目录如下：
```log
.
├── code
│   ├── goodbye.c
│   ├── goodbye.h
│   ├── hello.c
│   └── hello.h
├── main.c
└── SConstruct
```

`main.c`
```c
#include <stdio.h>
#include "hello.h"
#include "goodbye.h"

int main(int argc, char* argv[])
{
    printf("-----main-----\n");
    for(int i = 0; i < argc ; i++) {
        printf("argv[%d] = %s\n", i, argv[i]);
    }

    hello_world(3);
    goodbye_name("Jack");

    return 0;
}
```

`hello.c`
```c
#include <stdio.h>

int hello_world(int num)
{
    int i = 0;
    for(i = 0; i < num; i++) {
        printf("Hello World!\n");
    }

    return 0;
}
```

`hello.h`
```c
#ifndef __HELLO_H__
#define __HELLO_H__

int hello_world(int num);

#endif
```

`goodbye.c`
```c
#include <stdio.h>

int goodbye_name(const char* name)
{
    printf("goodbye %s\n", name);

    return 0;
}
```

`goodbye.h`
```c
#ifndef __GOODBYE_H__
#define __GOODBYE_H__

int goodbye_name(const char* name);

#endif
```

`SConstruct`
```python
src = Glob("code/*.c")
src.append("main.c")

inc = ["code"]

Program(
    target = "main",
    source = src,
    CPPPATH = inc)
```

# 1.2 编译库
`SConstruct`
```python
lib_src = Glob("code/*.c")
Library(
    target = "code",
    source = lib_src
)
```

但是这样编译出来的`libcode.a`会出现在根目录下，需要想个办法重新定义输出路径。

`scons`是**没有指定输出路径的功能的**。

解决办法是，在子目录中添加`SConscript`文件，并在上层的`SConstruct`中指定`variant_dir`。

增加`code/SConscript`文件：
```log
.
├── code
│   ├── goodbye.c
│   ├── goodbye.h
│   ├── hello.c
│   ├── hello.h
│   └── SConscript
├── main.c
└── SConstruct
```

`SConstruct`:
```python
V = {"hello": "world"}

SConscript("code/SConscript", variant_dir="lib/code", duplicate=0, exports=V)
```

`SConscript`:
```python
Import('hello')
print(f'debug {hello}')

lib_src = Glob("./*.c")
Library(
    target = "code",
    source = lib_src
)

```

执行`scons`后的结果：
```log
.
├── code
│   ├── goodbye.c
│   ├── goodbye.h
│   ├── hello.c
│   ├── hello.h
│   └── SConscript
├── lib
│   └── code
│       ├── goodbye.o
│       ├── hello.o
│       └── libcode.a
├── main.c
└── SConstruct
```

这样就可以指定生成路径了。

`SConscript()`的基本用法：
> `SConscript(scripts, [exports, variant_dir, duplicate, must_exist])`
>
> 可以使用`export`来向子文件传递变量信息
>
> 指定多路径
>
> `SConscript(dirs=['sub1', 'sub2'], name='MySConscript')`

## 1.3 链接一个库
修改`SConstruct`如下：
```python
SConscript("code/SConscript", variant_dir="lib/code", duplicate=0)

src = Glob("*.c")

inc = ["code"]

Program(
    target = "main",
    source = src,
    CPPPATH = inc,
    LIBS = ["code"],
    LIBPATH = ["lib/code"]
)
```

## 1.4 判断是否需要重新编译

