#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SVG/HTML 地图生成脚本

功能：
1. 读取 worldbuilding/map/*.json 坐标数据
2. 生成 SVG 静态地图
3. 生成 HTML 交互式地图

用法：
    python generate_map.py .novel/worldbuilding/map/world-map.json
    python generate_map.py .novel/worldbuilding/map/cities/东海城.json --level L2
"""

import json
import os
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional


class MapGenerator:
    """地图生成器"""
    
    def __init__(self, map_data: Dict, width: int = 800, height: int = 600):
        self.data = map_data
        self.width = width
        self.height = height
        self.name = map_data.get('name', '未命名地图')
        self.level = map_data.get('level', 'L0')
        
    def _coord_to_px(self, x: float, y: float) -> Tuple[int, int]:
        """将相对坐标 (0-1) 转换为像素坐标。"""
        px = int(x * self.width)
        py = int(y * self.height)
        return px, py
    
    def _get_level_color(self, level: str, is_fog: bool = False) -> str:
        """根据层级和迷雾状态返回颜色。"""
        if is_fog:
            return '#cccccc'
        colors = {
            'L0': '#4a90e2',
            'L1': '#50c878',
            'L2': '#f5a623',
            'L3': '#d0021b',
            'L4': '#9013fe'
        }
        return colors.get(level, '#4a90e2')
    
    def _get_level_label(self, level: str) -> str:
        """层级中文标签。"""
        labels = {
            'L0': '世界',
            'L1': '区域',
            'L2': '城市',
            'L3': '场景',
            'L4': '细节'
        }
        return labels.get(level, level)
    
    def generate_svg(self) -> str:
        """生成 SVG 字符串。"""
        svg_parts = []
        svg_parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" viewBox="0 0 {self.width} {self.height}">')
        
        # 背景
        svg_parts.append(f'<rect width="{self.width}" height="{self.height}" fill="#f8f9fa"/>')
        
        # 标题
        svg_parts.append(f'<text x="20" y="30" font-family="sans-serif" font-size="18" font-weight="bold" fill="#333">{self.name} ({self._get_level_label(self.level)})</text>')
        
        # 连接线路径
        connections = self.data.get('connections', [])
        for conn in connections:
            target = conn.get('to', '')
            # 找到目标节点的坐标
            target_node = self._find_node(target)
            if target_node:
                x1, y1 = self._get_center_coord()
                x2, y2 = self._coord_to_px(target_node['x'], target_node['y'])
                svg_parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#999" stroke-width="2" stroke-dasharray="5,3"/>')
                # 交通信息
                mid_x, mid_y = (x1 + x2) // 2, (y1 + y2) // 2
                method = conn.get('method', '')
                time = conn.get('time', '')
                label = f"{method} {time}".strip()
                if label:
                    svg_parts.append(f'<text x="{mid_x}" y="{mid_y - 5}" font-family="sans-serif" font-size="10" fill="#666" text-anchor="middle">{label}</text>')
        
        # 子节点（区域/城市/场景）
        nodes = self._get_nodes()
        for node in nodes:
            name = node.get('name', '')
            level = node.get('level', self.level)
            x, y = self._coord_to_px(node['x'], node['y'])
            is_fog = name in self.data.get('fog_of_war', [])
            color = self._get_level_color(level, is_fog)
            radius = 25 if level == 'L1' else 18 if level == 'L2' else 12
            
            # 节点圆圈
            svg_parts.append(f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{color}" stroke="#333" stroke-width="2" opacity="{0.5 if is_fog else 1.0}"/>')
            
            # 节点名称
            svg_parts.append(f'<text x="{x}" y="{y + radius + 15}" font-family="sans-serif" font-size="12" fill="#333" text-anchor="middle">{name}</text>')
            
            # 层级标签
            if not is_fog:
                svg_parts.append(f'<text x="{x}" y="{y + 4}" font-family="sans-serif" font-size="9" fill="white" text-anchor="middle">{level}</text>')
        
        # 迷雾区域提示
        fog_areas = self.data.get('fog_of_war', [])
        if fog_areas:
            fog_text = '迷雾区域：' + '、'.join(fog_areas)
            svg_parts.append(f'<text x="20" y="{self.height - 20}" font-family="sans-serif" font-size="12" fill="#999">{fog_text}</text>')
        
        # 图例
        legend_y = 60
        svg_parts.append(f'<text x="{self.width - 150}" y="{legend_y}" font-family="sans-serif" font-size="12" font-weight="bold" fill="#333">图例</text>')
        for i, (level, color) in enumerate([
            ('L0', '#4a90e2'), ('L1', '#50c878'), ('L2', '#f5a623'),
            ('L3', '#d0021b'), ('L4', '#9013fe'), ('迷雾', '#cccccc')
        ]):
            y = legend_y + 25 + i * 20
            svg_parts.append(f'<circle cx="{self.width - 140}" cy="{y - 4}" r="6" fill="{color}"/>')
            svg_parts.append(f'<text x="{self.width - 125}" y="{y}" font-family="sans-serif" font-size="11" fill="#333">{self._get_level_label(level)}</text>')
        
        svg_parts.append('</svg>')
        return '\n'.join(svg_parts)
    
    def _find_node(self, name: str) -> Optional[Dict]:
        """根据名称查找节点。"""
        nodes = self._get_nodes()
        for node in nodes:
            if node.get('name') == name:
                return node
        return None
    
    def _get_nodes(self) -> List[Dict]:
        """获取所有子节点。"""
        nodes = []
        
        # L0: regions
        if 'regions' in self.data:
            for region in self.data['regions']:
                nodes.append({
                    'name': region.get('name', ''),
                    'level': region.get('level', 'L1'),
                    'x': region.get('coordinates', {}).get('x', 0.5),
                    'y': region.get('coordinates', {}).get('y', 0.5)
                })
        
        # L1/L2: districts
        if 'districts' in self.data:
            for name, info in self.data['districts'].items():
                coords = info.get('coordinates', {})
                nodes.append({
                    'name': name,
                    'level': info.get('level', 'L3'),
                    'x': coords.get('x', 0.5),
                    'y': coords.get('y', 0.5)
                })
        
        return nodes
    
    def _get_center_coord(self) -> Tuple[int, int]:
        """获取当前地图中心点（用于绘制连接线起点）。"""
        return self.width // 2, self.height // 2
    
    def generate_html(self, svg_content: str) -> str:
        """生成 HTML 交互页面。"""
        nodes_json = json.dumps(self._get_nodes(), ensure_ascii=False)
        connections_json = json.dumps(self.data.get('connections', []), ensure_ascii=False)
        fog_json = json.dumps(self.data.get('fog_of_war', []), ensure_ascii=False)
        
        html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.name} - 交互地图</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1000px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        h1 {{ margin-top: 0; color: #333; }}
        .meta {{ color: #666; margin-bottom: 20px; }}
        #map {{ border: 1px solid #ddd; border-radius: 4px; }}
        #info {{ margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 4px; min-height: 60px; }}
        #info h3 {{ margin-top: 0; }}
        .legend {{ margin-top: 15px; display: flex; gap: 15px; flex-wrap: wrap; }}
        .legend-item {{ display: flex; align-items: center; gap: 5px; font-size: 12px; }}
        .legend-color {{ width: 12px; height: 12px; border-radius: 50%; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{self.name}</h1>
        <div class="meta">层级：{self._get_level_label(self.level)} | 生成时间：自动生成</div>
        
        <div id="map">{svg_content}</div>
        
        <div id="info">
            <h3>地点详情</h3>
            <p>点击地图上的节点查看详情。</p>
        </div>
        
        <div class="legend">
            <div class="legend-item"><div class="legend-color" style="background:#4a90e2"></div>世界</div>
            <div class="legend-item"><div class="legend-color" style="background:#50c878"></div>区域</div>
            <div class="legend-item"><div class="legend-color" style="background:#f5a623"></div>城市</div>
            <div class="legend-item"><div class="legend-color" style="background:#d0021b"></div>场景</div>
            <div class="legend-item"><div class="legend-color" style="background:#9013fe"></div>细节</div>
            <div class="legend-item"><div class="legend-color" style="background:#cccccc"></div>迷雾</div>
        </div>
    </div>
    
    <script>
        const nodes = {nodes_json};
        const connections = {connections_json};
        const fogAreas = {fog_json};
        
        document.querySelectorAll('circle').forEach(circle => {{
            circle.style.cursor = 'pointer';
            circle.addEventListener('click', function() {{
                const text = this.nextElementSibling;
                const name = text ? text.textContent : '未知';
                const node = nodes.find(n => n.name === name);
                const isFog = fogAreas.includes(name);
                
                let html = '<h3>' + name + '</h3>';
                if (node) {{
                    html += '<p>层级：' + node.level + '</p>';
                }}
                html += '<p>状态：' + (isFog ? '迷雾（未解锁）' : '已解锁') + '</p>';
                
                // 查找连接
                const conn = connections.find(c => c.to === name);
                if (conn) {{
                    html += '<p>交通：' + (conn.method || '') + ' ' + (conn.time || '') + '</p>';
                }}
                
                document.getElementById('info').innerHTML = html;
            }});
        }});
    </script>
</body>
</html>'''
        return html


def load_map_data(json_path: Path) -> Dict:
    """加载 JSON 地图数据。"""
    return json.loads(json_path.read_text(encoding='utf-8'))


def main():
    parser = argparse.ArgumentParser(
        description='根据 JSON 坐标生成 SVG/HTML 地图'
    )
    parser.add_argument(
        'input',
        help='输入 JSON 文件路径'
    )
    parser.add_argument(
        '-o', '--output-dir',
        default='.',
        help='输出目录（默认：当前目录）'
    )
    parser.add_argument(
        '-w', '--width',
        type=int,
        default=800,
        help='SVG 宽度（默认：800）'
    )
    parser.add_argument(
        '-ht', '--height',
        type=int,
        default=600,
        help='SVG 高度（默认：600）'
    )
    parser.add_argument(
        '--no-html',
        action='store_true',
        help='不生成 HTML 文件'
    )
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"错误：输入文件不存在：{input_path}", file=sys.stderr)
        sys.exit(1)
    
    map_data = load_map_data(input_path)
    generator = MapGenerator(map_data, width=args.width, height=args.height)
    
    svg_content = generator.generate_svg()
    
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    base_name = input_path.stem
    svg_path = output_dir / f"{base_name}.svg"
    svg_path.write_text(svg_content, encoding='utf-8')
    print(f"SVG 地图已生成：{svg_path}")
    
    if not args.no_html:
        html_content = generator.generate_html(svg_content)
        html_path = output_dir / f"{base_name}.html"
        html_path.write_text(html_content, encoding='utf-8')
        print(f"HTML 交互地图已生成：{html_path}")


if __name__ == '__main__':
    main()
