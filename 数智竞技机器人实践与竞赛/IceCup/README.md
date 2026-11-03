# IceCup — 项目交接说明

> **2026-10-29 活动已结束，全部文件已归档整理：先读 `整理说明.md`**（最终交付件在 `成品\`）。

> 给人类读的入口。给 agent 读的规则在 `AGENTS.md`（会被自动加载），那份里有完整的赛规尺寸表、
> 工具链决策理由、以及踩过的坑。**两份都要带上**，这份只讲"怎么在新机器上跑起来"和"现在到哪一步了"。

## 一句话状态

哈工大冰壶机器人对抗赛。赛规已读、基准几何与六个结构件已建成 CAD 并通过体积校核、
`cadgen` 工具链已跑通、Z 轴升降模块已建完并通过干涉校核。**取壶方式仍未定**。
**本文"到哪一步"这部分写完于 2026-10-14，已过期；以 `PROGRESS.md` 为准**（2026-10-17 交接文档）。

## 目录

| 路径 | 是什么 | 要拷吗 |
|---|---|---|
| `AGENTS.md` | **规则尺寸表 + 工具链决策 + 环境坑**，agent 自动读 | **必须** |
| `README.md` | 本文件 | 必须 |
| `src/` | **模型本体**（参数化 Python，改尺寸改这里） | **必须** |
| `checks/` | 量测脚本，算出取壶包络 | 必须 |
| `oldSTEP/` `newSTEP/` | 导出的中性几何（老件 / Z 模块），SolidWorks 直接开 | 可拷可重建 |
| `GLB/` `renders/` | 网格和渲染图，纯产物 | 不用拷 |
| `.vendor/` | text-to-cad 上游源码副本，只当参考文档读（762K） | 不用拷，可重下 |

`oldSTEP/spur_gear.step` 有 12.6 MB，是那个演示齿轮（48 齿 × 折线采样），占了文件夹绝大部分体积。
它不是机器人零件，删了不心疼，`python spur_gear.py` 30 秒能重建。

整个目录约 17 MB，去掉演示齿轮约 4 MB。

## 换电脑要做的事

脚本里**没有任何绝对路径**，输出都是相对脚本位置的 `../oldSTEP/`（老件）或 `../newSTEP/`
（Z 模块），所以代码本身直接拷走就能用。
要重装的是运行时依赖：

### 1. 前置检查（两条，都是硬条件）

- **Python 3.11+**（本机用的 3.13.1）
- **Windows 11 要看 Smart App Control 是否关闭**。cadgen 依赖的 OCP（OpenCascade 绑定）
  wheel 带未签名 native module，SAC 开着会 `ImportError: DLL load failed while importing OCP`，
  且**没有按应用豁免**。查：
  ```powershell
  reg query "HKLM\SYSTEM\CurrentControlSet\Control\CI\Policy" /v VerifiedAndReputablePolicyState
  ```
  `0x0` = 关，可以直接用。非 0 = 开，只能"关掉 SAC（**关闭后只能重装系统才能恢复**）"或"改用 WSL"。
  本机是 `0x0`，所以这条路是通的。

### 2. 装 uv

```powershell
python -m pip install uv ezdxf -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

`ezdxf` 是读 DXF 用的（`src/gen_parts_data.py` 和 `checks/dxf_*.py` 依赖它）；
只用 cadgen 建模、不重新从图纸生成数据的话可以不装。

装完确认 `uv` / `uvx` 在 PATH 里（本机的 `D:\Python\Scripts` 不在 PATH，所以下面所有命令前
都要 `export PATH="/d/Python/Scripts:$PATH"`；新机器上如果在 PATH 里就不用）。

**注意 PyPI 直连可能不可靠**：本机实测 `pypi.org` 会在约 746 KB 处截断连接，`pip install`
直接卡死。所以上面那条**必须带 `-i` 国内镜像**。新机器如果网络环境不同，可能不需要。

### 3. 验证 cadgen 能跑

cadgen 本身不用装，`uvx` 首次调用时自动下载（约 58 个包）。

```bash
export UV_DEFAULT_INDEX="https://pypi.tuna.tsinghua.edu.cn/simple/"
uvx --no-config --python 3.13 --from "cadgen==0.7.21" cadgen doctor
```

看到 `kernel OK` 就成了。然后**第一件事关遥测**：

```bash
uvx --no-config --python 3.13 --from "cadgen==0.7.21" cadgen telemetry off
```

### 4. 重建全部模型

```bash
export UV_DEFAULT_INDEX="https://pypi.tuna.tsinghua.edu.cn/simple/"
export CADGEN_TELEMETRY=0
cd <项目>

# 结构件：先从 DXF 生成理想化数据，再建模，再校核
PYTHONIOENCODING=utf-8 python src/gen_parts_data.py     # 需要 ezdxf + dxf/*.dxf
cd src
for m in six_circle eight_circle move_item short_item wheel l_shape \
         curling_stone stone_rack rack_loaded spur_gear; do
  uvx --no-config --python 3.13 --from "cadgen==0.7.21" python $m.py
done
cd ..
uvx --no-config --python 3.13 --from "cadgen==0.7.21" \
  python checks/verify_parts.py                          # 应输出 FAILURES: 0
```

`gen_parts_data.py` 会**拒绝**输出不合格的数据（拟合残差超限、孔跑出轮廓），
所以它在没通过时是非零退出，不会静默生成坏坐标。

## 常用命令速查

```bash
# 三个环境变量，每次开新 shell 都要
export UV_DEFAULT_INDEX="https://pypi.tuna.tsinghua.edu.cn/simple/"
export PATH="/d/Python/Scripts:$PATH"
export CADGEN_TELEMETRY=0
export PLAYWRIGHT_DOWNLOAD_HOST="https://cdn.npmmirror.com/binaries/playwright"  # 渲染才需要

# 建模（改完 src/*.py 后）
cd src && uvx --no-config --python 3.13 --from "cadgen==0.7.21" python <model>.py

# 渲染成 PNG（--camera 可给 front/back/left/right/top/bottom/iso 或 "方位角:仰角"）
uvx --no-config --python 3.13 --from "cadgen==0.7.21" \
  cadgen step snapshot oldSTEP/<m>.step renders/<m>.png --camera front

# 导 STL 去 3D 打印
uvx --no-config --python 3.13 --from "cadgen==0.7.21" \
  cadgen stl build oldSTEP/<m>.step STL/<m>.stl

# 算取壶包络（纯 Python，不需要 cadgen）
python checks/reach_envelope.py
```

**渲染有个坑**：`cadgen step snapshot` 首次要下载 Playwright Chromium。默认 CDN
`playwright.azureedge.net` 已退役（返回 307），会**静默挂住十几分钟没有任何输出**。
必须设 `PLAYWRIGHT_DOWNLOAD_HOST` 指到 npmmirror。不想折腾就别渲染，
STEP 直接拖进 SolidWorks 看更省事。

## 现在到哪一步了

### 已定（不要再讨论）

- **SolidWorks 2024 = 主 CAD**，所有自己设计的零件在里面建
- **cadgen = 客观基准件 + 概念探索**，不是主 CAD；它自带独立内核，**不驱动 SolidWorks**
- **取壶架和冰壶当"外部参考件"**导进 SW 装配体，不重画 → 两边各有权威源，不分叉
- **MoveIt / SRDF 已从链路删除**：真实约 5 DOF，但取壶是"到位→直上直下→闭合"、
  投壶是"贴瞄准辅助线→直线推"，**没有 IK 也没有位形规划需求**
- **仿真优先级 A > B > C**：A 冰壶滑多远（1D，几十行 Python，现在就能做）
  > B 取壶能否取到（SW 干涉检查 / 3D 打印手试）> C 整机 2 分钟流程（**不装仿真器**，2026-10-17 定）
- 冰壶几何已按图纸重建并逐高度实测校核；撞击带中心三来源 **10.90 / 11.05 / 12.0 mm**
  散布 1.1 mm → 推壶接触面按 **10.4–12.5 mm 可调**设计，不再是单值

### 已建成的结构件（2026-10-14，`dxf/*.dxf` → STEP）

六个件全部 5 mm 厚，规格表和理想化规则在 `AGENTS.md`，数值以 `src/parts_data.py` 为准
（它是 `src/gen_parts_data.py` 生成的，**不要手改**）。每个件都过 `checks/verify_parts.py`，
解析体积与 CAD 体积 **delta 全部 0.00000 mm³**。

`Motor.dxf`（舵机三视图）和 `Whells.dxf` 里的周长展开矩形**不建模**——它们是参考图/计算图。

### 还欠的事实

1. ~~取壶架的格子有没有背板~~ **已答（2026-10-16）：有 2 mm 亚克力背板**，
   内深 58 → "从后方顶出"类方案作废
2. **架体是否立在地面上**——影响 Z 行程 208.5 mm 的起算基准（尚未量，参数 `PLATFORM_HEIGHT`）
3. **场地表面是什么**：真冰 / 人造冰板（PTFE、HDPE）/ 组委会发的塑料面板 → 决定摩擦系数

**拿到第 3 条就能立刻做 A**（μ 波动 ±20% 时落点差多少 → 反推控制精度要求）。
**2 拿到才能定取壶机构**（现状详见 `PROGRESS.md` §3）。

### 仍然未定的设计决策

- **取壶方式**——候选已换过一轮，见 `PROGRESS.md` §3.4（磁吸手柄顶盖 / 抓 Ø11 手柄 / 侧夹 / 笼罩）；
  铲叉、底部磁吸、从格后顶出均已排除
- ~~仿真器~~ **已决定：不装**（主控是 Arduino 不是 ROS 2，Gazebo 的复用价值不存在；μ 只能实测）
- **材料**：受力件用亚克力还是 PLA。我的主张是 **3D 打印 PLA，不要激光切亚克力**
  （PMMA 脆断无预警、激光切边留微裂纹、孔边预紧即崩），他未表态
- **舵机规格**：壶重实测 **70 g** → 投壶只需 ~1.3 N，但 40×40×20 级舵机（~10 N·m）
  堵转时往轮缘砸 **~370 N**。**设计工况是"轮子卡死"不是"投壶那一推"**，差 280 倍，
  降舵机规格比加强结构便宜。这条提过两次，还没结论。
- ~~`l_shape` 的腿从 24.4 长到 34.5~~ **已定（2026-10-17）**：34.5 实物已打印并接受；
  孔改 Ø4.5、靠折弯一排删除、内角加 45° 加强筋（详见 `AGENTS.md`）
- **`eight_circle` 板长 198.34 而非标注的 198.66**——pitch 钉 8.25 后累计压缩 0.39 mm。

### 已经算出来的设计约束（讨论直接用）

| 约束 | 值 |
|---|---|
| 取壶机构 Z 行程 | **208.5 mm**（壶心 32.2 → 上层壶顶 240.8） |
| 夹爪侧向间隙 | **单侧 16.5 mm**（格口 80 − 壶径 47） |
| 壶前面板凹进 | **6.5 mm** → **不能沿前后方向闭爪** |
| 壶上方净空 | **48 mm** → 夹爪本体可坐在壶上方 |
| 推壶接触高度 | **11–12 mm**，不用留大范围调节 |
| 换列位移 | **96.25 mm**，必须靠底盘移动 |
| 机器人投影限值 | 350 × 350 mm，高度不限 |
| 单次取+投时限 | 120 s（**很宽松，可靠性压倒速度**） |
| 判负条件 | 取壶过程中壶**翻转或掉落至界外区** |

## 不在文件夹里的东西

Qoder 的项目记忆存在 `C:\Users\Spindrift\.qoder-cn\projects\D--IceCup\memory\`
和 `...\memory\`（用户级），**不在 `D:\IceCup` 里，拷文件夹不会带上**。

里面是"你怎么和我协作"的偏好（deliver-first、"不动手"=只评估、说"CAD"指 AutoCAD、
会拿别的 AI 的方案回来让我评审）和三条项目记忆。丢了不影响任何代码，
新机器上重新说一遍就行。要保险就把这两个目录也一起拷走。
