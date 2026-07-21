from src.dashboard.utils.db import *

print("=" * 50)
print("Companies")
print(get_companies().shape)

print("=" * 50)
print("Latest Ratios")
print(get_latest_ratios().shape)

print("=" * 50)
print("Sector Summary")
print(get_sector_summary())

print("=" * 50)
print("Peer Groups")
print(get_peer_groups())
print("=" * 50)
print("Market Summary")
print(get_market_summary())

print("=" * 50)
print("Top Market Cap")
print(get_top_market_cap().head())

print("=" * 50)
print("Latest Market Data")
print(get_latest_market_data().shape)