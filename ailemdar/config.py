import os
from enum import Enum
from typing import Optional

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class LLMProvider(str, Enum):
    OPENAI = "openai"
    AZURE_OPENAI = "azure_openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    MISTRAL = "mistral"
    OLLAMA = "ollama"


class EmbeddingMode(str, Enum):
    OPENAI = "openai"
    AZURE_OPENAI = "azure_openai"
    OLLAMA = "ollama"
    HUGGINGFACE = "huggingface"


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    llm_provider: LLMProvider = Field(LLMProvider.OPENAI, env="LLM_PROVIDER")
    llm_model: str = Field("gpt-4o", env="LLM_MODEL")
    llm_temperature: float = Field(0.1, env="LLM_TEMPERATURE")

    embedding_mode: EmbeddingMode = Field(EmbeddingMode.OPENAI, env="EMBEDDING_MODE")
    embedding_model: str = Field("text-embedding-3-small", env="EMBEDDING_MODEL")

    bitbucket_username: Optional[str] = Field(None, env="BITBUCKET_USERNAME")
    bitbucket_app_password: Optional[str] = Field(None, env="BITBUCKET_APP_PASSWORD")
    bitbucket_base_url: Optional[str] = Field(None, env="BITBUCKET_BASE_URL")
    bitbucket_server_url: Optional[str] = Field(None, env="BITBUCKET_SERVER_URL")

    github_token: Optional[str] = Field(None, env="GITHUB_TOKEN")

    repository_full_name: str = Field(..., env="REPOSITORY_FULL_NAME")
    target_branch: str = Field("main", env="TARGET_BRANCH")
    workspace_path: str = Field("workspace", env="WORKSPACE_PATH")

    theme_mode: str = Field("light", env="THEME_MODE")

    @computed_field
    @property
    def is_bitbucket_configured(self) -> bool:
        return self.bitbucket_username is not None and self.bitbucket_app_password is not None

    @computed_field
    @property
    def is_bitbucket_server(self) -> bool:
        return self.bitbucket_server_url is not None


_config: Optional[Config] = None

def get_config() -> Config:
    global _config
    if _config is None:
        _config = Config()
    return _config
