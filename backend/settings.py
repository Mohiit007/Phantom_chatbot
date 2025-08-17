from pydantic_settings import BaseSettings  # ✅ instead of from pydantic import BaseSettings


class Settings(BaseSettings):
    # World Bank
    world_bank_base_url: str
    fallback_inflation: float
    cache_ttl_inflation_seconds: int = 86400

    # Yahoo Finance
    yf_nifty_url: str
    yf_sensex_url: str
    cache_ttl_market_seconds: int = 900

    class Config:
        env_file = ".env"


settings = Settings()
