# GitHub Actions 自动更新 README 设置指南

## 📋 配置步骤

### 1️⃣ 创建 Personal Access Token (PAT)

1. 访问 GitHub Settings: https://github.com/settings/tokens
2. 点击 **Developer settings** → **Personal access tokens** → **Tokens (classic)**
3. 点击 **Generate new token (classic)**
4. 填写信息：
   - **Note**: `README Auto Update` (或任何你喜欢的名称)
   - **Expiration**: 建议选择 `No expiration` 或 `1 year`
   - **Select scopes**: 勾选以下权限
     - ✅ `repo` (完整权限，包括私有仓库)
     - ✅ `workflow` (允许修改GitHub Actions)

5. 点击 **Generate token**
6. **重要**: 复制生成的token（离开页面后将无法再次查看）

### 2️⃣ 添加 Token 到仓库 Secrets

1. 进入你的仓库: https://github.com/FB208/FB208
2. 点击 **Settings** → **Secrets and variables** → **Actions**
3. 点击 **New repository secret**
4. 填写信息：
   - **Name**: `GH_TOKEN`
   - **Secret**: 粘贴刚才复制的token
5. 点击 **Add secret**

### 3️⃣ 验证配置

1. 进入 **Actions** 标签页
2. 选择 **Update README with Repositories** 工作流
3. 点击 **Run workflow** → **Run workflow** (手动触发)
4. 等待工作流运行完成（约30秒-1分钟）
5. 检查 README.md 是否已自动更新

## 🔧 工作原理

### 自动触发时机

- ⏰ **定时任务**: 每周日凌晨 2:00 UTC（北京时间上午10:00）
- 🖱️ **手动触发**: 在 Actions 页面随时手动运行
- 📝 **可选**: 取消注释 workflow 文件中的 `push` 触发器，每次提交时自动运行

### 分类逻辑

脚本会自动：
1. 获取你的所有仓库（公开 + 私有）
2. 使用每个仓库的**第一个 Topic** 作为分类依据
3. 如果仓库没有 Topics，归类到"其他项目"
4. 私有仓库会显示 🔒 标记
5. 按 Star 数量排序

### 添加 Topics 到仓库

为了更好的分类效果，建议给每个仓库添加 Topics：

1. 进入仓库页面
2. 点击仓库描述右侧的 ⚙️ 图标
3. 在 **Topics** 字段添加标签（第一个标签将用作分类）

**推荐 Topics**:
- `tool` - 工具类
- `ai` - AI相关
- `obsidian` - Obsidian插件
- `webdav` - WebDAV相关
- `browser-extension` - 浏览器扩展
- `blog` - 博客
- `python` / `javascript` / `csharp` - 按语言分类
- `productivity` - 生产力工具
- `backup` - 备份工具
- `network` / `proxy` - 网络工具

## 🎨 自定义

### 修改分类 Emoji

编辑 `scripts/update_readme.py` 中的 `CATEGORY_EMOJI` 字典：

```python
CATEGORY_EMOJI = {
    'tool': '🛠️',
    'ai': '🤖',
    'your-topic': '🎯',  # 添加你自己的
}
```

### 修改更新频率

编辑 `.github/workflows/update-readme.yml` 中的 cron 表达式：

```yaml
schedule:
  - cron: '0 2 * * 0'  # 每周日 2:00 UTC
  # - cron: '0 2 * * *'  # 每天 2:00 UTC
  # - cron: '0 2 1 * *'  # 每月1号 2:00 UTC
```

### 排除某些仓库

在 `scripts/update_readme.py` 的 `categorize_repos` 函数中添加：

```python
# 跳过特殊仓库
if repo['name'] in ['FB208', 'repo-to-skip', 'another-repo']:
    continue
```

## 🔒 安全提示

- ✅ Token 存储在 GitHub Secrets 中，加密且安全
- ✅ 私有仓库信息只在你的 Actions 日志中可见
- ✅ README 中的私有仓库链接依然受 GitHub 权限保护
- ⚠️ 不要将 Token 提交到代码仓库
- ⚠️ 定期检查 Token 的使用情况
- ⚠️ 如果 Token 泄露，立即在 GitHub Settings 中撤销

## 🐛 故障排除

### 问题1: Actions 运行失败，提示 "GH_TOKEN not found"
**解决**: 检查是否正确添加了 Secret，名称必须是 `GH_TOKEN`

### 问题2: 获取不到私有仓库
**解决**: 确保 Token 具有 `repo` 完整权限

### 问题3: README 没有更新
**解决**: 
1. 检查 Actions 日志是否有错误
2. 确保 README 中有标记注释
3. 尝试手动运行 workflow

### 问题4: 分类不正确
**解决**: 给仓库添加 Topics，第一个 Topic 将用作分类

## 📞 需要帮助？

如有问题，可以：
1. 查看 Actions 运行日志
2. 检查 `scripts/update_readme.py` 的输出
3. 在仓库创建 Issue

---

**祝使用愉快！** 🎉

