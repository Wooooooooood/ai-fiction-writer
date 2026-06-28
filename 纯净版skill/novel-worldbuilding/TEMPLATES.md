# Worldbuilding 初始化模板

提供三套通用模板，项目初始化时根据题材选择。

---

## 模板一：都市穿越

适用题材：都市重生、年代文、商战、职场穿越

### 目录结构

```
worldbuilding/
├── world.md
├── map/
│   ├── world-map.md              # 城市总体布局
│   ├── world-map.json
│   ├── world-map.svg
│   ├── world-map.html
│   ├── regions/
│   │   └── {城区名}.md            # 老城区/开发区/商务区等
│   ├── cities/
│   │   └── {城市名}.md            # 若涉及多个城市
│   └── scenes/
│       ├── {街道/小区}.md
│       ├── {单位/公司}.md
│       └── {学校/工厂}.md
├── timeline/
│   ├── calendar.md               # 公历/农历，关键年代节点
│   └── eras.md                   # 时代阶段（如改革开放、互联网泡沫）
├── factions/
│   ├── {家族}.md
│   ├── {公司}.md
│   ├── {单位/体制}.md
│   └── relations.md
├── identities/
│   ├── professions.md            # 职业体系：干部、工人、个体户、知识分子
│   └── statuses.md               # 社会阶层
├── systems/
│   ├── technology.md             # 通讯、交通、家电水平
│   ├── economy.md                # 物价、工资、货币
│   └── laws.md                   # 时代政策、法律限制
└── culture/
    ├── customs.md                # 年代风俗
    ├── taboos.md                 # 政治/社会红线
    └── languages.md              # 方言、年代流行语
```

### 核心关注点

- **真实地理 + 时代细节**：城市街区、公交线路、地标建筑
- **社会势力**：单位、家族、官场、商圈关系
- **时代限制**：通讯方式、交通工具、政策壁垒
- **物价锚点**：与 `novel-knowledge` 联动

---

## 模板二：玄幻修真

适用题材：玄幻、修仙、武侠、东方奇幻

### 目录结构

```
worldbuilding/
├── world.md
├── map/
│   ├── world-map.md              # 大陆分布
│   ├── world-map.json
│   ├── world-map.svg
│   ├── world-map.html
│   ├── regions/
│   │   └── {州/域}.md
│   ├── cities/
│   │   └── {城池}.md
│   └── scenes/
│       ├── {宗门}.md
│       ├── {秘境}.md
│       └── {洞府}.md
├── timeline/
│   ├── calendar.md               # 修真历、纪元
│   └── eras.md                   # 上古/中古/近古/当世
├── factions/
│   ├── {宗门}.md
│   ├── {王朝}.md
│   ├── {魔道}.md
│   └── relations.md
├── identities/
│   ├── races.md                  # 人族、妖族、魔族、灵族
│   ├── professions.md            # 剑修、丹修、符修、阵修
│   └── statuses.md               # 凡人、修士、大能、老祖
├── systems/
│   ├── magic.md                  # 修炼体系、境界、灵根
│   ├── technology.md             # 炼器、阵法、傀儡
│   ├── economy.md                # 灵石、丹药、法宝市场
│   └── laws.md                   # 天道规则、宗门戒律
└── culture/
    ├── customs.md                # 宗门礼仪、收徒大典
│   ├── taboos.md                 # 夺舍、屠城、叛师
│   └── languages.md              # 上古语、妖语
```

### 核心关注点

- **修炼体系清晰**：境界划分、突破条件、能力边界
- **地图层次分明**：大陆 → 州域 → 城池 → 宗门 → 秘境
- **势力恩怨复杂**：宗门、王朝、魔道、散修关系网
- **资源分布**：灵石矿、药园、秘境位置

---

## 模板三：科幻星际

适用题材：科幻、星际、赛博朋克、末日

### 目录结构

```
worldbuilding/
├── world.md
├── map/
│   ├── world-map.md              # 星域/星系分布
│   ├── world-map.json
│   ├── world-map.svg
│   ├── world-map.html
│   ├── regions/
│   │   └── {星域}.md
│   ├── cities/
│   │   └── {星球/空间站}.md
│   └── scenes/
│       ├── {飞船}.md
│       ├── {城市}.md
│       └── {遗迹}.md
├── timeline/
│   ├── calendar.md               # 星历、标准时
│   └── eras.md                   # 旧地球/大航海/星际联盟
├── factions/
│   ├── {星际联盟}.md
│   ├── {企业}.md
│   ├── {反抗军}.md
│   └── relations.md
├── identities/
│   ├── races.md                  # 人类、改造人、外星人、AI
│   ├── professions.md            # 舰长、工程师、佣兵、科学家
│   └── statuses.md               # 公民、殖民者、流亡者
├── systems/
│   ├── magic.md                  # 超能力/灵能/异能
│   ├── technology.md             # 跃迁、AI、义体、武器
│   ├── economy.md                # 信用点、资源星、黑市
│   └── laws.md                   # 星际法、AI 三定律、物理上限
└── culture/
    ├── customs.md                # 太空礼仪、舰队传统
│   ├── taboos.md                 # AI 觉醒、基因改造、殖民屠杀
│   └── languages.md              # 通用语、外星语、黑话
```

### 核心关注点

- **科技树完整**：哪些技术存在、哪些不存在、限制是什么
- **星际距离合理**：跃迁时间、通讯延迟
- **势力博弈**：国家、企业、宗教、AI、外星文明
- **资源与生态**：宜居星、资源星、生态改造

---

## 模板使用方式

初始化时：

```
用户：初始化一个都市穿越世界观
→ 复制对应模板到 .novel/worldbuilding/
→ 引导用户填写关键字段
→ 生成初始 world-map.svg 和 world-map.html
```

模板中的 `{占位符}` 需要替换为具体作品设定。
