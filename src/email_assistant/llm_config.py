"""
LLM 初始化模块
统一管理 LLM 的初始化配置，支持 OpenAI 兼容的 API
"""

import os
from langchain.chat_models import init_chat_model
from email_assistant.env_setup import get_env_var


def init_llm(temperature: float = 0.0, **kwargs):
    """
    初始化 LLM 模型
    
    Args:
        temperature: 温度参数，控制输出的随机性
        **kwargs: 其他 LLM 参数
    
    Returns:
        初始化后的 LLM 实例
    """
    # 获取环境变量
    api_key = get_env_var("ARK_API_KEY")
    base_url = get_env_var("ARK_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3/")
    model = get_env_var("ARK_MODEL", "ep-20250327064751-rjnld")
    
    # 使用 OpenAI 兼容的配置
    llm = init_chat_model(
        model="openai",  # 使用 OpenAI 兼容的接口
        temperature=temperature,
        api_key=api_key,
        base_url=base_url,
        model_name=model,
        **kwargs
    )
    
    return llm


def init_structured_llm(schema_class, temperature: float = 0.0, **kwargs):
    """
    初始化结构化输出的 LLM 模型
    
    Args:
        schema_class: Pydantic 模型类，定义输出结构
        temperature: 温度参数
        **kwargs: 其他 LLM 参数
    
    Returns:
        带有结构化输出的 LLM 实例
    """
    llm = init_llm(temperature=temperature, **kwargs)
    return llm.with_structured_output(schema_class)


def init_llm_with_tools(tools, tool_choice="any", parallel_tool_calls=False, temperature: float = 0.0, **kwargs):
    """
    初始化带有工具调用的 LLM 模型
    
    Args:
        tools: 工具列表
        tool_choice: 工具选择策略
        parallel_tool_calls: 是否允许并行工具调用
        temperature: 温度参数
        **kwargs: 其他 LLM 参数
    
    Returns:
        绑定工具的 LLM 实例
    """
    llm = init_llm(temperature=temperature, **kwargs)
    return llm.bind_tools(tools, tool_choice=tool_choice, parallel_tool_calls=parallel_tool_calls)


# 为了向后兼容，提供一个默认的 LLM 实例
def get_default_llm():
    """获取默认的 LLM 实例"""
    return init_llm()
