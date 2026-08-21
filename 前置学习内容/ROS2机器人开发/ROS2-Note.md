# ROS2学习笔记及代码

ROS2机器人开发课程内容：

1. 基础-学会使用ROS2
2. 建模仿真-从零创建一个移动机器人模型
3. 导航-让机器人自己动起来
4. 实体机器人-从零搭建一个实体机器人
5. ROS2进阶-深入掌握ROS2
 - 课程来自Bilibili:鱼香ROS机器人
   https://www.bilibili.com/video/BV1GW42197Ck/?share_source=copy_web&vd_source=90d9499756896bb51e1ab3bdfe1ac934

作者开源库&GithHub代理：https://github.fishros.org

## 第一章
### 1.1 ROS的介绍
ROS-Robot Operating System
ROS包含大量搭建机器人所需的软件和工具，是目前应用最为广泛的机器人操作系统，本质上其实就是用于快速搭建机器人的软件库（核心是通信）和工具集，追求目标：稳定、安全和实时通信能力，ROS凭借生态成为最广泛使用的工具（真像老黄的CUDA）
 - ROS 是什么？
 - ROS主要目的用于传递数据，模拟神经网络的突触，例：

```
             <---温度信号----  皮肤
   大脑           ROS       （传感器）
（决策系统）    (神经网络)      肌肉
             ----运动指令--->（执行器）
```

 - DDS：Data Distribution Service  数据分发服务
 - RMW: ROS Middle Ware

```
                          ROS 2架构概述
应用层                  用户代码（ROS 2节点）
<------------------------------------------------------------>
                 rclcpp         rclpy          其他
                (C++ API)  （Python API）    (语言API)
ROS 2客户端层
                ROS 2客户端库 (rcl:C语言实现)
<------------------------------------------------------------>
DDS 接口层       ROS中间件接口(RMW)
<------------------------------------------------------------>
                  eProsima        Eclipse           RTI
DDS实现层         Fast DDS  或  Cyclone DDS  或  Connext DDS
<------------------------------------------------------------>
操作系统层         Linux  或  Windows  或  macOS
<------------------------------------------------------------>
```

ROS 2已发布版本查询地址

 - http://docs.ros.org/en/humble/Releases.html
主要版本：
 - Foxy Fitzroy  发布日期:2020.6.5      停止维护日期:2023.6.20 （2021作者课程配套软件）
 - Humble Hawksbill  发布日期:2022.5.23    停止维护日期:2027.5 （本课程配套软件）

ROS 2最核心的地方是通信，ROS 2机器人开发特色为：

1. 提供四大核心通信机制
   - 话题(Topic)：基于发布-订阅模式的通信方式，允许节点之间异步交换数据
   - 服务(Service)：同步通信方式，客户端发送请求，服务端处理并返回结果
   - 参数(Parameter):用于机器人参数的设置和读取
   - 动作(Action):支持复杂行为的通信方式，服务端可以反馈处理进度，客户端可以取消请求
2. 拥有各种可视化调试工具
3. 拥有丰富的建模与运动学工具
4. 拥有强大的开源社区和应用框架，例：
   - Gazabo，一个强大的开源仿真工具，可用于模仿机器人行为和环境
   - Navigation 2框架，为移动机器人提供导航功能
   - Moveit 2框架，用于机械臂的运动规划

ROS 2开发中的槽点：
1. 机器人操作系统并不是真的操作系统，受操作系统限制！系统BUG也是你的BUG
2. 本身做不到实时性，硬实时还需依赖操作系统
3. 通信速度受内存速度、网速等物理层限制
4. 大而全，注定和小而美此生无缘

### 1.2.1-1.2.3 ROS2安装虚拟机和Ubuntu
- 操作系统选择  
   尽管ROS 2可以安装在多种操作系统上，但推荐使用Linux操作系统，因为Linux提供了更好的兼容性和性能优化  
   初学者在Windows上安装虚拟机，并在虚拟机中运行Linux系统  
   对于实际的机器人建模仿真和实体机器人开发，建议使用搭载Linux的实体机  

 - 虚拟机安装
用户在Windows系统上创建一个独立的Linux环境，对学习和测试很有用
 - 快速创建包含ROS2的双系统
使用FISHROS2OS等工具可以简化在移动磁盘上安装Linux与Windows并存的双系统过程。
https://www.fishros.org.cn/forum/topic/1835

 - 准备软件：  
虚拟机：VirtualBox  
下载网址：https://www.virtualbox.org/wiki/Downloads  
选择Windows hosts进行下载Windows版本，下载完成后双击运行  
Linux系统镜像：Ubuntu 22.04 version  

因为个人电脑原因，这里VB使用出现问题，已将虚拟机更换为VMware Workstation Pro

 - 创建新虚拟机
打开VirtualBox之后，点击新建进入到新建虚拟电脑的界面，名称自拟或者起Ubuntu，文件夹选择建议在其他盘符下新建文件夹作为Ubuntu系统盘，虚拟光盘则选择刚才下载的镜像iso.文件，跳过自动安装，内存设置4096-8192MB，处理器设置为4核心，虚拟硬盘分配磁盘空间时建议将磁盘空间设置为50-100GB，除非点击预先分配全部空间，否则只会用多少占用多少主机的磁盘空间，这样就创建完成了

 - 安装Ubuntu  
⭕注意事项：如果出现分辨率原因导致Ubuntu页面内容显示不完全的话，按Ctrl + Alt + t 打开终端，然后输入 gnome-control-center display 打开分辨率设置页面，自己选择分辨率调整至Ubuntu页面全部显示为止(本人设置为1280*800，16:10)  
左侧语言栏选择简体中文，点击右边安装，选择键盘配置为Chinese-Chinese，下一步选择最小安装，取消勾选“安装Ubuntu时下载更新”。对于“为图形或无限硬件......”，在安装双系统的时候可以勾选，下一步选择“清除整个磁盘并安装Ubuntu”，下一步地区选择东八区(默认应该是Shanghai)，输入名字和密码，按自己喜好输入，勾选“登录时需要密码”，安装完毕后进行Ubuntu重启并自动初始化，进入桌面如有一系列设置都选择跳过/否，不发送系统信息，最后安装成功。

### 1.2.4 在Ubuntu中安装ROS2
1. 打开并运行Ubuntu，进入桌面后右键鼠标点击“在终端中打开”，输入 sudo apt update ,升级完成之后运行安装工具，输入wget http://fishros.com/install -O fishros 和. fishros,接着选择 1 回车，然后会有一个提示让你更换啊源，目前新的Ubuntu系统已经是国内源了，这里换源和不换源都可以，如果不放心可以去更换一下，放心可以选择 2 回车。如果在运行中显示“检测到您的系统支持多个ROS镜像源......”，可以选择中科大的镜像源并继续，在“选择你要安装的ROS版本名称”选择 humble ，之后在“选择安装的具体版本”选择桌面版，等待安装完成。  
安装成功后输入 ros2 会有一系列提示  
如果要寻找ROS2具体的安装路径，可以输入whereis ros2
2. 在Ubuntu中安装包后缀是 .deb ，右键复制清华开源软件链接后在左上角浏览器中打开，选择pool/main/就可以找到软件的.deb安装包了

### 1.3 运行你的第一个机器人
 - 在学习编程语言的时候第一个项目是"Hello World !"，在学习ROS2的时候第一个项目则是启动海龟模拟器
 - 启动海龟模拟器的方法很简单，直接去在终端运行命令就可以
1. 打开Ubuntu
2. 打开终端
3. 输入ros2 run turtlesim turtlesim_node并回车，成功启动
4. 成功启动后就可以拿键盘控制小海龟了
 - ⭕注意事项：要想控制界面上的海龟移动需要在键盘的窗口进行操作而不是界面
 - 控制海龟例子的简单分析：为什么在键盘控制窗口通过按键就可以实现对海龟模拟器窗口的控制呢？  
 该问题可以通过ROS2提供的一个工具叫做 rqt 里面的一个插件 Node Graph 节点图进行分析  
 使用键盘控制小海龟使用另一个终端，打开新终端后输入run turtlesim turtle_teleop_key并回车，这时的turtle_teleop_key终端充当遥控器功能，小海龟界面为玩具车功能，ROS2起到通信连接作用，在点击turtle_teleop_key终端后就可以在键盘上按方向键对海龟进行控制
5. 案例分析  
新开一个终端，输入rqt回车，点击plugins，选择introspection，选择Node Graph，如果界面较小使用鼠标中键进行放大，箭头为信号的传输方向，其中有cmd_vel代表ROS通信机制的话题。

### 1.4.1 Linux终端基础操作
1. 目录部分  
```bash
$ pwd # 查看终端当前目录默认主目录  
/home/Spindrift  
$ ls # 查看当前目录下的文件  
bin dev home lib lib64 ...  
$ cd / #从当前进入到根目录  
$ cd ~ #从当前进入到主目录  
$ ls   #查看主目录下所有文件  
公共的 模板 视频 图片 文档 下载 音乐 桌面 snap  
````
2. 文件部分
```bash
$ cd ~    #进入主目录  
$ mkdir chapt1             #在主目录下创建chapt1文件夹  
$ cd chapt1                #从主目录进入chapt1  
$ touch hello_world.txt    #创建空白文件  
$ nano hello_world.txt     #在命令行中编辑文件  
$ pwd    #查看当前路径  
/home/fishros/chapt1  
$ ls    #查看chapt1目录下所有文件  
hello_world.txt  
$ cat hello_world.txt    #查看文件内容
hello ros 2!  
$ rm hello_world.txt     #删除文件
```
3. 命令的帮助
```bash
$ rm --help  
用法：rm[选项]...  [文件]...  
删除 (unlink) 一个或多个 <文件>  
```

### 1.4.2 在Linux中安装软件
 - 在VMware虚拟机前提下提前安装 open-vm-tools 可以在Ubuntu中像Kali一样把主机和虚拟机中的内容互相复制粘贴和随着虚拟机窗口大小自动改变分辨率功能，指令如下：  
 ```bash
$ sudo apt update
$ sudo apt install -y open-vm-tools-desktop
```
 - 在VirtualBox虚拟机下可以安装所提供的虚拟机增强插件来实现：  
 点击设备  
 安装增强功能  
 在桌面的左边会有一个CD图标，打开，右键当前页面以终端打开，输入 pwd 查看当前路径，输入 ./autorun.sh 进行执行当前文件夹目录下脚本
在安装完成后进行重启就可以(可以使用指令或者手动关机重启，指令：sudo reboot)  
1. 在Linux中下载VSCODE  
打开虚拟机中的Ubuntu，再打开火狐浏览器输入VSCODE下载网址，在Ubuntu中下载.deb格式的安装包，VSCODE下载网址：https://code.visualstudio.com  
可能会用到的指令：  
```bash
$ cd ~/下载   #使用 Win + 空格 可以切换中英文输入法  
$ sudo dpkg -i ./code_1.77.0-1680085573_amd64.deb  
[sudo] Spindrift 的密码：  
```
虽然使用 dpkg 可以直接安装下载好的.deb格式的安装包，但是使用另外一个更高级的包管理工具 apt 则可以直接通过软件包的名字进行下载和安装  
```bash
$ sudo apt install git
```
除了dpkg和apg之外，还可以通过运行脚本安装，用已安装VisualBox的增强功能为例，来学习如何使用安装脚本  
```bash
$ ./autorun.sh
```
2. 安装  
Ctrl+Alt+T 打开终端，查看所下载的安装包所在目录并进入到安装包所在的目录中，查看当前文件夹下所存在的文件，然后使用 sudo depkg -i ./code(按tab补全)，最后按回车运行  
⭕如有显示以下问题：  
```bash
spindrift@spindrift-virtual-machine:~/ 下载$ sudo dpkg -i./code_1.134.0-1787078834_and64.deb  
dpkg:错误:dpkg前端锁 已被另一个pid为4823的进程加锁注意:删除锁文件的操作是错误的，这样操作会损坏上锁的部分甚至损坏  
个系统。详情请见<https://wiki.debian.org/Teams/Dpkg/FAQ>。  
spindrift@spindrift-virtual-machine:~/下载s  
```
则说明是dpkg的安装锁冲突，系统里以及有另一个程序正在用dpkg/apt，最常见为Ubuntu的后台更新，在终端执行
```bash
$ ps -ef | grep 4823(该四位号码为上述问题pid所显示的号码，如有该问题按实际显示的进程码为准)
```
大概率会看到这几个情况之一:  
unattended-upgrades → 系统自动更新（最常见，刚装的 Ubuntu 会自己跑更新）  
apt-get / apt → 你之前开过更新没等它结束  
dpkg → 之前装包没装完  
处理办法（按顺序）  
第 1 步：等几分钟（推荐，90% 情况管用）  
自动更新一般 5-10 分钟就结束，等锁释放后重试：  
```bash
sudo dpkg -i ./code_1.134.0-1787078834_amd64.deb  
```
第 2 步：如果确认没有其他安装在进行，可以安全解锁  
先看锁是否还被占用：  
```bash
sudo fuser /var/lib/dpkg/lock-frontend
```
如果有输出（返回 pid）→ 说明真有进程在用，别动，继续等  
如果没输出 → 锁是残留的，可以清掉： 
```bash 
sudo rm /var/lib/dpkg/lock-frontend /var/lib/dpkg/lock /var/cache/apt/archives/lock  
sudo dpkg --configure -a
```
⚠️ 注意：报错里那句"删除锁文件是错误的"指的是在有进程运行时硬删会损坏系统。按上面顺序先确认无进程再删，是安全的。  
第 3 步：装完后顺便修掉 apt 卡住的半成品状态  
```bash
sudo dpkg --configure -a
sudo apt-get install -f
```
在运行完安装命令后如果有提示显示：  
```bash
Configuring code

This package will configure the Microsoft repository (apt source)
to receive updates for Visual Studio Code.

Do you want to continue?

                    <Yes>  <No>
```
是VSCODE的软件源确认弹窗，选<Yes>就可以  
等待安装完成后在终端里面输入code来进行调用VSCODE

3. git安装
 - git是Linux中一个用于管理代码版本的工具，安装指令如下：  
```bash
$ sudo apt install git
```
后续选择Y即可  

## 1.4.3 在Linux中编写Python程序
 - 在学机器人开发的时候最常用的为Python语言和C++语言。  
为了使用方便，现在VSCODE安装简体中文汉化插件。  
点击左侧从上往下数第五个图标(Extensions)，然后搜索Chinese，安装第一个简体中文插件包即可，然后点击提示的Change Language and Restart  
1. 进入指定文件夹  
打开VSCODE之后，可以点击左侧的“打开文件夹”，选择之前创建的Chapt1即可，也可以通过终端打开，终端的操作指令如下：  
```bash
$ cd Chapt1/
$ code ./
```
2. 新建hello_world.py文件  
在VSCODE中点击左侧从上往下数第一个图标，切换到资源管理器界面，右键，选择新建文件，输入文件名字 hello_world.py  
3. 输入程序  
输入程序内容，并保存(Ctrl + s)
```py
print('Hello World!')
```
4. 运行程序   
继续右键资源管理器界面，选择在集成终端中打开，使用指令来运行该文件：  
```bash
$ ls   #展示当前目录下所存在的文件  
hello_world.py  
$ cat hello_world.py   #查看当前文件内容  
print('Hello World!')  
$ python3 hello_world.py   #使用python3执行当前文件
```

## 1.4.4 在Linux中编写C++程序
1. 新建hello_world.cpp文件  
在资源管理器界面右键，选择新建文件，输入文件名字 hello_world.cpp  
2. 输入程序  
输入程序内容，并保存(Ctrl + s)
```cpp
#include <iostream>
using namespace std;
int main()
{
   cout << "Hello World" << endl;
}
```
3. 编译并执行代码  
可以使用VSCODE中的集成终端，也可以新建终端  
先将终端目录切换到文件所在的目录下  
```bash
$ g++ hello_world.cpp   #使用g++编译所指定的.cpp文件  
$ ls   #展示当前文件夹下内容  
a.out  
$ ./a.out   #运行当前编译完的文件  
Hello World!
```
 - 对于简单的代码g++可以很轻松编译，但是对于使用多个头文件库的复杂代码g++使用起来就会很麻烦，在程序开发中，可以使用工具 CMake list 来编译c++文件。  
4. 使用CMake list (简称CMake)  
在资源管理器界面右键，选择新建文件，输入文件名字 CMakeLists.txt  
输入内容并保存  
```bash
cmake_minimum_required(VERSION 3.8)  
project(HelloWorld)  
add_executable(learn_cmake hello_world.cpp)
```
然后使用 CMake 指令把它转换成一个 MakeFile 的文件， MakeFile 再调用一个 Make 指令生成可执行文件executable.exe
 - 编译并运行
 打开CODE的集成终端，输入指令:  
 ```bash
spindrift@spindrift-virtual-machine:~/Chapt1$ cmake .
CMake Warning (dev) in CMakeLists.txt:
  No project() command is present.  The top-level CMakeLists.txt file must
  contain a literal, direct call to the project() command.  Add a line of
  code such as
spindrift@spindrift-virtual-machine:~/Chapt1$ make
-- Configuring done
-- Generating done
-- Build files have been written to: /home/spindrift/Chapt1
[ 50%] Building CXX object CMakeFiles/learn_cmake.dir/hello_world.cpp.o
[100%] Linking CXX executable learn_cmake
[100%] Built target learn_cmake
spindrift@spindrift-virtual-machine:~/Chapt1$ ls
a.out           cmake_install.cmake  hello_world.py   Makefile
CMakeCache.txt  CMakeLists.txt       hello_world.txt
CMakeFiles      hello_world.cpp      learn_cmake
spindrift@spindrift-virtual-machine:~/Chapt1$ ./learn_cmake 
Hello World!
spindrift@spindrift-virtual-machine:~/Chapt1$ ^C
spindrift@spindrift-virtual-machine:~/Chapt1$ 
```