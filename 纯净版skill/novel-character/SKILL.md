---
name: novel-character
description: 小说角色档案管理工具。管理角色卡、言行一致性检测、关系图谱、角色弧线、出场统计。当用户需要创建/编辑角色、查看角色档案、检测角色言行一致性、管理角色关系、追踪角色成长时使用。触发词：角色、人物、角色卡、档案、言行一致、OOC检测、关系网、角色弧线。
---

# Novel Character — 角色档案管理

管理 `.novel/characters/` 下的角色档案，支持言行一致性检测、关系图谱与角色弧线追踪。

> **核心原则**：角色档案是 Source of Truth，AI 写作前必须读取，写作中必须约束角色言行。

## 工作区规范

```
.novel/
├── characters/
│   ├── {角色名}.md              # 人编辑（Source of Truth）
│   ├── {角色名}.html            # AI 消费（自动同步）
│   └── new/                     # 新增配角档案
│       └── {新角色名}.md
└── tracking/
│   ├── relationships.json       # 关系网数据
│   ├── character-arcs.json      # 角色弧线追踪
│   └── appearances.json         # 出场统计
```

## 角色档案 Markdown 规范

```markdown
---
name: {角色名}
type: {主角/女主/反派/配角/穿越者/原住民}
origin_era: "{原属时代，如适用}"
current_era: "{当前时代，如适用}"
cover_identity: {当前身份}
age: {年龄}

# 与世界 building 关联
faction: {所属势力}
race: {种族}
profession: {职业/身份}
status: {社会阶层}

# 知情边界
known_info:
  - {信息A}: {来源章节}
  - {信息B}: {来源章节}
unknown_info:
  - {信息C}: {预计获知章节}
  - {信息D}: {预计获知章节}

# 外貌
appearance:
  height: "{身高}"
  weight: "{体重}"
  build: "{体型}"
  face: "{面部特征}"
  features: "{显著特征}"

# 语言风格
speech_pattern: {角色通用语言风格}
speech_era: {时代用语风格，如适用}

# 性格标签（用于一致性检测）
personality_tags:
  - {标签1}
  - {标签2}
  - {标签3}

# 情绪状态（随剧情更新）
emotion_state:
  current: "{当前情绪}"
  baseline: "{基础情绪}"
  stress_level: 3  # 0-10，压力值

# 能力值（用于爽点设计，可选）
abilities:
  {能力1}: 9
  {能力2}: 8

# 风险规则（什么不能说/做）
risk_rules:
  - {规则1}
  - {规则2}

# 关系网
relationships:
  - target: {关系对象}
    type: {关系类型}
    stage: "{关系阶段}"
    desc: "{关系描述}"

# 成长弧线
growth_arc:
  - stage: "{阶段名称}"
    chapter_range: "{章节范围}"
    trait: "{阶段特征}"
    goal: "{阶段目标}"

# 标志性言行
signature_behaviors:
  - "{行为1}"
  - "{行为2}"

# 禁忌清单
forbidden_list:
  | 场景 | 禁止行为 | 后果 |
  |------|---------|------|
  | {场景1} | {禁止行为} | {后果} |
---

## 现代身份（如适用）

{角色在原属时代的身份、经历、能力}

## 当前身份

{角色在当前作品世界中的身份、处境}

## 性格核心

{性格分析}

## 角色弧线

### 阶段1：{阶段名}（ch{X}-ch{Y}）
- **起点**：{起点状态}
- **冲突**：{冲突}
- **成长**：{成长}
- **转折点**：ch{Z} {转折点}
```

## 核心操作

### 0. 写作前角色档案读取

AI 续写或修改正文前，必须完成以下步骤：
1. 扫描当前章节出场角色
2. 读取 `.novel/characters/{角色名}.md` 和 `.novel/characters/new/{角色名}.md`
3. 重点确认：
   - **身份/职业**：教授、军人、高管、学生等行为边界
   - **性格标签**：冷静、倔强、温和等
   - **dialect/籍贯**：方言、粗口是否符合籍贯
   - **关系阶段**：对其他角色的关系亲密度
   - **禁忌清单**：什么不能说/做
4. 未读取角色档案不得写该角色戏份
5. 若角色有 `faction` / `race` / `profession` 字段，必须同步读取 `.novel/worldbuilding/` 中对应档案
6. 必须读取角色的 `known_info` 和 `unknown_info`，约束其言行符合知情边界
7. 角色行为必须同时符合：职业身份、所属势力立场、种族/职业/阶层设定、知情边界

**职业决定行为规则**：
- 教授/教师：可看书、写论文、指导学生，不宜做与职业身份冲突的事
- 军人/干部：雷厉风行，不拖泥带水
- 学生：可谨慎、可冲动，但应符合具体人设
- 经纪人/高管：职业化、利益导向
- 任何与职业身份冲突的行为必须向作者确认

### 1. 创建/编辑角色卡

1. 用户在对话中提供角色信息
2. 按规范生成 Markdown 文件，保存到 `.novel/characters/{角色名}.md`
3. 触发双备份同步 → 生成同名 `.html`
4. 更新关系网数据 `.novel/tracking/relationships.json`

### 2. 角色列表管理

侧边栏/列表显示：
- 按类型分组（主角 / 女主 / 反派 / 配角 / 穿越者 / 原住民）
- 显示角色名、当前身份、出场次数、当前状态
- 支持搜索和筛选
- 角色标签云（性格标签、能力标签）

### 3. 言行一致性检测（OOC检测）

检测流程：
1. 扫描当前章节文本，提取角色对话和行为
2. 对比角色档案中的 `personality_tags`、`speech_era`、`risk_rules`
3. 检测时代错位（如角色使用了不属于当前时代的词汇）
4. 检测性格OOC（如冷静角色突然冲动无铺垫）
5. 生成警告列表

**OOC检测规则示例**：
```json
{
  "personality_rules": {
    "{角色名}": {
      "must": ["{必须行为}"],
      "must_not": ["{禁止行为}"],
      "only_when": {
        "{特定行为}": "{允许场景}"
      }
    }
  },
  "era_speech_rules": {
    "{时代}": {
      "forbidden_words": ["{禁用词}"],
      "forbidden_phrases": ["{禁用短语}"],
      "required_style": "{用语风格}"
    }
  }
}
```

### 4. 关系图谱

关系数据 `.novel/tracking/relationships.json`：
```json
{
  "nodes": [
    {"id": "{角色A}", "type": "{类型}", "group": "{分组}"},
    {"id": "{角色B}", "type": "{类型}", "group": "{分组}"}
  ],
  "links": [
    {"source": "{角色A}", "target": "{角色B}", "type": "{关系}", "stage": "{阶段}"}
  ]
}
```

**关系演变追踪**：
- 记录每对关系的关键转折点（章节、事件、变化）
- 预警：关系变化必须有铺垫，不能突兀
- 关系网可视化（文本描述形式）

### 5. 角色弧线追踪

`.novel/tracking/character-arcs.json`：
```json
{
  "arcs": [
    {
      "character": "{角色名}",
      "stages": [
        {
          "name": "{阶段名}",
          "chapter_range": "{章节范围}",
          "trait": "{特征}",
          "status": "completed"
        },
        {
          "name": "{阶段名}",
          "chapter_range": "{章节范围}",
          "trait": "{特征}",
          "status": "in_progress"
        }
      ],
      "current_stage": "{当前阶段}"
    }
  ]
}
```

**弧线检测**：
- 角色当前行为是否符合当前阶段特征
- 阶段转换是否有明确转折点
- 成长轨迹是否清晰、合理

### 6. 出场统计

`.novel/tracking/appearances.json`：
```json
{
  "statistics": {
    "{角色A}": {
      "total_chapters": 50,
      "last_chapter": 50,
      "chapters_since_last": 0
    },
    "{角色B}": {
      "total_chapters": 30,
      "last_chapter": 48,
      "chapters_since_last": 2
    }
  }
}
```

**预警规则**：
- 主角连续出场<3章：正常
- 女主连续3章未出场：预警（边缘化风险）
- 重要配角连续10章未出场：提醒

### 7. 上下文注入

AI 续写时，检索当前章节出场角色，读取对应档案，注入 Prompt：

```
[角色上下文]
出场角色：{角色A}（{类型}）
- 当前身份：{身份}
- 所属势力：{势力}（与主角关系：{关系}）
- 种族/职业/阶层：{race} / {profession} / {status}
- 当前状态：{状态}
- 语言风格：{风格}
- 性格标签：{标签}
- 当前弧线阶段：{阶段}
- 禁忌：{禁忌}
- 与{角色B}关系：{阶段}
- 与{角色C}关系：{阶段}

出场角色：{角色B}（{类型}）
- 当前身份：{身份}
- 所属势力：{势力}（与主角关系：{关系}）
- 种族/职业/阶层：{race} / {profession} / {status}
- 当前状态：{状态}
- 性格标签：{标签}
- 当前弧线阶段：{阶段}
- 标志性言行：{行为}
```

## 双备份同步

- Markdown 保存后，自动渲染为 HTML
- HTML 保留 YAML frontmatter 为 `<meta>` 标签
- 单向同步：Markdown → HTML
