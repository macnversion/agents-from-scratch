"""
Environment variable management module.
This module implements a secure two-tier environment variable management:
1. Non-sensitive config (base URLs, models, etc.) loaded from .env file
2. Sensitive info (API keys) loaded from system environment variables only
"""

import os
import logging
from typing import Optional, Dict, Any
from pathlib import Path
from dotenv import load_dotenv

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load .env file for non-sensitive configuration
# The .env file can be safely committed to version control
env_path = Path(__file__).parent.parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)
    logger.info(f"Loaded non-sensitive config from {env_path}")

# SENSITIVE variables - MUST be set in system environment (e.g., ~/.zshrc)
# These should NEVER appear in any .env file
SENSITIVE_ENV_VARS = [
    "ARK_API_KEY",
    "LANGSMITH_API_KEY",
    "OPENAI_API_KEY",  # Optional but sensitive if used
    "GMAIL_CREDENTIALS_PATH",  # Path to sensitive Gmail credentials
    "GMAIL_TOKEN_PATH",  # Path to sensitive Gmail token
]

# NON-SENSITIVE variables - loaded from .env file with defaults
# These can be safely shared and committed to version control
NON_SENSITIVE_ENV_VARS = {
    "LANGSMITH_TRACING": "true",
    "LANGSMITH_PROJECT": "agents-from-scratch", 
    "ARK_BASE_URL": "https://ark.cn-beijing.volces.com/api/v3/",
    "ARK_MODEL": "ep-20250327064751-rjnld",
}

# Required sensitive variables that must be present
REQUIRED_SENSITIVE_VARS = [
    "ARK_API_KEY",
    "LANGSMITH_API_KEY",
]

def check_required_env_vars() -> Dict[str, str]:
    """
    检查所有必需的环境变量是否已设置。
    实施安全的两层环境变量管理：
    1. 敏感信息必须来自系统环境变量
    2. 非敏感信息从 .env 文件或环境变量加载
    
    Returns:
        Dict[str, str]: 包含所有环境变量的字典
        
    Raises:
        ValueError: 如果缺少必需的敏感环境变量
    """
    missing_sensitive_vars = []
    env_vars = {}
    
    # 检查必需的敏感环境变量（必须来自系统环境）
    for var in REQUIRED_SENSITIVE_VARS:
        # 直接从系统环境读取，不使用 .env 文件中的值
        value = os.environ.get(var)
        if not value:
            missing_sensitive_vars.append(var)
        else:
            env_vars[var] = value
    
    # 检查所有敏感变量（包括可选的）
    for var in SENSITIVE_ENV_VARS:
        if var not in REQUIRED_SENSITIVE_VARS:
            value = os.environ.get(var)
            if value:
                env_vars[var] = value
    
    # 加载非敏感环境变量（可以来自 .env 文件或系统环境）
    for var, default_value in NON_SENSITIVE_ENV_VARS.items():
        env_vars[var] = os.environ.get(var, default_value)
    
    if missing_sensitive_vars:
        raise ValueError(
            f"Missing required sensitive environment variables: {', '.join(missing_sensitive_vars)}\n"
            f"These MUST be set in your system environment (e.g., in ~/.zshrc) for security:\n"
            + "\n".join([f"export {var}='your_value'" for var in missing_sensitive_vars]) + "\n\n"
            f"Non-sensitive config is loaded from .env file automatically."
        )
    
    logger.info("All required environment variables are set.")
    logger.info(f"Loaded {len([v for v in env_vars.keys() if v in SENSITIVE_ENV_VARS])} sensitive variables from system environment")
    logger.info(f"Loaded {len([v for v in env_vars.keys() if v in NON_SENSITIVE_ENV_VARS])} non-sensitive variables")
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
