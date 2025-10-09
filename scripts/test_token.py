#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试GitHub Token是否配置正确，是否能访问私有仓库
"""

import os
import sys
import requests

# 设置UTF-8编码输出
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

GITHUB_TOKEN = os.environ.get('GH_TOKEN')
API_BASE = 'https://api.github.com'

def test_token():
    """测试Token配置"""
    
    print("=" * 60)
    print("GitHub Token 诊断工具")
    print("=" * 60)
    print()
    
    # 检查环境变量
    if not GITHUB_TOKEN:
        print("❌ 错误：未找到 GH_TOKEN 环境变量")
        print()
        print("请设置环境变量：")
        print("  Windows CMD: set GH_TOKEN=你的token")
        print("  PowerShell:  $env:GH_TOKEN='你的token'")
        print("  Linux/Mac:   export GH_TOKEN=你的token")
        return
    
    print(f"✅ 找到 GH_TOKEN: {GITHUB_TOKEN[:10]}...{GITHUB_TOKEN[-4:]}")
    print()
    
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # 测试1: 检查Token权限
    print("📝 测试1: 检查Token权限...")
    try:
        response = requests.get(f'{API_BASE}/user', headers=headers)
        response.raise_for_status()
        user_data = response.json()
        print(f"✅ Token有效！当前用户: {user_data['login']}")
        print(f"   公开仓库数: {user_data.get('public_repos', 0)}")
        print(f"   私有仓库数: {user_data.get('total_private_repos', 0)}")
        print(f"   总仓库数: {user_data.get('public_repos', 0) + user_data.get('total_private_repos', 0)}")
    except Exception as e:
        print(f"❌ Token无效或权限不足: {e}")
        return
    
    print()
    
    # 测试2: 获取仓库列表
    print("📝 测试2: 获取仓库列表...")
    try:
        params = {
            'per_page': 10,
            'type': 'owner',
            'sort': 'updated'
        }
        response = requests.get(f'{API_BASE}/user/repos', headers=headers, params=params)
        response.raise_for_status()
        repos = response.json()
        
        print(f"✅ 成功获取仓库列表（前10个）")
        print()
        
        public_count = 0
        private_count = 0
        
        print("仓库列表：")
        print("-" * 60)
        for repo in repos:
            status = "🔒 私有" if repo['private'] else "🌐 公开"
            print(f"{status} - {repo['name']}")
            if repo['private']:
                private_count += 1
            else:
                public_count += 1
        
        print("-" * 60)
        print(f"前10个仓库中: 公开 {public_count} 个, 私有 {private_count} 个")
        
        if private_count == 0 and user_data.get('total_private_repos', 0) > 0:
            print()
            print("⚠️  警告: 你有私有仓库，但API没有返回")
            print("   可能的原因:")
            print("   1. Token没有勾选 'repo' 完整权限")
            print("   2. 请重新生成Token，确保勾选 'repo' (Full control of private repositories)")
        
    except Exception as e:
        print(f"❌ 获取仓库列表失败: {e}")
        return
    
    print()
    
    # 测试3: 检查Token的OAuth scopes
    print("📝 测试3: 检查Token权限范围...")
    try:
        response = requests.get(f'{API_BASE}/user/repos', headers=headers, params={'per_page': 1})
        scopes = response.headers.get('X-OAuth-Scopes', '')
        print(f"✅ Token权限范围: {scopes}")
        
        if 'repo' not in scopes:
            print()
            print("❌ 错误: Token缺少 'repo' 权限！")
            print("   请重新生成Token，并确保勾选:")
            print("   ✅ repo (Full control of private repositories)")
        else:
            print("✅ Token具有访问私有仓库的权限")
            
    except Exception as e:
        print(f"⚠️  无法检查权限范围: {e}")
    
    print()
    print("=" * 60)
    print("诊断完成")
    print("=" * 60)


if __name__ == '__main__':
    test_token()

