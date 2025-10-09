#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动更新GitHub个人主页README
- 获取所有仓库（公开+私有）
- 使用Topics第一个标签作为分类
- 私有仓库添加🔒标记
"""

import os
import re
import requests
from collections import defaultdict
from datetime import datetime

# GitHub API配置
GITHUB_TOKEN = os.environ.get('GH_TOKEN')
GITHUB_USERNAME = 'FB208'
API_BASE = 'https://api.github.com'

# Topic对应的Emoji和中文名称映射
TOPIC_CONFIG = {
    'fork': {'emoji': '📦', 'name': 'Fork'},
    'deprecated': {'emoji': '🙈', 'name': '弃用存档'},
    'services': {'emoji': '☁️', 'name': '服务'},
    'ai': {'emoji': '🤖', 'name': '人工智能'},
    'obsidian': {'emoji': '📝', 'name': 'Obsidian'},
    'tool': {'emoji': '🛠️', 'name': '工具'},
    'browser-extension': {'emoji': '🌐', 'name': '浏览器扩展'},
    'education': {'emoji': '📚', 'name': '教育'},
    
    'blog': {'emoji': '📰', 'name': '博客'},
    'python': {'emoji': '🐍', 'name': 'Python'},
    'javascript': {'emoji': '💛', 'name': 'JavaScript'},
    'csharp': {'emoji': '💚', 'name': 'C#'},
    'game': {'emoji': '🎮', 'name': '游戏'},
    'security': {'emoji': '🔓', 'name': '安全研究'},
    'productivity': {'emoji': '⚡', 'name': '生产力'},
    'backup': {'emoji': '💾', 'name': '备份'},
    'network': {'emoji': '🌐', 'name': '网络'},
    'proxy': {'emoji': '🔄', 'name': '代理'},
    'desktop': {'emoji': '🖥️', 'name': '桌面应用'},
    'powershell': {'emoji': '💙', 'name': 'PowerShell'},
    'vue': {'emoji': '💚', 'name': 'Vue.js'},
    'rust': {'emoji': '🦀', 'name': 'Rust'},
    'go': {'emoji': '🐹', 'name': 'Go'},
    'web': {'emoji': '🌍', 'name': 'Web'},
    'cli': {'emoji': '⌨️', 'name': '命令行工具'},
    'api': {'emoji': '🔌', 'name': 'API'},
    'database': {'emoji': '🗄️', 'name': '数据库'},
    'docker': {'emoji': '🐳', 'name': 'Docker'},
    'automation': {'emoji': '🤖', 'name': '自动化'},
    'markdown': {'emoji': '📝', 'name': 'Markdown'},
    
    'entertainment': {'emoji': '🎭', 'name': '娱乐'},
}


def get_all_repos():
    """获取用户的所有仓库（包括私有）"""
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    repos = []
    page = 1
    per_page = 100
    
    while True:
        url = f'{API_BASE}/user/repos'
        params = {
            'per_page': per_page,
            'page': page,
            'type': 'owner',  # 只获取自己的仓库，不包括fork的组织仓库
            'sort': 'updated',
            'direction': 'desc'
        }
        
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        if not data:
            break
            
        repos.extend(data)
        page += 1
    
    return repos


def categorize_repos(repos):
    """根据topics分类仓库"""
    categorized = defaultdict(list)
    original_repos = []
    forked_repos = []
    
    for repo in repos:
        # 跳过特殊仓库（个人主页仓库）
        if repo['name'] == GITHUB_USERNAME:
            continue
        
        # 获取topics
        topics = repo.get('topics', [])
        
        # 跳过没有topics的仓库
        if not topics:
            continue
        
        # 区分原创和fork
        if repo['fork']:
            forked_repos.append(repo)
        else:
            original_repos.append(repo)
        
        # 使用第一个topic作为分类
        category = topics[0]
        
        # 生成显示名称（emoji + 中文名）
        if category in TOPIC_CONFIG:
            emoji = TOPIC_CONFIG[category]['emoji']
            name = TOPIC_CONFIG[category]['name']
            category_display = f"{emoji} {name}"
        else:
            # 如果没有配置，使用默认格式
            category_display = f"📦 {category.replace('-', ' ').title()}"
        
        repo_info = {
            'name': repo['name'],
            'description': repo['description'] or '暂无描述',
            'url': repo['html_url'],
            'private': repo['private'],
            'stars': repo['stargazers_count'],
            'language': repo['language'],
            'topics': topics,
            'updated_at': repo['updated_at'],
            'fork': repo['fork']
        }
        
        categorized[category_display].append(repo_info)
    
    return categorized, len(original_repos), len(forked_repos)


def format_repo_item(repo):
    """格式化单个仓库条目"""
    name = repo['name']
    url = repo['url']
    desc = repo['description']
    private_badge = ' 🔒' if repo['private'] else ''
    
    return f"- **[{name}]({url})**{private_badge} - {desc}"


def generate_projects_section(categorized):
    """生成项目分类部分的Markdown"""
    lines = []
    
    # 按分类名称排序
    sorted_categories = sorted(categorized.keys())
    
    for category in sorted_categories:
        repos = categorized[category]
        
        # 按stars数量排序
        repos.sort(key=lambda x: x['stars'], reverse=True)
        
        lines.append(f"\n### {category}\n")
        
        for repo in repos:
            lines.append(format_repo_item(repo))
        
        lines.append('')  # 空行
    
    return '\n'.join(lines)


def update_readme(content):
    """更新README文件"""
    # 读取当前README
    readme_path = 'README.md'
    with open(readme_path, 'r', encoding='utf-8') as f:
        readme = f.read()
    
    # 定义标记
    start_marker = '<!-- AUTO-GENERATED-PROJECTS-START -->'
    end_marker = '<!-- AUTO-GENERATED-PROJECTS-END -->'
    
    # 检查是否存在标记
    if start_marker in readme and end_marker in readme:
        # 替换标记之间的内容
        pattern = f'{re.escape(start_marker)}.*?{re.escape(end_marker)}'
        new_content = f'{start_marker}\n{content}\n{end_marker}'
        updated_readme = re.sub(pattern, new_content, readme, flags=re.DOTALL)
    else:
        # 如果没有标记，在文件末尾添加
        updated_readme = readme + f'\n\n{start_marker}\n{content}\n{end_marker}\n'
    
    # 写回文件
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(updated_readme)
    
    print("✅ README已更新")


def main():
    """主函数"""
    print("🚀 开始更新README...")
    
    if not GITHUB_TOKEN:
        print("❌ 错误：未找到GH_TOKEN环境变量")
        return
    
    # 获取所有仓库
    print("📥 正在获取仓库列表...")
    repos = get_all_repos()
    print(f"✅ 获取到 {len(repos)} 个仓库")
    
    # 分类仓库
    print("📊 正在分类仓库...")
    categorized, original_count, forked_count = categorize_repos(repos)
    print(f"✅ 分类完成：{len(categorized)} 个分类")
    print(f"   - 原创项目: {original_count}")
    print(f"   - Fork项目: {forked_count}")
    
    # 生成Markdown内容
    print("📝 正在生成Markdown...")
    update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    markdown_content = f"""
## 🎯 我的所有项目

> 📊 总计 **{len(repos)}** 个仓库 | 原创 **{original_count}** | Fork **{forked_count}**  
> 🔒 带锁标记的为私有仓库  
> 🤖 最后更新: {update_time} (UTC+0)

{generate_projects_section(categorized)}
"""
    
    # 更新README
    print("💾 正在更新README文件...")
    update_readme(markdown_content)
    
    print("🎉 完成！")


if __name__ == '__main__':
    main()

