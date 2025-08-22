from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # World Bank
    world_bank_base_url: str = (
        "https://api.worldbank.org/v2/country/IND/indicator/FP.CPI.TOTL.ZG?format=json"
    )
    fallback_inflation: float = 6.0
    cache_ttl_inflation_seconds: int = 86400

    # Yahoo Finance
    # These endpoints are the JSON chart endpoints commonly used for quick pulls
    yf_nifty_url: str = (
        "https://query1.finance.yahoo.com/v8/finance/chart/%5ENSEI?range=1d&interval=1d"
    )
    yf_sensex_url: str = (
        "https://query1.finance.yahoo.com/v8/finance/chart/%5EBSESN?range=1d&interval=1d"
    )
    cache_ttl_market_seconds: int = 900
    
    # Mock toggle - set to False to enable live market data
    use_mock_market: bool = False

    class Config:
        env_file = ".env"


settings = Settings()
