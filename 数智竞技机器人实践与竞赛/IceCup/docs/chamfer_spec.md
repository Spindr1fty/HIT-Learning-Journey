# 倒角规范（g_mount_b 风格）—— 2026-10-23

> 用户要求："`newSTEP/g_mount_b.step` 这样的倒角先记一下，等下发四个文件你也像这样做"。
> 以后任何件要"照 g_mount_b 倒角"，按本文执行。

## 1. 规则

| 项 | 值 |
|---|---|
| 形式 | **45° × 1.0 mm 对称倒角**（`--size` 可改） |
| 位置 | **外部凸棱**（自动探测） |
| 底面 | **不动**（留完整平面贴热床/贴板） |
| 孔口（圆棱） | **不动**（Ø4.5 孔边到外形/邻孔很近，倒角会啃穿） |
| 螺丝承压面 | **看件决定**，用 `--skip-plane` 排除；g_mount_b 是 `x=0` |
| 碎边 | 短于 **1.0 mm** 的不动 |

**凸/凹判定**：在棱中点、垂直棱的圆环上打 24 个探针（半径 0.15），
超过一半落在空气里 → 凸棱 → 倒；否则凹棱 → 跳过。

**倒不全时的退让**：先整组倒；OCCT 拒绝就递归二分（一次被拒的边不连累其它边）；
被拒的边再按 **0.6 / 0.4 / 0.3 倍**尺寸重试；仍拒绝的打印坐标，肉眼判断是否可忽略。

## 2. g_mount_b 上的实施结果（rev 30）

```
候选凸棱 33 条 → 倒成 31 条（2 条是法兰槽口 2.5mm 小棱，OCCT 拒绝，可忽略）
体积 16.738 → 16.569 cm³（−0.169）
面数 35 → 68，边数 106 → 197，valid=True，单实体，外形 40 × 74.5 × 29 不变
故意不倒：X=0 前面（4×M4 头压在 8 mm 宽面上，头对角 8.1）
          底面 Z=9、Ø4.5 孔口
副作用：法兰与柱内侧面贴合带 4.0 → 3.0 宽（被 Y=29.94 那条棱的倒角吃掉 1mm）
```

代码在 `src/g_mount_b.py` 里的 `chamfered()`（内嵌，件自身能独立重建）。

## 3. 通用工具（给别的件用）

`src/chamfer_part.py` —— 对任意 **素件** STEP 套同一套规则：

```powershell
cd D:\IceCup\src

# 1) 先看候选棱（不动手）
python chamfer_part.py ..\newSTEP\某件.step --report

# 2) 正式做（可加多个承压面排除）
python chamfer_part.py ..\newSTEP\某件.step ..\newSTEP\某件_chamfer.step --skip-plane x=0

# 3) 顺带出 STL
python chamfer_part.py in.step out.step --size 1.0 --stl out.stl
```

参数：`--size`（默认 1.0）、`--skip-plane AXIS=VALUE`（可重复）、`--no-bottom`、
`--min-edge`、`--report`、`--stl`。

**输入必须是还没倒过角的 STEP**；已倒过角的再跑一次会把倒角面自己的边再切一刀。

## 4. 自测记录

拿 `g_mount_b` 的素件（`M.bracket()`）导出 STEP，再用通用工具跑一遍：

```
input  16.738 cm3  →  output 16.569 cm3 (−0.169)  valid True
和正式件 g_mount_b.step 完全一致（同样 2 条槽口棱被拒）
```

即：工具与内嵌实现等价，可以放心套到别的件上。


---

## 5. 2026-10-23 四个 3MF 件（u_clamp / base_plate / plunger / rack）—— 暂停点

用户要求在四个件上做同样的 1 mm 倒角，**先出缩略图确认再动手**。
文件在 `C:\Users\Spindrift\Desktop\`：`u_clamp(1).3mf`、`base_plate.3mf`、
`plunger.3mf`、`rack.3mf`。用户 2026-10-23 13:05 让先停。

### 关键事实：这四件**只有网格，没有 B-rep**
3MF 里是三角面片（u_clamp 1940 面 / base_plate 13756 / plunger 7442 / rack 2284），
没有 STEP。所以不能直接用 `chamfer_part.py`，先得转回 B-rep。

| 件 | 外形 (mm) | 三角面 | 网格体积 | 原始网格是否闭合 |
|---|---|---|---|---|
| u_clamp(1) | 117.6 × 113.7 × 70.0 | 1940 | 33.28 cm³ | ❌ 否 |
| base_plate | 99.0 × 252.0 × 66.5 | 13756 | 219.99 cm³ | ❌ 否 |
| plunger | 16.0 × 251.3 × 24.5 | 7442 | 89.93 cm³ | ✅ 是 |
| rack | 16.0 × 243.3 × 24.5 | 2284 | 83.98 cm³ | ✅ 是 |

四件都在同一个装配坐标系里（不是原点），渲染时按包围盒居中。

### 已经跑通的路：网格 → B-rep（`src/mesh2brep.py`）
OCCT 缝合三角面 → `ShapeUpgrade_UnifySameDomain` 合并共面 → MakeSolid：
- **rack 成功**：2284 面缝成 1 个壳，unify 后 **560 面**，Solid **valid**，
  体积 83.98 cm³（与网格一致），外形 16.0 × 243.3 × 24.5 不变
  → `newSTEP/upload_rack_brep.step`
- **尚未跑**：u_clamp、base_plate、plunger（u_clamp/base_plate 网格本身不闭合，
  缝合后可能不是闭合壳，需先补洞或调 sewing 容差）

### 没走通的路：直接在网格上倒角（`src/mesh_chamfer.py`）
思路是"每条凸棱生成一张 45° 切平面，用 trimesh 顺序切"。
问题：网格是 CAD 细分出来的，齿纹/圆角处有大量微小三角形，
按三角形法向算出的切平面不可靠（个别平面会把件切成两半）。
加了"共面区域聚类 + 两侧面积阈值 + 切除体积预算"三重过滤后，
rack 只剩 10 张可靠平面（应远不止），倒角覆盖率太低。**建议放弃这条路，走 B-rep**。

### 恢复时要做的
1. 先跑 `mesh2brep.py` 把四件都转成 STEP（u_clamp/base_plate 可能需要先补洞，
   或在 trimesh 里 `fill_holes()` 后导出干净 STL 再缝）。
2. 用 `chamfer_part.py --min-face-area 25`（避开碎面）在 B-rep 上倒角；
   底面默认不动，螺丝承压面按件用 `--skip-plane` 排除。
3. 出 4 张倒角后的缩略图给用户确认，确认后再出正式 STEP/STL。
4. 若用户其实有这四个件的 **STEP/源文件**，那最省事——直接要 STEP，跳过网格重建。
