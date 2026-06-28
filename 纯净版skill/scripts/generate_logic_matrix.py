#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
逻辑矩阵生成脚本

功能：
1. 扫描小说正文中的 HTML 注释 <!-- LOGIC: ... -->
2. 提取时间、地点、在场人物、信息状态
3. 生成本章或全书的逻辑矩阵 Markdown 文件

用法：
    python generate_logic_matrix.py chapters/vol1-开篇/ch05-示例.md
    python generate_logic_matrix.py chapters/ --output .novel/tracking/逻辑矩阵.md
"""

import re
import os
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional


# HTML 注释匹配规则
# <!-- LOGIC: time=09:15 | loc=公司会议室 | present=主角,李总 | info=主角知道B，李总不知道C -->
LOGIC_PATTERN = re.compile(
    r'<!--\s*LOGIC:\s*([^>]+?)\s*-->',
    re.MULTILINE | re.DOTALL
)


def parse_logic_annotation(raw: str) -> Dict[str, str]:
    """解析 LOGIC 注释内容，返回字段字典。"""
    fields = {}
    # 按 | 分隔，但保留中文内容
    parts = [p.strip() for p in raw.split('|')]
    for part in parts:
        if '=' in part:
            key, value = part.split('=', 1)
            fields[key.strip()] = value.strip()
    return fields


def extract_chapter_info(file_path: Path) -> Dict:
    """从文件路径和 frontmatter 提取章节信息。"""
    content = file_path.read_text(encoding='utf-8')
    
    # 简单解析 frontmatter
    title = file_path.stem
    chapter_num = ""
    match = re.match(r'ch(\d+)', file_path.stem)
    if match:
        chapter_num = match.group(1)
    
    # 尝试从 frontmatter 读取标题
    if content.startswith('---'):
        end = content.find('---', 3)
        if end != -1:
            fm = content[3:end]
            title_match = re.search(r'^title:\s*(.+)$', fm, re.MULTILINE)
            if title_match:
                title = title_match.group(1).strip()
    
    return {
        'file': str(file_path),
        'chapter': chapter_num,
        'title': title,
        'content': content
    }


def extract_logic_entries(chapter_info: Dict) -> List[Dict]:
    """从章节内容中提取所有 LOGIC 注释条目。"""
    entries = []
    content = chapter_info['content']
    
    for match in LOGIC_PATTERN.finditer(content):
        raw = match.group(1)
        fields = parse_logic_annotation(raw)
        
        # 获取注释后的第一句作为上下文，遇到下一个注释停止
        end_pos = match.end()
        next_comment = content.find('<!--', end_pos)
        if next_comment == -1:
            context_text = content[end_pos:]
        else:
            context_text = content[end_pos:next_comment]
        context = context_text.strip().replace('\n', ' ')
        if len(context) > 80:
            context = context[:80] + '...'
        context = context.replace('|', '｜')  # 避免破坏 Markdown 表格
        
        entry = {
            'chapter': chapter_info['chapter'],
            'title': chapter_info['title'],
            'time': fields.get('time', ''),
            'loc': fields.get('loc', ''),
            'present': fields.get('present', ''),
            'info': fields.get('info', ''),
            'pov': fields.get('pov', ''),
            'context': context
        }
        entries.append(entry)
    
    return entries


def time_to_minutes(time_str: str) -> Optional[int]:
    """将 HH:MM 格式转换为分钟数，用于排序。"""
    if not time_str:
        return None
    # 支持 "09:15" 或 "9:15"
    match = re.match(r'(\d{1,2}):(\d{2})', time_str)
    if match:
        h, m = int(match.group(1)), int(match.group(2))
        return h * 60 + m
    return None


def sort_entries(entries: List[Dict]) -> List[Dict]:
    """按章节号和时间排序条目。"""
    def sort_key(e):
        chapter = int(e['chapter']) if e['chapter'].isdigit() else 0
        minutes = time_to_minutes(e['time'])
        if minutes is None:
            minutes = 9999
        return (chapter, minutes)
    
    return sorted(entries, key=sort_key)


def generate_matrix_markdown(entries: List[Dict]) -> str:
    """生成逻辑矩阵 Markdown。"""
    lines = []
    lines.append(f"# 逻辑矩阵")
    lines.append("")
    lines.append(f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"> 条目数：{len(entries)}")
    lines.append("")
    
    if not entries:
        lines.append("暂未找到 LOGIC 注释。")
        return '\n'.join(lines)
    
    # 按章节分组
    current_chapter = None
    for entry in entries:
        if entry['chapter'] != current_chapter:
            current_chapter = entry['chapter']
            lines.append(f"## 第 {current_chapter} 章 {entry['title']}")
            lines.append("")
            lines.append("| 时间 | 地点 | 在场人物 | 信息状态 | 上下文 |")
            lines.append("|------|------|---------|---------|--------|")
        
        present = entry['present'] or '-'
        info = entry['info'] or '-'
        loc = entry['loc'] or '-'
        time = entry['time'] or '-'
        context = entry['context'] or '-'
        
        lines.append(f"| {time} | {loc} | {present} | {info} | {context} |")
    
    lines.append("")
    lines.append("## 检查摘要")
    lines.append("")
    
    # 简单统计
    locations = set(e['loc'] for e in entries if e['loc'])
    characters = set()
    for e in entries:
        if e['present']:
            for c in e['present'].split(','):
                characters.add(c.strip())
    
    lines.append(f"- 涉及地点：{len(locations)} 个")
    lines.append(f"- 涉及人物：{len(characters)} 位")
    lines.append(f"- 总条目：{len(entries)} 条")
    lines.append("")
    
    # 潜在问题提示
    issues = []
    prev_entry = None
    for entry in entries:
        # 检查同一时间不同地点
        if prev_entry and entry['time'] == prev_entry['time'] and entry['loc'] != prev_entry['loc']:
            # 可能是不同人物线，只作为提示
            pass
        
        # 检查缺少时间或地点
        if not entry['time'] or not entry['loc']:
            issues.append(f"第 {entry['chapter']} 章存在缺少时间或地点的条目")
        
        prev_entry = entry
    
    if issues:
        lines.append("### 待检查项")
        lines.append("")
        for issue in issues[:10]:  # 最多显示 10 条
            lines.append(f"- {issue}")
        lines.append("")
    
    return '\n'.join(lines)


def find_chapter_files(input_path: Path) -> List[Path]:
    """查找所有章节文件。"""
    files = []
    if input_path.is_file():
        files.append(input_path)
    elif input_path.is_dir():
        for md_file in sorted(input_path.rglob('*.md')):
            # 只处理正文章节文件，排除 skill 文档
            if 'ch' in md_file.stem and '纯净版skill' not in str(md_file):
                files.append(md_file)
    return files


def main():
    parser = argparse.ArgumentParser(
        description='根据正文 HTML 注释生成逻辑矩阵'
    )
    parser.add_argument(
        'input',
        help='输入文件或目录（如 chapters/vol1/ch05.md 或 chapters/）'
    )
    parser.add_argument(
        '-o', '--output',
        default='.novel/tracking/逻辑矩阵.md',
        help='输出文件路径（默认：.novel/tracking/逻辑矩阵.md）'
    )
    parser.add_argument(
        '--stdout',
        action='store_true',
        help='同时输出到控制台'
    )
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"错误：输入路径不存在：{input_path}", file=sys.stderr)
        sys.exit(1)
    
    files = find_chapter_files(input_path)
    if not files:
        print("未找到章节文件。", file=sys.stderr)
        sys.exit(1)
    
    all_entries = []
    for file_path in files:
        info = extract_chapter_info(file_path)
        entries = extract_logic_entries(info)
        all_entries.extend(entries)
        print(f"已处理：{file_path} ({len(entries)} 条注释)")
    
    sorted_entries = sort_entries(all_entries)
    markdown = generate_matrix_markdown(sorted_entries)
    
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding='utf-8')
    print(f"\n逻辑矩阵已生成：{output_path}")
    
    if args.stdout:
        print("\n--- 输出预览 ---")
        print(markdown[:1000])
        if len(markdown) > 1000:
            print("...")


if __name__ == '__main__':
    main()
