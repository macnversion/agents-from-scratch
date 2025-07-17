"""
Environment variable management module.
This module handles environment variable loading without using .env files.
"""

import os
import logging
from typing import Optional, Dict, Any

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 必需的环境变量
REQUIRED_ENV_VARS = [
    "ARK_API_KEY",
    "LANGSMITH_API_KEY",
]

# 可选的环境变量及其默认值
OPTIONAL_ENV_VARS = {
    "LANGSMITH_TRACING": "true",
    "LANGSMITH_PROJECT": "agents-from-scratch",
    "ARK_BASE_URL": "https://ark.cn-beijing.volces.com/api/v3/",
    "ARK_MODEL": "ep-20250327064751-rjnld",
}

def check_required_env_vars() -> Dict[str, str]:
    """
    检查所有必需的环境变量是否已设置。
    
    Returns:
        Dict[str, str]: 包含所有环境变量的字典
        
    Raises:
        ValueError: 如果缺少必需的环境变量
    """
    missing_vars = []
    env_vars = {}
    
    # 检查必需的环境变量
    for var in REQUIRED_ENV_VARS:
        value = os.environ.get(var)
        if not value:
            missing_vars.append(var)
        else:
            env_vars[var] = value
    
    # 检查可选的环境变量
    for var, default_value in OPTIONAL_ENV_VARS.items():
        env_vars[var] = os.environ.get(var, default_value)
    
    if missing_vars:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing_vars)}\n"
            f"Please set them in your shell environment (e.g., in ~/.zshrc):\n"
            + "\n".join([f"export {var}='your_value'" for var in missing_vars])
        )
    
    logger.info("All required environment variables are set.")
    return env_vars

def get_env_var(var_name: str, default: Optional[str] = None) -> Optional[str]:
    """
    获取环境变量的值。
    
    Args:
        var_name: 环境变量名称
        default: 默认值
        
    Returns:
        环境变量的值或默认值
    """
    return os.environ.get(var_name, default)

def ensure_env_setup() -> None:
    """
    确保环境变量已正确设置。
    这个函数应该在每个模块的开始调用。
    """
    try:
        check_required_env_vars()
    except ValueError as e:
        logger.error(str(e))
        raise

# 在模块导入时自动检查环境变量
if __name__ != "__main__":
    ensure_env_setup()
