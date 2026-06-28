# 辅助脚本

本目录提供小说创作工作流的辅助脚本。

---

## 1. generate_logic_matrix.py

**功能**：扫描正文中的 `<!-- LOGIC: ... -->` 注释，自动生成逻辑矩阵。

### 用法

```bash
# 处理单章
python generate_logic_matrix.py chapters/vol1-开篇/ch05-示例.md

# 批量处理整个 chapters 目录
python generate_logic_matrix.py chapters/ -o .novel/tracking/逻辑矩阵.md

# 同时输出到控制台
python generate_logic_matrix.py chapters/ -o .novel/tracking/逻辑矩阵.md --stdout
```

### 输入格式

在正文初稿的每个段落前添加 HTML 注释：

```markdown
<!-- LOGIC: time=09:15 | loc=公司会议室 | present=主角,李总 | info=主角知道B，李总不知道C -->

主角推门进来，李总已经在会议室坐了十分钟。
```

### 输出格式

生成 `.novel/tracking/逻辑矩阵.md`：

```markdown
# 逻辑矩阵

## 第 5 章 ch05-示例

| 时间 | 地点 | 在场人物 | 信息状态 | 上下文 |
|------|------|---------|---------|--------|
| 09:15 | 公司会议室 | 主角,李总 | 主角知道B，李总不知道C | 主角推门进来，李总已经在会议室坐了十分钟。... |
```

---

## 2. generate_map.py

**功能**：读取 `worldbuilding/map/*.json` 坐标数据，生成 SVG 静态地图和 HTML 交互地图。

### 用法

```bash
# 生成世界地图
python generate_map.py .novel/worldbuilding/map/world-map.json -o .novel/worldbuilding/map/

# 生成城市地图
python generate_map.py .novel/worldbuilding/map/cities/东海城.json -o .novel/worldbuilding/map/cities/ -w 600 -ht 400

# 只生成 SVG，不生成 HTML
python generate_map.py .novel/worldbuilding/map/world-map.json -o .novel/worldbuilding/map/ --no-html
```

### 输入 JSON 格式

```json
{
  "name": "东海城",
  "level": "L2",
  "coordinates": {"relative_to": "东大陆", "x": 0.7, "y": 0.3},
  "districts": {
    "上城区": {"level": "L3", "unlocked_by": "ch03", "coordinates": {"x": 0.3, "y": 0.2}},
    "下城区": {"level": "L3", "unlocked_by": "ch05", "coordinates": {"x": 0.7, "y": 0.6}}
  },
  "connections": [
    {"to": "青云镇", "method": "马车", "time": "6h"}
  ],
  "fog_of_war": ["北郊矿山", "西海岸线"]
}
```

### 输出文件

- `{map-name}.svg`：静态 SVG 地图
- `{map-name}.html`：可点击交互的 HTML 地图

---

## 依赖

两个脚本均只依赖 Python 标准库，无需安装第三方包。

---

## 集成到工作流

### novel-writing 流程

1. **写作模式 - 每章写完后**：调用 `generate_logic_matrix.py` 生成本章逻辑矩阵
2. **修改模式 - 涉及时间/地点/人物/信息变化后**：调用 `generate_logic_matrix.py` 更新逻辑矩阵
3. **定稿前**：确认 HTML 注释已清理，避免注释进入最终正文

### novel-worldbuilding 流程

1. **动态地图解锁后**：作者确认 `map-update-suggestion.md`，写入 `.md` + `.json`
2. **立即调用** `generate_map.py` 重新生成 `.svg` + `.html`
3. **设定变更涉及地理/地点后**：重新生成受影响层级的地图

### novel-logic 流程

1. **章末**：调用 `generate_logic_matrix.py` 生成本章逻辑矩阵
2. **修改模式**：涉及逻辑信息变化时更新逻辑矩阵
3. **初始化冻结状态前**：确认逻辑矩阵已是最新

### 修改模式注意事项

- 用户说"改"时，**只执行最小化修改**，不重新跑完整写作流程
- 修改涉及字数变化 > 10 字时，同步 `word_count` / `progress.json`
- 修改涉及逻辑信息变化时，调用 `generate_logic_matrix.py`
- 小改动（<500字）且未涉及关键设定时，可跳过脚本调用
- 修改后状态从 `final` 自动降为 `polishing`，不自动触发完整质检
