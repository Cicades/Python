## 1.linux文件与目录管理

- 文件默认权限与隐藏权限
  + `umask`——指定文件创建时默认的权限
  + `touch`——可以修改与文件相关的时间（atime, mtime, ctime）
  + 文件的特殊权限
    1. SUID
    2. SGID
    3. SBIT
  + `file <filename>`——查看文件的基本数据类型
- 文件的查找
  + `whereis`——在特定的一些列目录中查找文件或指令
  + `locate <keyword>` ——通过系统数据库查找名字包含keyword的文件
  + `updatedb`——更新系统数据库
  + `find`——可根据时间范文，文件名，权限等信息来查找文件

## 2.磁盘与文件系统管理

- 文件系统的基本构成
  + `superblock`——记录此文件系统的整体信息，包括`inode\block`的使用情况，文件系统的格式以及相关信息
  + `inode`——记录文件属性，一个文件占用一个`inode`同时记录此文件所在`block`号码
  + `block`——实际记录文件的内容，常见大小为`1k\2k\4k`，若文件太大时，会占用多个`block`
  + `Linux VFS(Virtual Filesystem Switch)`——os通过VFS的核心功能去读取filesysytem

- 文件系统的简单操作

  + 磁盘与目录的容量
    1. `df`——列出文件系统的磁盘使用量，主要读取`superblock`中的信息
    2. `du`——评估文件系统的磁盘使用量，直接到文件系统内去搜寻所有文件的数据

- 实体链接与符号链接

  + `ln [source][target]`——创建`hard link`

    ![硬链接文件读取流程](.\images\2-1hardlink.PNG)

  + `ln -s [source] [target]`——创建`symbolic link`

    ![符号链接文件读取流程](.\images\2-2symbolic-link.PNG)

## 3.文件系统的压缩、打包、与备份

- `gzip(GNU zip)`

  + 使用gzip进行压缩时，在默认状态下原本的文件会被压缩成.gz的文件名，原始的文件不再存在
  + `zcat/zmore/zless/zgrep`——查看和检索`gzip`的压缩文件

- `bzip2`

  > bzip2是为了取代gzip并提供更佳的压缩比而来的，其用法与gzip几乎相同

  + `bzcat/bzmore/bzless/bzgrep`

- `xz`

  > xz的压缩比更高，其用法与gzip/bzip2几乎一模一样

  + `xzcat/xzmore/xzless/xzgrep`

- `tar`

  > 上述压缩指令大多只能针对单一文件进行压缩，而tar则可以将多个文件或者目录打包成一个大文件同时还可通过gzip/bzip2/xz的支持将该文件同时进行压缩

  + 基本选项

  ![tar常用指令](.\images\3-1-tar.PNG)

  + 基本名称——仅打包而不经压缩的文件称为`tarfile`,而经过压缩的文件称为`tarball`

## 4.文件编辑

- dos与linux断行
  + `dos2unix`——将dos断行转换为linux断行
  + `unix2linux`——将unix断行转换为dos断行
- 语系编码转换
  + `iconv`

## 5.BASH

- 指令下达

  + `type`——查看`bash`命令的类型

  + `\[Enter]`——指令断行
  + `[ctrl]+u/[ctrl]+k`——从光标处向前或向后删除指令

- Shell变量

  + `echo ${varname}`——取对应的变量
  + 变量的基本操作

  ~~~shell
  version=$(uname -r) # 将uname -r指令输出内容赋值给version
  test=hello
  test=${test}' world' # test由hello变为hello world
  unset test # 删除test变量
  ~~~

  + `env`——查看环境变量

  + `set`——查看所有变量

  + 重要的变量（以下变量不一定是环境变量）

    * `PS1`——提示字符的设置
    * `$`——当前shell的pid
    * `?`——上个执行指令的回传值
    * `OSTYPE`——os类型如：linux-gnu
    * `HOSTTYPE`——主机架构类型如：x86_64
    * `MACHTYPE`——机器类型，涵盖上述两者

  + `export`——将自定义变量转换为环境变量

    > bash是一个独立的程序，在bash下面下达的任何指令都是bash衍生出来的，被称为子程序，子程序只会继承父程序的环境变量，即无法访问父程序的自定义变量 

  + `read [-pt] var`——类似于input函数，从键盘接受变量值

  + `declare [-aixr] var`——声明变量的类型

  +  `ulimit`——设置文件系统即程序的限制关系，如限制新建文件的大小

  + 变量内容修改操作

    * `${PATH#/*local/bin:}`——从左往右，删除`PAHT`中所匹配`/*local/bin:`的内容,

    * `${PATH##/*local/bin:}`上者的贪婪模式

    * `${PATH%:*bin}`——从右往左删除`PATH`中所匹配`:*bin`的内容

    * 同理`%%`开启贪婪模式

    * `${path/sbin/SBIN}`——将`path`中所有的`sbin`替换成`SBIN` 

    * 变量测试与内容替换

      ![](F:\study\books\linux\images\5-1-bash-var.PNG)

- 命令别名和历史命令
  + `alias cls='clear'` ——将`cls`设为`clear`的别名
  + `unalias cls`——取消设置`cls`的别名
  + `history [-craw] [n]`——操作历史命令

- `Bash shell 操作环境`

  + 路径与指令的搜寻顺序

    ![](.\images\5-0-mehtod-order.PNG)

  + `login shell`

    ![login shell 配置读取流程](F:\study\books\linux\images\5-2-login-shell.PNG)

  + `non-login shell`

    * 仅读取`.bashrc`的配置内容

  + `<.|source> <config_file>`——读取配置文件的内容，并生效

- 终端机环境设置

  + `stty`和`set`

  + `bash`默认组合键

    ![](./images/5-3-bash-shortcut.png)

  + `bash`特殊符号

    ![](./images\5-4-bash-special-letter.PNG)

- 数据流重导向

  ~~~shell
  $ > # 将正确信息输出到指定文件或者设备
  $ >> # 追加
  $ 2> # 将错误信息重定向
  $ 2>> # 将错误信息以追加的方式重定向
  $ cat > test.txt # 将标准输入的内容写入test.txt
  $ cat > test1.txt < test.txt # 将test.txt的内容作为标准输入，以此创建test1.txt 
  $ cmd1 && cmd2 # if $?=0 cmd2 or cmd1
  $ cmd1 || cmd2
  $ cmd1 && cmd2 || cmd3 # cmd1正确则执行cmd2否则执行cmd3
  ~~~

   + `/dev/null`——垃圾桶黑洞设备，任何导向这个设备的信息都会被忽略

   + `cut -d '分割字符' -f fields(n)`

   + `cut -c 字符区间`

   + `sort`——根据字段进行排序

   + `wc`——统计字数

   + `uniq`——去重

   + `tee`——双重导向

     ~~~shell
     $ ls -l | tee -a <filename> | more # 将ls输出保存至文件并打印到屏幕
     ~~~

  + 字符串转换

    ~~~shell
    $ tr -d <str> # 删除str字符串
    $ tr -s <str> <str1> # 以str1替换str
    $ col -x # 将tab按键处理为空白格
    $ join # 处理两个文件当中有“相同数据”的那一行，并将其相加
    $ paste # 将数据直接粘合在一起
    $ expand [-t] file # 将tab转换为空白符
    ~~~

  + 其他命令

    * `split [-bl] file <prefix>`——分区命令，可以将文件切割成几个文件

    * `xargs`——xargs可以读入stdin数据，并且以空白符或者断行符作为分辨

    * `-`——用来代替stdout和stdin

      ~~~ shell
      $ tar -cvf - /home | tar -xvf - -C /tmp/homeback # 将/home里面的文件打包，但并不产生文件而是将数据传送到stdout；经过管道将stdout传给tar -xvf -
      ~~~
***
  ##  6.文件格式化处理

- `nl [options] <filename>`——读取文件的内容作为标准输出

- `sed`工具

  + 基本用法

    ![](./images/6-sed-usage.png)

- `prinf`——格式化输出，用法和C语言中printf函数相似

- `awk`——数据处理工具，倾向于将一行分成数个字段和来处理

- `diff<from-file> <to-file>`——比价文件之间差异

- `cmp <file1> <file2>`——以字节为单位比较文件之间的差异

- `patch`——为文件打补丁

- `pr [options] <filename>`——在屏幕上打印文件的内容

***

## 7.shell脚本

- 数值运算

  + 基本用法——`$((运算内容))`
  + 保留小数——`bc`

- script脚本执行方式差异

  - `sh script`或`./script`——脚本会在子程序中执行，执行结果不会影响父程序
  - 利用`source`执行脚本：在父程序中执行

- 判断式

  - `test`指令:`test [options] <item>`提供了许多测试功能，包括文件类型判断，文件权限检测，判等...
  - `[ <expression> ]`——判断表达式，和`test`的用法相似

- 脚本执行传递参数

  ~~~shell
  $ ./gensh.sh filename1 filename2 ...
  #	$0			$1		$2
  ~~~

  + `script`内可使用的特殊参数
    * `$#`——执行脚本所带参数的个数
    * `$@`——列出所有参数
    * `shift <n>`——参数偏移

- 条件判断式

  - `if`

    ~~~shell
    if [ 条件判断式1 ]；then
    	expression1
    elfi [ 条件判断式2 ]；then
    	expression2
    else
    	expression
    fi
    ~~~

  - `case`

    ![](./images/7-script-case.png)

- 函数

  + 定义

    ~~~shell
    function fname （）{
        函数体...
    }
    ~~~

  + 调用——`**fname**`

- 循环

  + 条件循环

    ~~~shell
    while [ condition ]
    do
    	程序段落
    done
    ##################################
    until [ condition ]
    do
    	程序段
    done
    ~~~

  + 固定循环

    ~~~shell
    for var in con1 con2 con3
    do
    	程序段
    done
    ~~~
