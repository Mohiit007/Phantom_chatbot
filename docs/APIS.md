## External APIs

### World Bank – Inflation (India)
- Base endpoint: `https://api.worldbank.org/v2/country/IND/indicator/FP.CPI.TOTL.ZG?format=json`
- Data: Annual inflation, consumer prices (annual %)
- Notes: Paginated. Use most recent non-null value.

### Yahoo Finance – Indices (Unofficial JSON endpoints may change)
- Nifty 50: `https://query1.finance.yahoo.com/v8/finance/chart/%5ENSEI?range=1d&interval=1m`
- Sensex (BSE SENSEX): `https://query1.finance.yahoo.com/v8/finance/chart/%5EBSESN?range=1d&interval=1m`
- Notes: No API key for these endpoints; subject to change or rate limit. For production, consider a stable provider or RapidAPI.

### Fallback Strategy
- If API calls fail, use default inflation rate of 6.5%.
- Cache last successful responses to disk for offline demo.


