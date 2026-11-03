# IceCup — 机器人冰壶比赛项目

## 用户长期偏好

### 终端 / Shell
- **在 Windows 上一律默认使用 PowerShell 7（`pwsh`）**执行命令。
- **不要使用 Windows PowerShell 5.1**（`C:\WINDOWS\System32\WindowsPowerShell\v1.0\powershell.exe`），
  除非用户明确指定，或某操作确实只能在 5.1 下完成。
- 若 `pwsh` 不可用，先报告并询问，不要静默回退到 5.1。

### 环境事实（2026-10-13 更新）
- 已授权软件：**SolidWorks 2024**、**AutoCAD 2024**。
- **PowerShell 7.6.6（MSI / Core 版）已安装**：`C:\Program Files\PowerShell\7\pwsh.exe`，
  该路径已写入机器级 PATH，会被执行器的"常见安装位置"探测优先命中。
- Microsoft Store 版 PowerShell 已卸载；`WindowsApps\pwsh.exe` 的 0 字节应用执行别名已移除。
- 工作目录 `D:\IceCup` 用于本比赛的 CAD / 仿真 / 加工产物。

### CAD 软件实测位置（注册表查证，2026-10-13）
- SolidWorks **2024 SP05** → `D:\SoildWorks\SOLIDWORKS\`（注意目录名 `SoildWorks` 是拼错的既成事实，别改）。
  含 Flow Simulation / Electrical / Inspection / Visualize / Composer，属 Premium 级别。
- AutoCAD **2024**（R24.3）→ `D:\CAD\AutoCAD 2024\`。
- **Smart App Control = 关**（`HKLM\SYSTEM\CurrentControlSet\Control\CI\Policy`
  的 `VerifiedAndReputablePolicyState = 0x0`）。
  这条很重要：text-to-cad 依赖的 OCP（OpenCascade Python 绑定）wheel 带未签名 native module，
  上游 README 说 SAC 开着就会 `ImportError: DLL load failed while importing OCP`。
  本机 SAC 已关，**该阻塞不存在**，已实测 `cadgen doctor` 报 `kernel OK`。
- Python 3.13.1 在 `D:\Python\`；Scripts 目录 `D:\Python\Scripts` **不在 PATH**。
- uv **0.13.0** 已装到 `D:\Python\Scripts\uv.exe`（`uvx` 同目录）。

## 已知环境问题
- **DSH shell 解析是启动时缓存的。** `dsh-pwsh-local` 的执行文件解析是
  `(configured, env, platform)` 的纯函数，**仅当 `pwshPath` 配置值变化时才重新探测文件系统**。
  因此更换 PowerShell 安装后必须重启 DSH 才会生效；否则会一直用旧的解析结果
  （曾长期落到 Windows PowerShell 5.1）。
- 解析顺序：显式 `pwshPath` → 常见安装位置（`C:\Program Files\PowerShell\7\pwsh.exe`）
  → PATH → Windows PowerShell 5.1（最后手段）。
- **已验证生效**：重启 DSH 后 shell 为 `C:\Program Files\PowerShell\7\pwsh.exe`（Core 7.6.6）。
- **`workspace-write` 文件沙箱下 shell 无法启动**，稳定复现 `0xC0000142`
  （`STATUS_DLL_INIT_FAILED`）。已排除 PowerShell 因素——换 MSI 版后症状不变，
  且该错误在旧的 powershell.exe 上同样出现，说明与解释器无关。
  DSH 文档说明：ACL 沙箱的 keep-alive ACE 组（登录 SID + Everyone）缺失时，
  "早期 DLL 初始化会以 `0xC0000142` 死亡"。属 DSH 沙箱在本机的环境缺陷。
  **变通办法：把会话文件策略设为 `danger-full-access`，shell 即正常工作。**
- **GitHub 域名要分开看**（2026-10-13 实测，修正旧记录）：
  - `api.github.com` ✅ 可用（拉 README / 仓库元数据走 REST 最稳）
  - `codeload.github.com` ✅ 可用 → **下源码用这个**：
    `curl -L -o x.tar.gz https://codeload.github.com/<owner>/<repo>/tar.gz/refs/heads/<branch>`
  - `github.com` 根域名 ❌ curl 返回 `000`（连接失败），所以 `git clone` 不要指望
  - `raw.githubusercontent.com`、`cdn.jsdelivr.net`、`raw.gitmirror.com` ❌ DNS 解析失败
- **`pypi.org` 会中途截断**：JSON API 在 ~746KB 处断流，`pip install` 直接卡死。
  **一律加国内镜像**：`-i https://pypi.tuna.tsinghua.edu.cn/simple/`（实测 4.4 MB/s）。
  uv 侧用环境变量 `UV_DEFAULT_INDEX` 指同一个镜像。

## DSH MCP 接入（2026-10-16 搭建完成并实测通过）

自建配置型 bundle **`@local/icecup-mcp`**，源文件在
`C:\Users\Spindrift\.dsh\bundles\icecup-mcp\`（`package.json` + `cordis.patch.yml`），
经 `plugin_manager` 以 `link:` 方式安装。**改完配置用 `set_bundle` 关→开即可重载，不用重启 DSH。**

| serverName | 传输 | 提供方 | 实测 |
|---|---|---|---|
| `swapi_pilot` | streamable-http → `https://swapi-pilot.com/mcp` | 远程服务 2.14.7 | ✅ 返回真实 SolidWorks API 文档 |
| `autocad` | stdio → `C:\Users\Spindrift\.local\bin\autocad-mcp.exe` | PyPI `autocad-mcp-pro 1.6.0` | ✅ 建图→画线→导 DXF 全链路通过 |

工具命名 `mcp__<serverName>__<tool>`。autocad 侧开了 `DISCOVERY_MODE=search`，
只暴露 `search_tools` + `call_tool`（约 356 tokens）——
**不要关掉它**，完整目录的闲置成本是 **83,921 tokens**。

### 踩过的坑（重要）
- **`AUTOCAD_MCP_BACKEND` 必须写 `ezdxf`，不能用 `auto`。**
  `auto` 因 COM 类已注册而选中 `com`，然后**不回退**；AutoCAD 没开时每次调用都报
  `Cannot connect to CAD application 'AutoCAD.Application'`。
  更要命的是 `system_about` 的 `active_backend` 报的是"配置的"后端，**会误报成 `com`**——
  别信那个字段，要看实际调用成不成。
  **要驱动活的 AutoCAD**：先手动打开 AutoCAD，再把该值改成 `com`。
- 已设 `ALLOWED_PATHS=D:\IceCup`、`DANGEROUS_COMMANDS_ENABLED=false`（未放开危险命令）。
- swapi-pilot 首次调用偶发 `fetch failed`（冷启动），**重试一次即可**。
- swapi-pilot 自带工作流模板主张**一律生成 C# 控制台项目**，不写 Python/VBA。
  写 SolidWorks 代码前必须
  `search_solidworks_api` → `get_api_detail` → `get_enum`，**绝不凭记忆写 API**。
- 上游源码副本：`D:\IceCup\.vendor\mcp\`（Autocad-MCP-main、swapi-pilot-solidworks-mcp-main），备查。

## 项目背景
- 赛事：**哈尔滨工业大学 冰壶机器人对抗赛**（规则来源＝组委会场地/规则介绍两页，2026-10-13 已读）。

### 规则已钉死的几何（不要凭记忆改，以 `src/spec.py` 为准）
| 项 | 值 |
|---|---|
| 场地 | 2940 × 1000 mm |
| 机器人铅锤投影 | **≤ 350 × 350 mm，高度方向无限制** |
| 冰壶 | 直径 47 × 总高 32 mm |
| 击球点 | 中心距地面 **≈12 mm** |
| 取壶架 | 305（宽）× 305（高）× 60（深）mm，**立面板** |
| 单元格 | 80 × 80 × 60 mm，**3×3 共 9 格**（"9X9格"是排版笔误，已由用户确认） |
| 架壁厚度 | 16.25 mm（= (305−3×80)/4，推导值） |
| 格间距 pitch | 96.25 mm（= 80 + 16.25，推导值） |
| 每队壶位 | 5 只：底层 2 / 中层 2 / 上层 1，**具体哪几格由对手摆放** |
| 时限 | 一次"取壶+投壶" **2 分钟**内完成，超时记零分 |
| 判负 | 取壶过程中冰壶**翻转、掉落至界外区**即失败 |
| 得分 | 只有大本营内、且比对方所有壶更接近圆心的壶计分，每壶 1 分，单局 0:0～5:0 |

### 由几何推出的机构约束（`checks/pick_envelope.py` 算出，已用 STEP 实测校核）
- 壶心高度三档：**32.2 / 128.5 / 224.8 mm**；上层壶顶 **240.8 mm**。
  → 取壶机构 Z 向需 **≈208.5 mm 行程**（32.2 → 240.8）。
- 格口 80 − 壶径 47 = 33 mm，**单侧仅 16.5 mm**（实测壶径 46 时 17.0 mm）。
- **格后有 2 mm 亚克力背板**（用户 2026-10-16 确认）→ 内深 58，**"从后顶出"类方案作废**。
- 58 − 47 = **11 mm 前后余量**：壶在格里前后位置不确定，夹爪必须吃掉这 11 mm 或靠导向自位。
  夹爪要越过架前脸 **23.5 … 34.5 mm**。
- 格高 80 − 壶高 32 = **48 mm 净空** → 夹爪本体可坐在壶上方，爪指下伸 32 mm 夹壶身。
- 推壶接触高度**三个来源不一致**：实测 10.90 / 图纸推算 11.05 / 规则页 12.0，
  散布 1.1 mm → **叶片按 10.4–12.5 mm 可调设计**，宽度做窄于实测齿带 9.4 mm。
- **换列不能只靠底盘对中**：外列壶心在 |Y|=346.25，350 宽的车体对中后会**越出场地边缘 21.2 mm**
  （场地半宽 500、无围挡）。要么给夹爪 **±96.25 mm 的 Y 向行程**，要么接受越边风险。
  这条修正了之前"换列靠底盘移动"的说法。

### 整机概念设计（2026-10-16，`src/robot.py` / `src/robot_in_venue.py`）

六个自由度，每个都对应一条规则约束，**没有一个是多余的**：

| 子系统 | 方案 | 对应约束 |
|---|---|---|
| 底盘 | 4× 麦克纳姆 Ø53.6×25.56，300×300 板 | 全向移动，对准列不用原地转；2 分钟时限省动作 |
| 换列 | **桅杆整体 Y 滑台 ±100mm** | 外列壶心 \|Y\|=346.25，车体对中会越边 21.2mm，**不能靠底盘对中** |
| 升降 | 前置单立柱，行程 350mm | 208.5mm 架内行程 + 未量的平台高 H（留到 140） |
| 取壶 | 双爪沿 Y 闭合，爪厚 14、伸入 40、带导向斜面 | 单侧间隙 16.5；沿 Y 闭合对 11mm 前后余量不敏感 |
| 投壶 | **固定推板 + 底盘加速推过固定行程后停车**，壶靠惯性滑出 | 初速重复性=编码器重复性；不需要独立推壶轴 |
| 推板收纳 | 舵机翻折贴平前脸 | 否则取壶时推板撞取壶架面板 |

**校核数字**（`robot_in_venue.py` 打印）：footprint **340×300**（限 350）；车前脸离架面 5mm；
**爪尖 −735.0 对贴后壁壶心 −734.5**；车体 Y 向 100–400，完全在场内。

**对准不上视觉**：前端两路线传感器骑瞄准辅助线（±95），一路停投壶线。规则白送的基准。

**未建模**：麦轮滚子、传感器、线束、桅杆导轨/丝杠细节、舵机具体型号布置。
**若磁铁测试通过**（壶底三球是钢的），夹爪+导向整组删除，换成 Z 轴末端一个电磁铁。

**⚠️ 2026-10-17 更新——以下三条已被后续工作取代，当前状态以 `PROGRESS.md` 为准**：
- **升降**：不再是"前置单立柱 350"。已设计并验证 **Z 轴模块**（齿条固定 + 齿轮爬行 + 3 个限位开关），
  行程 230，6 件打印文件在 `newSTEP/`，源码 `src/z_params.py` + `src/z_*.py`。
- **投壶**：**"底盘推板"已证伪**——舵机 62 rpm × 轮周长 168.4 = 轮面最高 **0.175 m/s**，
  而滑到圆心需要 0.81–2.87 m/s（差 5–16 倍）。方向改为**弹簧发射器**（舵机上弦 + 凸轮释放）。
- **取壶**：仍未定。壶底 3 颗万向滚珠着地且会转 → 铲叉/底部磁吸均不可行；磁吸目标改为**手柄顶盖**，
  新增"抓 Ø11 手柄杆"候选。`src/robot.py` 的双爪仍只是概念模型。

## 场地几何（`dxf/Place.DXF` → `src/venue_spec.py`，2026-10-16）

坐标系原点在**投壶线与中线交点**，+X 朝大本营，+Z 向上，台面 Z=0。

| 项 | 值 | 来源 |
|---|---|---|
| 圆心 | X = **+1680.000** | 图上一条正好 1680 的引出线 |
| 大本营四圈半径 | **35 / 100 / 165 / 230**（环距均匀 65） | 画的 |
| 轨道 | 半宽 **±275**（宽 550），长 2000（X 0→2000） | 画的 + 用户口述"轨道宽55cm" |
| 瞄准辅助线 | 半宽 **±95**（虚线，卡尺量得） | 标注 180=275−95；画在 ±97.5 是误差 |
| 场地半宽 | 端区 **±500**，轨道只有 **±275** | 画的：±500 那两条边只有 800 长，±275 的有 2000 长 |
| 端区 | 投壶线后 800 长（X −800→0），全宽 1000 | 画的 |
| **平面形状** | **不是等宽长方形**，是"550×2000 轨道 + 1000×800 端区"的 T 形，台阶正好在投壶线上。旁证：大本营外径 Ø460 刚好塞进 550 轨道 | 画的 |
| 取壶架 | 前脸 **X=−700**，深 60 到 −760，Y 中心 **±250**，背距场边 40 | 画的 |
| 台面 | **轨道与外围同一高度**，纯平人造板，**无围挡、无斜坡** | 用户确认 |
| 长度矛盾 | 图上 2800，规则 2940，**差 140 = 一段没量的白色地带** | 参数 `EXTRA_LENGTH` |
| 平台高度 | **未量**，架高放在平台上，参数 `PLATFORM_HEIGHT`（默认 0） | 待现场量 |

装配体 `src/venue.py` → `STEP/venue.step`（2940×1000×315，13 个实体）。
**仿真用**，所以按碰撞体建：一块板 + 两个架 + 十只壶；零厚度的地面标线不建。

### 尚未冻结的决定（2026-10-17 更新）
- 取壶方式——**未定**，候选见 `PROGRESS.md` §3.4（磁吸手柄顶盖 / 抓 Ø11 手柄 / 侧夹 / 笼罩）。
  已排除：铲叉（滚珠着地、缝隙极小）、底部磁吸（够不到）、从格后顶出（2mm 背板）。
  已确认：手柄杆 **Ø11**、提着不晃（用户实测）；壶底 **3 颗万向滚珠**会转（用户拍照）。
- 投壶方式——**底盘推壶已证伪**（理由见上）。方向：**弹簧发射器**，调参靠换凸轮。
  在此之前先做"手推 20 次"实验，定 μ 与台面倾斜。
- **仿真器：决定不装**。主控是 Arduino 不是 ROS 2，Gazebo 的"同一套控制代码跑仿真和真机"
  这条价值不存在；且 μ 只能实测，仿真给不出新信息。省下的时间做落点标定实验。
- 待现场量：**平台高度 H**（架高放在平台上；与 Z 模块 STROKE=230 的对应关系待核）、
  **140 mm 白色地带在哪一端**、**场地表面具体材质**（定 μ）
- 待验证：**手柄顶盖能不能被磁铁吸住**（取壶候选见 `PROGRESS.md` §3）

## 工具链决定（2026-10-13 修订）
- **SolidWorks 2024 = 主 CAD**，出加工图、公差、钣金展开、装配。AutoCAD 2024 出 2D 切割图。
- **text-to-cad / cadgen = 概念探索与几何量测的副手**，不是主 CAD。
  它自带独立 OpenCascade 内核，**不驱动 SolidWorks、也不被 SolidWorks 调用**，
  两边同时建模会造成几何分叉——所以每个零件只能认一个权威源。
- **MoveIt / SRDF 已从链路中删除**。真实 DOF ≈ 底盘差速 2 + Z 升降 1 + 夹持 1 + 推壶 1，
  取壶是"车到位→直上直下→闭合"，投壶是"贴瞄准辅助线→直线推"，
  **不需要 IK、不需要位形空间路径规划**，上 MoveIt 是纯负债。
- **胜负手不在整机仿真，在冰壶滑行距离重复性**。落点要控在 ±30 mm 级，
  决定因素是摩擦一致性 + 初速可重复性，属 1 自由度滑移问题；
  优先做"同一初速重复推 20 次量落点分布"的辨识实验，而不是一上来建 Gazebo 世界。
- 相关开源参考（保留备查）：
  - `jsk-ros-pkg/solidworks_urdf_exporter2`（sw2robot，支持 SW2024）
  - `ros/solidworks_urdf_exporter`（老版，预编译包仅到 SW2021）
  - `earthtojake/text-to-cad`（**已装，见下**）

## cadgen 已安装状态与调用方式（2026-10-13 实测跑通）
- 版本 **cadgen 0.7.21**，经 uv 隔离环境安装，**遥测已关**（`cadgen telemetry off`）。
- `cadgen doctor` → `kernel OK`，OCP 正常加载。
- 每次调用需要这三个环境变量：
  ```bash
  export UV_DEFAULT_INDEX="https://pypi.tuna.tsinghua.edu.cn/simple/"
  export PATH="/d/Python/Scripts:$PATH"        # uvx 在这里
  export CADGEN_TELEMETRY=0
  ```
- 模型脚本用 `python`，CLI 用 `cadgen`：
  ```bash
  cd /d/IceCup/src && uvx --no-config --python 3.13 --from "cadgen==0.7.21" python <model>.py
  uvx --no-config --python 3.13 --from "cadgen==0.7.21" cadgen step snapshot ../STEP/<m>.step ../renders/<m>.png
  ```
- **注意**：技能原文钉的是 `--managed-python --python 3.13`，本机去掉了 `--managed-python`
  改用已装的 `D:\Python` 3.13.1，省掉一次 uv 自管 Python 的下载。
- 项目布局（按 cad skill 的 `project-layout` 约定）：
  `src/`＝模型入口脚本（一文件一 `@step` 模型），`STEP/`＝产物，`checks/`＝量测脚本，
  `renders/`＝快照图，`.vendor/text-to-cad-latest/`＝上游源码副本（skills 参考文档在这里）。
- **API 坑**：build123d 0.11 的 `bd.Compound()` 收 `children=` 或 `obj=`，
  **不是 `objects=`**（上游 positioning.md 的示例写的就是 `children`）。
- 终端是 GBK，中文 print 会乱码；量测脚本输出建议用英文，或先设 `PYTHONIOENCODING=utf-8`。
- **模型源码必须纯 ASCII**：cadgen 读源码不指定编码，中文注释会炸解析器（2026-10-17 实测）。
- 旧模型（车/场地/结构件）产物写到 `oldSTEP/`，Z 模块写到 `newSTEP/`，不再有 `STEP/`。

## MiMo 技能与拓竹打印（2026-10-17 接入）

- **已装 MiMo 全局技能**（`C:\Users\Spindrift\.config\mimocode\skills\`）：
  - `cad`：text-to-cad 的 CAD 建模技能（含 13 份 references）。建模任务走它，别再只靠本文件摘要。
  - `bambu-labs`：把切片件/模型交给拓竹打印。
- **打印机：拓竹 H2D**（2026-10-23 用户更正，旧记录写的 X2D 是错的）。
  Bambu Studio 在 `D:\Bambu Studio\bambu-studio.exe`（本机已装并配对过机器）。
  双喷嘴机型，成型尺寸 **350×320×325 mm**（`src/print_ready.py` 里的 `BED` 早就是这个值）。
  机型配置含 0.2/0.4/0.6/0.8 喷嘴。
- **打样闭环**：`newSTEP/*.step` → 导出 STL/3MF → 用 Bambu Studio 打开选 **H2D** → 用户切片开打。
  代理只负责打开文件/备好网格，**不代按打印、不读打印机状态**（拓竹官方边界）。
  若要读打印进度，需另接 LAN MQTT（开发者模式）——当前未开。
- 未装 Bambu Connect（仅 Bambu Studio）。已切好的 `.gcode.3mf` 要投递时再装。

## 冰壶实际重量（2026-10-14 用户实测）

**70 g**。这条把投壶的力学量级钉死了：加速到 ~1.2 m/s、行程 80 mm，只需要约 **1.3 N**。

## 结构件清单（`dxf/*.dxf` 重建，全部 5 mm 厚）

规格来源是用户给的 DXF；数值以 `src/parts_data.py` 为准，它是 `src/gen_parts_data.py`
从 DXF 生成的，**不要手改 `parts_data.py`**。

| 模型 | 外形 (mm) | 特征 | 体积 |
|---|---|---|---|
| `six_circle` | 148.677 × 24.360 | 54 孔：48×Ø4 + 6×Ø8，3 行 × 18 列 | 13.5850 cm³ |
| `eight_circle` | 198.340 × 24.360 | 72 孔：64×Ø4 + 8×Ø8，3 行 × 24 列 | 18.1260 cm³ |
| `move_item` | 74.568 × 24.058 | 12 孔 Ø4 + 3 条腰形槽（1×长 62.15、2×长 16.44） | 5.8392 cm³ |
| `short_item` | 49.647 × 24.057 | 14 孔 Ø4 + 1 条腰形槽（长 24.79） | 4.4548 cm³ |
| `wheel` | Ø53.6 × 宽 25.56 | 轴孔 Ø5.9（= 舵机输出轴） | 56.9752 cm³ |
| `l_shape` | 34.5 × 34.5 × 34.5 | 两腿 90° 直角，各 2×3 Ø4.5（贴折弯一排已删）+ 全宽 45° 加强筋 | 10.9310 cm³ |
| `servo_clip` | 60.400 × 39.000 × 5 | 18×Ø4.5 + 42.4×23 通窗（按图保留 1mm 不对称） | 5.4706 cm³ |

`servo_clip` 是后加件（2026-10-17，来源 `dxf/舵机卡扣.dxf`），**不在 `parts_data.py` 里**——
图纸无标注无文字（9 线 + 18 圆），坐标反推后参数直接写在 `src/servo_clip.py`：
孔排 pitch 钉 8.000、窗口 23.001→23.000、重复底边线忽略。窗口按通窗切穿、板厚 5mm、
不对称按图保留，均由用户确认。

`Motor.dxf` **不建模**——它是 40×40×20 舵机的三视图（标注"俯视图/正视图/左视图"），
买件而非加工件。`Whells.dxf` 里那个 168.304 × 25.56 的矩形是**轮周长展开**
（π × 53.6 = 168.30），是计算图不是零件，也不建。

## 从图纸重建时的理想化规则（用户逐条确认过）

1. **列 pitch 钉死 8.25 mm**。图纸孔位有系统性抖动（每行 Y 散布 0.05–0.25 mm，
   X pitch 在 8.02–8.59 飘），名义值就是 8.25。
2. **大孔一律 Ø8.0**。`6circle` 原图标的是 Ø7.6，用户确认为 Ø8。
3. **腰形槽宽 4.5**（不是图纸的 4.0），因为要配 M4 做调节槽，且 3D 打印会吃掉间隙。
   **改槽宽必须同步改两端半径**（R2.0 → R2.25），圆心距保持不变。
4. **对称边距**：保留左边、移动右边，使左右孔边距相等。
5. 每个件生成后必须过 `checks/verify_parts.py`，用鞋带公式独立算面积再乘厚度，
   和 CAD 内核结果对。**六个件当前全部 delta = 0.00000 mm³。**

## 读 DXF 的三个坑（都实际踩过，别再踩）

- **列号不能按"行内第几个"分配**。`Moveitem` 的孔被长槽打断（21.84, 29.87, 38.32, **71.55**），
  顺序索引会把 pitch 拟合错成 14.68。要用全件统一的 `round((x - x_ref)/pitch)` 网格索引。
- **不要用 bbox 定外形尺寸**。图纸的边是斜的，bbox 会系统性偏大：`Shortitem` bbox
  49.730 × **24.285**，标注实为 49.647 × **24.057** —— **差 0.23 mm，会导致零件装不上**。
  优先取 DIMENSION 标注值，没有标注才取两条同向边的均值。
- **提取外框边时只认"纯 LINE 构成的闭合环"**。否则腰形槽的两条直边会被当成板边，
  算出荒谬尺寸（`Moveitem` 曾因此得到 42.4 mm）。

## 未决的结构问题

- **`l_shape` 已按实物反馈修改（2026-10-17）**。腿 24.4→34.5 的放大实物已打印并被接受。
  三处改动：① Ø4 → **Ø4.5**（3D 打印孔径收缩，Ø4 塞不进 M4）；② 贴折弯的两排孔
  （平板 y=9、立板 z=9，共 6 孔）**删除**——孔心到另一条腿的立面只有 4 mm，
  M4 头/垫圈 Ø9（半径 4.5）压不下去，本就装不了东西；
  ③ 直角内角加**全宽 45° 三角加强筋，腿长 7 mm**（"一掰就断"）。**7 是上限**：
  M4 垫圈 Ø9 最远伸到离腿面 12.75 mm，筋的 45° 面到 12.0 mm，再大就顶垫圈。
  给其余 5 个平件（48/64/12/14 个 Ø4 孔）是否也改 Ø4.5 **待用户拍板**。
- **`eight_circle` 板长 198.34 而非标注的 198.66**。它实际拟合 pitch 是 8.2671，钉成
  8.25 后 23 个间距累计压缩 0.39 mm。二选一：接受 198.34，或用 8.2671 保持 198.66。
- **材料**：用户只有亚克力和 PLA 可选。**受力件建议 3D 打印 PLA，不要用激光切亚克力**
  （PMMA 脆断无预警、激光切边留微裂纹、孔边预紧即崩）。
- **真正该做的是把舵机换小**：投壶只需 ~1.3 N，而 40×40×20 级舵机（~10 N·m）堵转时
  往轮缘砸 **~370 N**，差 280 倍。降载荷比加强结构便宜。设计工况是"轮子卡死"，
  不是"投壶那一推"。
