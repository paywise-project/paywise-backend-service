from archipy.configs.base_config import BaseConfig


class RuntimeConfig(BaseConfig):
    AUTH_GET_USER_CACHE_EXPIRATION_SECONDS: int = 11
    PUBLIC_BASE_DIR: str = "/app/media/static"
    SECURE_BASE_DIR: str = "/app/media"
    SECURE_BASE_URL: str = "https://paywise-api.dipper.ir"
    AUTH_CREATE_TOTP_CALLS_COUNT_LIMIT: int = 10
    AUTH_CREATE_TOTP_MINUTES_LIMIT: int = 1
    AUTH_VERIFY_TOTP_CALLS_COUNT_LIMIT: int = 10
    AUTH_VERIFY_TOTP_MINUTES_LIMIT: int = 1
    ADMIN_AUTH_LOGIN_CALLS_COUNT_LIMIT: int = 10
    ADMIN_AUTH_LOGIN_MINUTES_LIMIT: int = 1
    # REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_URL: str = "redis://redis:6379/0"
    SCHEDULER_TRIGGER_TYPE: str = "cron"
    SCHEDULER_HOUR: int = 2
    SCHEDULER_MINUTE: int = 30


BaseConfig.set_global(RuntimeConfig())
