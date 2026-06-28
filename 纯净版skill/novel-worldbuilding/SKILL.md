---
name: novel-worldbuilding
description: 小说世界构建工具。统一管理世界观、地图（动态迷雾解锁）、历法、势力、种族/职业、规则体系、文化禁忌。支持文本、JSON坐标、SVG、HTML四种地图形态。当用户需要创建世界观、管理地图、设计势力、设定规则、保证世界一致性时使用。触发词：世界观、世界构建、地图、历法、势力、种族、职业、规则、设定、地理、大陆、城市、禁忌。
---

# Novel Worldbuilding — 世界构建

统一管理小说的虚构世界设定：世界总览、动态地图、历法、势力、种族/职业、规则体系、文化禁忌。

> **核心原则**：世界设定是 Source of Truth。任何地点、势力、规则、文化细节，必须能在 worldbuilding 中找到依据；找不到的，写作时必须创建或向作者确认。

---

## 一、工作区规范

```
.novel/
├── worldbuilding/
│   ├── world.md                        # 世界总览（核心规则、基调、一句话）
│   ├── world.html                      # AI 消费层
│   ├── map/
│   │   ├── world-map.md                # L0 全局地图（文本关系图 + ASCII）
│   │   ├── world-map.json              # 结构化地理数据
│   │   ├── world-map.svg               # SVG 可视化
│   │   ├── world-map.html              # 完整交互式地图页面
│   │   ├── regions/
│   │   │   ├── {区域名}.md             # L1 区域
│   │   │   ├── {区域名}.json           # 区域结构化数据
│   │   │   └── {区域名}.svg
│   │   ├── cities/
│   │   │   ├── {城市}.md               # L2 城市
│   │   │   ├── {城市}.json             # 城市结构化数据
│   │   │   └── {城市}.svg
│   │   └── scenes/
│   │       ├── {场景}.md               # L3 场景（建筑、街道）
│   │       ├── {场景}.json             # 场景结构化数据
│   │       └── {场景}.svg
│   ├── timeline/
│   │   ├── calendar.md                 # 历法、纪年、季节、节日
│   │   └── eras.md                     # 世界历史纪元
│   ├── factions/
│   │   ├── {势力}.md                   # 国家、公司、家族、门派
│   │   └── relations.md                # 势力关系图谱
│   ├── identities/
│   │   ├── races.md                    # 种族（玄幻/科幻）
│   │   ├── professions.md              # 职业/身份体系
│   │   └── statuses.md                 # 社会阶层
│   ├── systems/
│   │   ├── magic.md                    # 魔法/异能/金手指
│   │   ├── technology.md               # 科技水平/限制
│   │   ├── economy.md                  # 货币、贸易、资源
│   │   └── laws.md                     # 法律/物理/社会规则
│   └── culture/
│       ├── customs.md                  # 风俗、礼仪、节日
│       ├── taboos.md                   # 禁忌、红线
│       └── languages.md                # 方言、黑话、特殊用语
└── tracking/
    ├── worldbuilding-usage.json        # 设定引用记录
    └── worldbuilding-changes.json      # 世界设定变更记录
```

---

## 二、核心模块说明

### 2.1 世界总览（world.md）

任何人在进入具体设定前，必须先读世界总览。它回答：

- 这是一个什么样的世界？
- 核心规则是什么？（物理、魔法、科技、社会）
- 故事的主题基调是什么？
- 最大的禁忌/红线是什么？

**world.md 模板**：

```markdown
---
name: {世界名}
genre: {题材：都市穿越/玄幻/科幻/...}
tone: {基调：热血/暗黑/轻松/史诗/...}
version: 1.0.0
locked: true                        # 是否已加设定锁
---

## 一句话世界观

{用一句话概括这个世界}

## 核心规则

1. **物理规则**：{如：与地球一致 / 存在灵气 / 有超光速航行}
2. **力量规则**：{如：普通人无法修炼 / 科技上限为 22 世纪}
3. **社会规则**：{如：阶层固化 / 宗门统治 / 公司共和国}
4. **时间规则**：{如：一年 12 个月，一天 24 小时}

## 主题基调

- {基调关键词 1}
- {基调关键词 2}
- {基调关键词 3}

## 最大禁忌

- {禁忌 1}
- {禁忌 2}

## 与现实的差异

- {差异 1}
- {差异 2}
```

---

### 2.2 动态地图系统

地图不是一次性画完的，而是随正文描写逐步解锁、细化的**迷雾地图**。

#### 2.2.1 地图层级

| 层级 | 范围 | 初始状态 | 解锁方式 | 可视化 |
|------|------|---------|---------|--------|
| **L0 世界图** | 全球/全大陆/全书主要区域 | 已解锁 | 项目初始化 | 文本关系图 + ASCII + SVG + HTML |
| **L1 区域图** | 省/州/大陆片区/城市集群 | 迷雾 | 正文首次提到 | 文本 + JSON + SVG + HTML |
| **L2 城市图** | 单个城市内部 | 迷雾 | 正文首次进入 | 文本 + JSON + SVG + HTML |
| **L3 场景图** | 建筑、街道、室内 | 迷雾 | 正文首次描写 | 文本 + JSON + SVG + HTML |
| **L4 动态细节** | 场景内物品、人物位置 | 迷雾 | 正文描写到具体细节 | 文本 + JSON |

#### 2.2.2 解锁流程

```
每章写完后
  ↓
AI 扫描正文，提取地名、新地点、相对位置、交通方式/时间
  ↓
生成 map-update-suggestion.md
  ↓
作者确认 / 修改建议
  ↓
写入对应层级 .md + .json
  ↓
调用 generate_map.py 重新生成 .svg + .html
  ↓
在 worldbuilding-changes.json 中记录变更
```

**脚本调用**：
```bash
python3 .novel/scripts/generate_map.py \
  .novel/worldbuilding/map/world-map.json \
  -o .novel/worldbuilding/map/
```

**map-update-suggestion.md 模板**：

```markdown
## 第 {N} 章地图升级建议

### 新增地点

| 地点 | 层级 | 相对位置 | 首次出现 | 建议操作 |
|------|------|---------|---------|---------|
| {地名} | L2 | {相对位置} | ch{N} | 创建城市档案 |

### 升级已有地点

| 地点 | 原层级 | 新层级 | 触发章节 | 建议操作 |
|------|--------|--------|---------|---------|
| {地名} | L2 | L3 | ch{N} | 添加场景细节 |

### 新增连接

| 起点 | 终点 | 交通方式 | 时间 | 触发章节 |
|------|------|---------|------|---------|
| {A} | {B} | 马车 | 6h | ch{N} |

### 潜在冲突

- {描述}
```

#### 2.2.3 地图档案 Markdown 规范

**城市档案示例**：

```markdown
---
name: 东海城
type: 城市
region: 东大陆·滨海平原
level: L2
unlocked_by: ch03
first_mentioned: ch01
coordinates:
  relative_to: 东大陆
  x: 0.7
  y: 0.3
population: 120万
climate: 温带季风
ruling_faction: 东海商会
connected_to:
  - target: 青云镇
    method: 马车
    time: 6小时
  - target: 王都
    method: 飞艇
    time: 2天
---

## 地理描述

背靠青云山脉，面向怒涛海峡。城市沿港口呈带状分布。

## 已知区域

| 区域 | 类型 | 首次出现 | 状态 |
|------|------|---------|------|
| 上城区 | 城区 | ch03 | 已解锁 |
| 下城区 | 城区 | ch05 | 已解锁 |
| 黑礁巷 | 地下街区 | ch03 | 已解锁 |
| 海天楼 | 建筑 | ch07 | 已知但未详细描写 |

## 迷雾区域

- 北郊矿山
- 西海岸线

## ASCII 地图

```text
         [青云山脉]
              │
    [王都]──[东海城]──[怒涛海峡]
              │
         [上城区]─[下城区]─[港口区]
              │
         [海天楼]  [黑礁巷]
```

## 禁忌与风俗

- 港口忌说"沉"字
- 商会谈判前必饮海盐茶
```

#### 2.2.4 地图结构化数据规范

**world-map.json**：

```json
{
  "name": "{世界名}",
  "level": "L0",
  "coordinate_system": "relative_2d",
  "regions": [
    {
      "name": "东大陆",
      "level": "L1",
      "unlocked_by": "init",
      "coordinates": {"x": 0.7, "y": 0.3},
      "file": "regions/东大陆.json"
    }
  ],
  "connections": [
    {"from": "东大陆", "to": "西大陆", "method": "远洋航线", "time": "3个月"}
  ],
  "fog_of_war": ["北境冰原", "南海群岛"]
}
```

**{城市}.json**：

```json
{
  "name": "东海城",
  "type": "城市",
  "level": "L2",
  "unlocked_by": "ch03",
  "first_mentioned": "ch01",
  "coordinates": {"relative_to": "东大陆", "x": 0.7, "y": 0.3},
  "districts": {
    "上城区": {"level": "L3", "unlocked_by": "ch03", "scenes": ["海天楼"]},
    "下城区": {"level": "L3", "unlocked_by": "ch05", "scenes": ["黑礁巷"]}
  },
  "connections": [
    {"to": "青云镇", "method": "马车", "time": "6h"},
    {"to": "王都", "method": "飞艇", "time": "2d"}
  ],
  "fog_of_war": ["北郊矿山", "西海岸线"]
}
```

#### 2.2.5 地图可视化

**文本关系图**：使用 Markdown 表格 + Mermaid 图描述。

**ASCII 地图**：在 `.md` 文件中用代码块展示，便于快速查看。

**SVG 地图**：基于 JSON 坐标自动生成，区分：
- 已解锁区域（实线、亮色）
- 迷雾区域（虚线、灰色）
- 当前章节涉及区域（高亮）

**HTML 交互地图**：完整页面，支持：
- 缩放、拖拽
- 层级切换（L0/L1/L2/L3）
- 点击查看地点详情
- 显示解锁章节
- 显示当前故事进度所在位置

---

### 2.3 时间历法（timeline/）

#### 2.3.1 历法（calendar.md）

```markdown
---
name: {历法名}
anchor_story_date: {故事第1天对应的历法日期}
real_anchor: {可选：对应现实日期}
locked: true
---

## 纪年法

- {历法名} {元年} 年 = {现实年份}
- 1 年 = {N} 个月
- 1 个月 = {N} 天
- 1 天 = {N} 小时

## 四季/节气

| 季节 | 月份 | 特征 |
|------|------|------|
| {春} | {1-3} | {特征} |

## 重要节日

| 节日 | 日期 | 习俗 | 故事意义 |
|------|------|------|---------|
| {海祭} | {3月15日} | {庆典} | {chXX 关键剧情} |

## 与故事日期换算

- 故事第 1 天 = {历法日期}
- 故事第 30 天 = {历法日期}
```

#### 2.3.2 历史纪元（eras.md）

记录世界重大历史阶段，供大纲和角色背景参考。

---

### 2.4 势力系统（factions/）

#### 2.4.1 势力档案

```markdown
---
name: {势力名}
type: {国家/公司/家族/门派/组织}
leader: {领袖}
headquarters: {总部地点}
alignment: {正义/中立/邪恶/灰色}
status: {活跃/衰落/隐秘}
locked: false
---

## 势力简介

{简介}

## 核心目标

- {目标 1}
- {目标 2}

## 与主角关系

- {阶段}：{描述}

## 与外部势力关系

| 势力 | 关系 | 起始章节 | 说明 |
|------|------|---------|------|
| {势力A} | 敌对 | ch01 | {说明} |
| {势力B} | 同盟 | ch05 | {说明} |
```

#### 2.4.2 势力关系图谱

`relations.md` 用文字表格或 Mermaid 图表示。

---

### 2.5 身份体系（identities/）

#### 2.5.1 种族（races.md）

适用于玄幻/科幻题材。

```markdown
| 种族 | 寿命 | 天赋 | 弱点 | 社会地位 |
|------|------|------|------|---------|
| {人族} | {80年} | {无} | {无} | {主流} |
| {妖族} | {300年} | {化形} | {惧雷} | {边缘} |
```

#### 2.5.2 职业/身份（professions.md）

```markdown
| 职业 | 能力范围 | 社会定位 | 常见组织 | 限制 |
|------|---------|---------|---------|------|
| {法师} | {元素操控} | {高贵} | {法师塔} | {魔力上限} |
```

#### 2.5.3 社会阶层（statuses.md）

```markdown
| 阶层 | 特征 | 流动方式 | 代表人物 |
|------|------|---------|---------|
| {贵族} | {世袭} | {军功/联姻} | {角色A} |
```

---

### 2.6 规则体系（systems/）

#### 2.6.1 魔法/异能/金手指（magic.md）

```markdown
---
name: {体系名}
locked: true
---

## 基本原理

{原理}

## 等级/境界

| 等级 | 特征 | 限制 |
|------|------|------|
| {一级} | {特征} | {限制} |

## 使用代价

- {代价 1}
- {代价 2}

## 主角当前等级

- {等级}（chXX 达到）
```

#### 2.6.2 科技水平（technology.md）

记录科技上限、已出现技术、禁用技术。

#### 2.6.3 经济体系（economy.md）

货币、贸易、资源分布。与 `novel-knowledge` 的物价表联动。

#### 2.6.4 法律/规则（laws.md）

社会规则、物理规则、世界红线。

---

### 2.7 文化风俗（culture/）

#### 2.7.1 风俗礼仪（customs.md）

节日、婚礼、葬礼、见面礼、饮食习俗等。

#### 2.7.2 禁忌红线（taboos.md）

社会禁忌、宗教禁忌、政治敏感、flag。

#### 2.7.3 语言/方言（languages.md）

特殊用语、黑话、方言对照。

---

## 三、设定锁机制

### 3.1 需要加锁的设定

- 世界物理/魔法/科技底层规则
- 主角金手指机制与限制
- 重大势力关系（如两国敌对、家族世仇）
- 历法核心参数
- 社会核心禁忌

### 3.2 变更流程

1. 用户提出变更需求。
2. AI 读取当前设定，评估影响范围。
3. 生成影响报告：受影响的章节、角色、大纲节点。
4. 作者确认后，更新设定并提升版本号。
5. 在 `worldbuilding-changes.json` 中记录：

```json
{
  "changes": [
    {
      "id": "wb-001",
      "file": "worldbuilding/systems/magic.md",
      "field": "主角当前等级",
      "old_value": "一级",
      "new_value": "二级",
      "reason": "chXX 获得奇遇",
      "impact_chapters": ["chXX", "chXX+1"],
      "approved_by": "作者",
      "date": "2026-06-28"
    }
  ]
}
```

6. 若变更涉及地理/地点，调用 `generate_map.py` 重新生成受影响层级的 SVG/HTML 地图：
   ```bash
   python3 .novel/scripts/generate_map.py \
     .novel/worldbuilding/map/cities/{城市}.json \
     -o .novel/worldbuilding/map/cities/
   ```
7. 触发受影响章节的重新质检。

---

## 四、AI 上下文注入

写作/审稿时，必须注入世界观上下文：

```markdown
[世界观上下文]
世界总览：{一句话}
当前地点：{城市/区域} — {地理特征}，{势力控制}
当前日期：{纪年} — {季节/节日}
相关势力：{势力名}（与主角关系：{关系}）
规则注意：{魔法/科技/社会限制}
禁忌：{文化禁忌}
地图状态：{已解锁地点 / 附近迷雾区域}
```

---

## 五、与现有 Skill 的协作

### 5.1 novel-writing

- 读上下文顺序：大纲 → 角色 → **世界观** → 知识 → 追踪 → 进度
- 写任何地点/势力/规则前必须先查 worldbuilding
- 新增地点/势力/规则必须同步创建 worldbuilding 档案
- 上下文注入模板增加 `[世界观上下文]`

### 5.2 novel-humanizer

- 新增评分维度「世界观一致性」
- 检测地点是否存在、地理移动是否合理、势力关系是否一致、规则是否超限

### 5.3 novel-review

- 作者视角新增「世界观一致性」检查项
- 毒点清单新增世界观相关 P0/P1/P2

### 5.4 novel-logic

- **地理移动校验**：角色从 A 到 B 的时间、交通方式、距离依赖 `worldbuilding/map/*.json`
- **地点一致性校验**：正文中出现的地点必须在 `worldbuilding/map/` 中有对应档案
- **层级校验**：未解锁区域不能出现超出其层级的细节
- **势力关系校验**：角色行为是否符合 `worldbuilding/factions/relations.md`
- **信息边界校验**：角色在某地出现/获得信息是否合理

**协作流程**：
1. novel-logic 写本章冻结状态时，读取 worldbuilding 地图和势力数据
2. 每个场景微逻辑卡填写时，校验地点、势力、规则是否与世界building一致
3. 动作前四问中「这个信息/道具/称呼从哪来的？」需要查询 worldbuilding 档案
4. 逻辑矩阵生成时，地理移动数据来自 worldbuilding JSON

### 5.5 与修改模式的协作

- **修改涉及地点时**：由 novel-worldbuilding 判断地点信息是否变化，变化时重新生成地图
- **修改涉及势力/规则时**：更新 worldbuilding 档案，但不必重走完整世界构建流程
- **修改模式下不触发**：地图升级建议扫描（除非用户主动要求）
- **修改模式最小同步**：只更新与本次修改直接相关的 worldbuilding 文件

### 5.6 novel-knowledge

- knowledge 管真实历史、物价、品牌、考据资料
- worldbuilding 管虚构设定、地图、历法、势力、规则

### 5.7 novel-character

- 角色档案 `faction` / `race` / `profession` 字段必须能在 worldbuilding 中找到对应

### 5.8 novel-outline

- 每章大纲增加「世界观约束」字段
- 大纲调整涉及地点/势力/规则变更时，触发世界设定影响分析

---

## 六、使用方法

### 初始化世界观

```
用户：帮我初始化一个都市穿越世界观
→ 选择模板 → 生成 worldbuilding/ 目录结构
→ 生成 world.md、基础地图、历法、势力框架
```

### 创建地点

```
用户：新增一个地点"黑礁巷"
→ 创建 worldbuilding/map/scenes/黑礁巷.md
→ 更新所属城市 JSON
→ 生成/更新 SVG 和 HTML 地图
```

### 地图升级建议

```
用户：第 5 章写完了，帮我看看地图要不要更新
→ 扫描正文 → 生成 map-update-suggestion.md
→ 作者确认 → 写入地图档案
```

### 修改核心设定

```
用户：我想把主角金手指的限制改一下
→ 评估影响 → 生成影响报告
→ 作者确认 → 更新 systems/magic.md
→ 记录 worldbuilding-changes.json
→ 触发受影响章节重新质检
```

---

## 七、写作纪律

1. **先查后写**：写到任何地点、势力、规则、文化细节前，先查 worldbuilding。
2. **一地一档**：每个出现的地名，必须有对应档案（L1/L2/L3 按需）。
3. **一地一坐标**：每个地点在结构化数据中有相对位置，避免地理穿帮。
4. **设定锁**：核心设定一旦写入，修改必须走变更流程。
5. **冲突即停**：正文与 worldbuilding 冲突时，优先按 worldbuilding 修正正文，或向作者申请修改设定。
6. **地图随正文生长**：每章写完后，根据正文描写升级/解锁地图。
7. **新增势力/规则/种族必须先建档**：不得在正文中凭空创造未在 worldbuilding 中备案的设定。

---

## 八、配置项

`.novel/skills/skill-worldbuilding.json`：

```json
{
  "auto_map_suggest_on_save": true,
  "map_visualization": {
    "enable_ascii": true,
    "enable_svg": true,
    "enable_html": true
  },
  "locked_fields": [
    "world.md:core_rules",
    "systems/magic.md",
    "timeline/calendar.md:calendar_params",
    "factions/relations.md"
  ],
  "map_levels": {
    "L0": {"unlock": "init"},
    "L1": {"unlock": "mentioned"},
    "L2": {"unlock": "entered"},
    "L3": {"unlock": "described"},
    "L4": {"unlock": "detailed"}
  },
  "consistency_check": {
    "distance_tolerance": 0.2,
    "time_tolerance": 0.1,
    "require_faction_alignment": true
  }
}
```

---

## 九、禁止行为

- ❌ 不查世界设定直接写地点、势力、规则
- ❌ 新增地点/势力/规则不建档
- ❌ 角色行为违反所属势力/种族/职业设定
- ❌ 未经审批修改带锁的核心设定
- ❌ 地理移动不合理（瞬移、时间矛盾）
- ❌ 地图档案与正文描述不一致
- ❌ 只给文字建议不执行工具操作
