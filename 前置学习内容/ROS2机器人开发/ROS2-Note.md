# ROS2学习笔记及代码

ROS2机器人开发课程内容：

1. 基础-学会使用ROS2
2. 建模仿真-从零创建一个移动机器人模型
3. 导航-让机器人自己动起来
4. 实体机器人-从零搭建一个实体机器人
5. ROS2进阶-深入掌握ROS2
 - 课程来自Bilibili:鱼香ROS机器人
   https://www.bilibili.com/video/BV1GW42197Ck/?share_source=copy_web&vd_source=90d9499756896bb51e1ab3bdfe1ac934

作者开源库&GithHub代理：https://github.fishros.org（打不开？）


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
----  
bin dev home lib lib64 ...  
$ cd / # 从当前进入到根目录  
$ pwd  
----  
/  
$ cd ~ # 查看主目录  
$ ls  
----  
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
----  
/home/fishros/chapt1  
$ ls    #查看chapt1目录下所有文件  
----  
hello_world.txt  
$ cat hello_world.txt    #查看文件内容
----  
hello ros 2!  
$ rm hello_world.txt     #删除文件
```
3. 命令的帮助
```bash
$ rm --help  
----  
用法：rm[选项]...  [文件]...  
删除 (unlink) 一个或多个 <文件>  
```

### 1.4.2 在Linux中安装软件



