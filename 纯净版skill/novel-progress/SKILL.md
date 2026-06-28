---
name: novel-progress
description: 小说进度管理工具。管理章节树、字数统计、写作状态标记、进度追踪、钩子管理、写作日历。当用户需要查看/更新小说进度、统计字数、标记章节状态、生成写作报告、追踪伏笔回收时使用。触发词：进度、字数、章节状态、写作报告、统计、钩子、伏笔。
---

# Novel Progress — 小说进度管理

管理 `chapters/` 目录下的章节结构、字数统计、状态流转、钩子追踪与写作日历。

> **核心原则**：进度管理不仅是字数统计，更是伏笔、质量、节奏的可视化仪表盘。

## 工作区规范

```
chapters/
├── vol1-{卷名}/
│   ├── ch01-{标题}.md
│   └── ch02-{标题}.md
├── vol2-{卷名}/
│   └── ...
.novel/
├── progress/
│   ├── progress.json       # 进度数据
│   └── calendar.json       # 写作日历
└── tracking/
│   ├── hooks.json          # 钩子/伏笔追踪
│   ├── arcs.json           # 故事弧线追踪
│   └── 修改记录.md
└── config.yaml             # 全局配置
```

## 文件命名规范

- 卷文件夹：`vol{N}-{卷名}/`（如 `vol1-开篇/`）
- 章节文件：`ch{NN}-{标题}.md`（如 `ch01-开局.md`）
- 卷名和章节标题使用中文

## 核心操作

### 1. 扫描章节树

扫描 `chapters/` 目录，构建卷→章的树形结构：
1. 按文件夹分组（卷）
2. 每卷内按文件名排序（ch01, ch02...）
3. 读取每章 frontmatter 和字数

### 2. 字数统计

- **中文字符数**：统计汉字、\u4e00-\u9fff 范围内的字符
- **总字数**：所有章节中文字符累加
- **卷字数**：单卷内所有章节累加
- **今日字数**：对比 `progress.json` 中上次记录的字数差

**字数同步规则**：
1. 每次修改正文后，若字数变化超过 10 字，必须同步更新：
   - 章节文件 front matter 中的 `word_count`
   - `.novel/progress/progress.json` 中对应章节的 `word_count`
   - `.novel/progress/progress.json` 中的 `total_words`
   - `last_modified` 时间戳
2. humanizer/review 报告中的字数也必须同步更新
3. 禁止 front matter、progress.json、报告三者字数不一致
4. **例外**：单次修改字数变化低于 500 字的小改动，可跳过字数元数据同步，也不重新生成质检报告；但涉及关键设定、人物关系转折、时间线或专业细节的改动除外

### 3. 章节状态流转

状态定义（存储在 `progress.json`）：
- `pending` — 未写（灰色）
- `draft` — 草稿（黄色）
- `polishing` — 精修（蓝色）
- `final` — 定稿（绿色）

状态操作命令：
- `novel: mark-draft <file>` — 标记为草稿
- `novel: mark-polishing <file>` — 标记为精修
- `novel: mark-final <file>` — 标记为定稿

**修改后的状态规则**：
- 章节状态为 `final` 时，修改后原则上自动降级为 `polishing`
- 修改模式下不自动触发完整质检，因此状态只降级，不重新评分
- 用户要求质检并达到标准后，可手动重新标记为 `final`
- 小改动（<500字）且未涉及关键设定时，可保持原状态不变，但必须在 修改记录.md 中记录
- 涉及关键设定、人物关系转折、时间线、专业细节的修改：无论字数多少都必须降级

**用户直接修改正文处理规则**：
1. 当用户说"我又调整了一下""我改了一下"时，先读取当前正文，确认用户版本
2. 不要擅自修改正文，只同步元数据（切片、progress、tracking）
3. 在 `.novel/tracking/修改记录.md` 中标注："用户直接修改正文，AI 同步切片与 tracking"
4. 若用户明确要求 AI 参与修正，方可动正文
5. 若用户单次修改低于 500 字且未要求质检，仅记录修改事实，不做汇总、不跑质检、不同步字数元数据

### 4. 进度数据格式

`.novel/progress/progress.json`：
```json
{
  "daily_target": 6000,
  "total_target": 3000000,
  "anchor_date": "{锚点日期}",
  "current_chapter": 3,
  "current_volume": 1,
  "volumes": [
    {
      "id": "vol1",
      "title": "{卷名}",
      "period": "{故事时间范围}",
      "arc": "{卷弧线}",
      "chapters": [
        {
          "file": "ch01-{标题}.md",
          "title": "{标题}",
          "status": "final",
          "word_count": 6000,
          "story_date": "{日期}",
          "last_modified": "2026-06-01T10:00:00Z",
          "quality_score": 85
        }
      ]
    }
  ],
  "writing_log": [
    {"date": "2026-06-01", "words_added": 6000, "chapter": 1, "quality_score": 85}
  ]
}
```

### 5. 钩子/伏笔追踪

`.novel/tracking/hooks.json`：
```json
{
  "hooks": [
    {
      "id": "hook-001",
      "type": "悬念钩子",
      "description": "{钩子描述}",
      "chapter_set": 1,
      "chapter_payoff": 5,
      "status": "pending",
      "priority": "high"
    },
    {
      "id": "hook-002",
      "type": "危机钩子",
      "description": "{钩子描述}",
      "chapter_set": 3,
      "chapter_payoff": null,
      "status": "active",
      "priority": "high"
    }
  ],
  "stats": {
    "total_hooks": 2,
    "active_hooks": 1,
    "resolved_hooks": 0,
    "overdue_hooks": 0
  }
}
```

**钩子类型**：
| 类型 | 说明 | 示例 |
|------|------|------|
| 悬念钩子 | 制造未解之谜 | "他打开门，看到的却是——" |
| 危机钩子 | 突发的危机 | 电话响起，传来噩耗 |
| 揭秘钩子 | 揭露重要信息 | "其实，我早就知道你是穿越者" |
| 期待钩子 | 铺垫即将发生的好事 | 明天就是决赛，他准备好了 |
| 情感钩子 | 关系转折 | 她看着他，眼中第一次有了异样的光芒 |
| 选择钩子 | 两难抉择 | 事业还是爱情，他必须选一个 |
| 伏笔钩子 | 为后文铺垫 | 看似无关的细节，后期成为关键 |

**钩子管理规则**：
- 每章至少1个钩子
- 每个钩子必须在10章内回收（长篇可放宽至20章）
- 超过20章未回收的钩子标记为`overdue`，触发预警
- 回收时必须达到读者预期，不能烂尾

### 6. 修改模式与字数同步

**修改模式下**：
- 字数变化 > 10 字：同步 `word_count` 和 `progress.json`（建议执行）
- 字数变化 < 500 字且未涉及关键设定：可跳过字数元数据同步
- 涉及关键设定、人物关系转折、时间线、专业细节的修改：无论字数多少都要完整同步

**修改记录**：
- 任何修改都应在 `.novel/tracking/修改记录.md` 中记录
- 记录内容：修改时间、范围、原因、影响评估、是否同步元数据

### 7. 写作日历

`.novel/progress/calendar.json`：
```json
{
  "entries": [
    {
      "date": "2026-06-01",
      "chapter": 1,
      "words_written": 6000,
      "time_spent_minutes": 120,
      "quality_score": 85,
      "mood": "顺畅",
      "notes": "开篇顺利，钩子设置成功"
    }
  ],
  "stats": {
    "total_days": 1,
    "total_words": 6000,
    "avg_daily": 6000,
    "best_day": "2026-06-01",
    "best_words": 6000,
    "current_streak": 1,
    "longest_streak": 1
  }
}
```

**写作日历规则**：
- 目标日更{目标字数}字，最低{最低字数}字
- 连续断更>3天触发预警
- 单章质量<70分触发修改流程
- 记录心情和notes，回顾写作状态

### 7. 生成写作报告

报告内容：
- 当前总字数 / 目标字数 / 完成百分比
- 各卷字数分布
- 今日/本周/本月字数趋势
- 章节状态统计（未写/草稿/精修/定稿 各多少章）
- 按当前速度预计完本日期
- **钩子状态统计**（活跃/已回收/逾期）
- **质量趋势**（最近10章评分变化）

## 状态栏显示

建议格式：
```
今日 {X}/{目标} 字 | 第 {N} 章 | 故事时间：{日期} | 活跃钩子：{N} | 质量：{分数}
```

## 与 novel-review skill 的配合

1. 每章写完后，novel-review给出质量评分
2. 评分写入progress.json的quality_score
3. 质量<70分触发修改流程
4. 修改完成后重新评分，直到达标
