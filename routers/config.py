from fastapi import APIRouter

from ailemdar.config import get_config

router = APIRouter()


@router.get("")
async def get_config_info():
    config = get_config()
    
    return {
        "platform": "bitbucket" if config.is_bitbucket_configured else "github",
        "repository": config.repository_full_name,
        "is_bitbucket_server": config.is_bitbucket_server,
        "llm": {
            "provider": config.llm_provider.value,
            "model": config.llm_model,
            "temperature": config.llm_temperature,
        },
        "embedding": {
            "mode": config.embedding_mode,
            "model": config.embedding_model,
        },
        "target_branch": config.target_branch,
        "workspace_path": config.workspace_path,
        "theme_mode": config.theme_mode,
    }
