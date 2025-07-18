# 环境变量安全管理指南

本项目采用安全的两层环境变量管理策略，确保敏感信息不会意外泄露到版本控制中。

## 🔒 安全策略

### 第一层：敏感信息（系统环境变量）
**必须**通过系统环境变量（如 ~/.zshrc）设置，**绝不**放在任何 .env 文件中：

```bash
# 添加到 ~/.zshrc 文件中
export ARK_API_KEY="your_actual_api_key"
export LANGSMITH_API_KEY="your_actual_api_key"
export OPENAI_API_KEY="your_actual_api_key"  # 可选
```

### 第二层：非敏感配置（.env 文件）
可以安全地提交到版本控制的配置：

```bash
# .env 文件内容
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=agents-from-scratch
ARK_BASE_URL=https://ark.cn-beijing.volces.com/api/v3/
ARK_MODEL=ep-20250327064751-rjnld
```

## 🚀 快速设置

### 方法一：使用设置脚本
```bash
# 交互式设置
source setup_env.sh
```

### 方法二：手动设置
1. **设置敏感环境变量**：
   ```bash
   # 编辑 zsh 配置
   vim ~/.zshrc
   
   # 添加敏感变量（参考 src/email_assistant/env_setup.py）
   export ARK_API_KEY="your_api_key"
   export LANGSMITH_API_KEY="your_api_key"
   
   # 重新加载配置
   source ~/.zshrc
   ```

2. **配置非敏感设置**：
   ```bash
   # .env 文件已经包含了默认的非敏感配置
   # 如需修改，直接编辑 .env 文件即可
   ```

## 📁 相关文件

- **`.env`** - 非敏感配置（可提交到 git）
- **`.env.example`** - 配置模板和说明
- **`src/email_assistant/env_setup.py`** - 敏感变量设置模板
- **`setup_env.sh`** - 交互式设置脚本

## ✅ 验证设置

运行以下命令验证环境变量是否正确设置：

```bash
# 检查敏感变量（只显示前几位）
echo "ARK_API_KEY: ${ARK_API_KEY:0:8}..."
echo "LANGSMITH_API_KEY: ${LANGSMITH_API_KEY:0:8}..."

# 检查非敏感变量
echo "ARK_BASE_URL: $ARK_BASE_URL"
echo "ARK_MODEL: $ARK_MODEL"
```

## 🛡️ 安全优势

1. **敏感信息隔离**：API Keys 永远不会出现在任何可能被提交的文件中
2. **便于协作**：非敏感配置可以安全地在团队间分享
3. **环境一致性**：默认配置确保开发环境的一致性
4. **意外保护**：即使误操作也不会将敏感信息提交到 git

## ⚠️ 重要提醒

- **绝对不要**将 API Keys 放在 .env 文件中
- **务必**将敏感变量添加到 ~/.zshrc 或 ~/.bashrc
- **定期检查**确保敏感信息没有被意外提交到版本控制
