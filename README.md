# FINA4150-Project
## ETH Derivative Pricing (Accumulator)
### OTC Accumulator on Crypto

Trade date: ____________

Valuation date / Maturity date: 3 months after Trade date

Underlying Ticker
Ethereum ETH

Initial spot: _____________USDT

Accumulation periods: Once every week (13 weeks).

Shares per day: 1 share

Forward Price (FP) or strike: XXX%

Gearing: 2x
- If the settlement price (weekend) is greater than or equal to the Forward Price (FP), the Daily
share accumulation shall be the shares per day.
- If the settlement price (weekend) is lower than the Forward Price, the Daily share accumulation
shall be 2x the shares per day.

Knock-out: 110% of initial spot
- If the settlement price (weekend) is greater than or equal to the KO price, the accumulator will
terminate immediately. Any share accumulated before the KO trigger will be delivered.
- If KO is NOT triggered, the investor will accumulate the share throughout the tenor of the
accumulator until maturity.
Guaranteed Period: 3 weeks (21 days)
- If KO occurs during the guaranteed period, the bank will sell investor the shares up to the
guaranteed period in addition to the shares accumulated before KO event.

Your task: Find FP 𝑿𝑿𝑿% such that the accumulator contract is priced at ZERO at inception
