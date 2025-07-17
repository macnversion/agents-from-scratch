#!/bin/bash

# 环境变量设置脚本
# 使用方法：source setup_env.sh 或 . setup_env.sh

echo "设置 AI Agent 项目环境变量..."

# 检查是否已经设置了环境变量
if [ -z "$ARK_API_KEY" ]; then
    echo "请输入您的字节跳动豆包(Doubao) API Key:"
    read -s ARK_API_KEY
    export ARK_API_KEY
fi

if [ -z "$LANGSMITH_API_KEY" ]; then
    echo "请输入您的 LangSmith API Key:"
    read -s LANGSMITH_API_KEY
    export LANGSMITH_API_KEY
fi

# 设置默认值
export LANGSMITH_TRACING="true"
export LANGSMITH_PROJECT="agents-from-scratch"
export ARK_BASE_URL="https://ark.cn-beijing.volces.com/api/v3/"
export ARK_MODEL="ep-20250327064751-rjnld"

echo "环境变量设置完成！"
echo "ARK_API_KEY: ${ARK_API_KEY:0:8}..."
echo "LANGSMITH_API_KEY: ${LANGSMITH_API_KEY:0:8}..."
echo "LANGSMITH_TRACING: $LANGSMITH_TRACING"
echo "LANGSMITH_PROJECT: $LANGSMITH_PROJECT"
echo "ARK_BASE_URL: $ARK_BASE_URL"
echo "ARK_MODEL: $ARK_MODEL"

# 可选：将这些变量添加到 ~/.zshrc 或 ~/.bashrc
echo ""
echo "要将这些变量永久添加到您的 shell 配置中，请运行以下命令："
echo ""
echo "echo 'export ARK_API_KEY=\"$ARK_API_KEY\"' >> ~/.zshrc"
echo "echo 'export LANGSMITH_API_KEY=\"$LANGSMITH_API_KEY\"' >> ~/.zshrc"
echo "echo 'export LANGSMITH_TRACING=\"$LANGSMITH_TRACING\"' >> ~/.zshrc"
echo "echo 'export LANGSMITH_PROJECT=\"$LANGSMITH_PROJECT\"' >> ~/.zshrc"
echo "echo 'export ARK_BASE_URL=\"$ARK_BASE_URL\"' >> ~/.zshrc"
echo "echo 'export ARK_MODEL=\"$ARK_MODEL\"' >> ~/.zshrc"
echo ""
echo "然后执行: source ~/.zshrc"
