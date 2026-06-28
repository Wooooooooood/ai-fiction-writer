# AI 小说创作助手 · 十大 Skill 体系

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> 一套面向长篇网络小说的「人机协作」创作系统。  
> 把小说创作从「一次性生成」变成**可管理、可追溯、可质检**的工程流程。

---

## 简介

`ai-fiction-writer` 是一套**本地化、模块化、Skill 化**的 AI 小说创作工作流。核心目标不是让 AI 替你把整章写出来，而是让 AI 帮你管理素材、执行规范、检查质量；**创意和决策权始终掌握在作者手里**。

这套体系将创作全流程拆解为 **10 个独立 Skill**，覆盖从市场拆书到章节定稿、从角色管理到世界构建、从逻辑预防到去 AI 味质检的完整链路。

---

## 十大 Skill

| Skill | 名称 | 解决什么问题 | 关键输出 |
|-------|------|------------|---------|
| `novel-analyze` | 扫榜与拆文 | 不知道写什么、不会设计爽点 | 市场趋势报告、对标书拆文、模块库 |
| `novel-outline` | 大纲编排 | 结构松散、节奏失控 | 卷章大纲、细纲、爽点与钩子规划 |
| `novel-character` | 角色档案 | 角色 OOC、关系混乱 | 角色卡、关系图谱、角色弧线 |
| `novel-knowledge` | 知识库管理 | 时代背景错漏、物价/品牌穿帮 | 时间线、物价表、品牌对照、参考文献 |
| `novel-worldbuilding` | 世界构建 | 世界观崩坏、地图矛盾、设定吃书 | 世界总览、动态迷雾地图、历法、势力、规则体系 |
| `novel-logic` | 逻辑预防 | 前后文不一致、细节逻辑漏洞 | 微逻辑卡、动作前四问、知情边界、逻辑矩阵、冻结状态 |
| `novel-progress` | 进度管理 | 写到哪忘了、伏笔丢了 | 章节树、字数统计、状态流转、写作日历 |
| `novel-writing` | 写作核心 | AI 写出来的东西和前文不接 | 上下文注入模板、段落级硬阻塞、修改模式 |
| `novel-humanizer` | 去 AI 味质检 | 文字机械、情感直给、时代错位 | 9 维度评分报告、质量趋势追踪 |
| `novel-review` | 多视角审稿 | 不知道改哪里、找不到毒点 | 编辑/读者/平台/作者四维审稿报告 |

---

## 快速开始

1. 克隆本仓库到本地：
   ```bash
   git clone https://github.com/Wooooooooood/ai-fiction-writer.git
   cd ai-fiction-writer
   ```

2. 阅读顶层文档了解整体架构：
   - `纯净版skill/PRD.md` —— 产品需求与架构设计
   - `纯净版skill/写作工作流.md` —— 完整工作流与命令清单

3. 按需查阅对应 Skill：
   - `纯净版skill/novel-writing/SKILL.md`
   - `纯净版skill/novel-logic/SKILL.md`
   - `纯净版skill/novel-worldbuilding/SKILL.md`
   - ……

4. 运行辅助脚本（可选）：
   ```bash
   python3 纯净版skill/scripts/generate_logic_matrix.py --help
   python3 纯净版skill/scripts/generate_map.py --help
   ```

---

## 核心原则

1. **零服务端**：所有创作数据以本地文件形式存在，100% 可 Git 追踪。
2. **文件即数据**：Markdown 供人编辑，HTML/JSON 供 AI 消费，双备份自动同步。
3. **Skill 化拆解**：每个 Skill 独立、可组合、可按需调用。
4. **人主导 + AI 辅助**：AI 负责执行、检查、建议；作者保留最终决策权。
5. **修改模式优先**：小改动（<500 字）可跳过完整流程，避免消耗过多 token。

---

## 项目结构

```
ai-fiction-writer/
├── README.md
├── LICENSE
├── .gitignore
└── 纯净版skill/
    ├── PRD.md                    # 产品架构与需求
    ├── 写作工作流.md              # 完整工作流
    ├── novel-analyze/
    ├── novel-character/
    ├── novel-knowledge/
    ├── novel-outline/
    ├── novel-worldbuilding/
    ├── novel-logic/
    ├── novel-progress/
    ├── novel-writing/
    ├── novel-humanizer/
    ├── novel-review/
    └── scripts/                  # 辅助脚本
        ├── generate_logic_matrix.py
        ├── generate_map.py
        └── test_data/
```

---

## 适用题材

本版本为**通用抽象版**，已去掉任何具体作品、角色、时代、世界观内容。可通过配置适配：

- 都市穿越 / 年代重生
- 玄幻 / 仙侠 / 奇幻
- 科幻 / 末世
- 言情 / 悬疑 / 历史

---

## 贡献

欢迎提交 Issue 与 PR。  
在扩展新 Skill 时，请先阅读 `novel-writing/SKILL.md` 中关于上下文注入与修改模式的规范，确保新 Skill 能与现有体系协同。

---

## 许可证

MIT © Wooooooooood
