#!/usr/bin/env python3
"""
Debug script to figure out how to detect Calendly availability
"""

import requests
from bs4 import BeautifulSoup
import re
import json

url = "https://calendly.com/markzoril/50-minute-emoney-planning-session?back=1&month=2025-11"

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

print("Fetching Calendly page...")
response = requests.get(url, headers=headers, timeout=30)
print(f"Status: {response.status_code}\n")

# Look for script tags with JSON data
soup = BeautifulSoup(response.text, 'html.parser')
scripts = soup.find_all('script')

print(f"Found {len(scripts)} script tags\n")

# Look for any JSON-like data
for i, script in enumerate(scripts):
    if script.string:
        # Look for anything that might contain event data
        if any(keyword in script.string.lower() for keyword in ['event', 'booking', 'available', 'calendar', 'slot']):
            content = script.string[:500]
            print(f"=== Script {i} (contains calendar keywords) ===")
            print(content)
            print("\n")

# Look for meta tags or data attributes
print("=== Looking for data attributes ===")
for tag in soup.find_all(attrs={"data-component": True}):
    print(f"{tag.name}: {tag.attrs}")

print("\n=== Looking for links to API ===")
api_patterns = [
    r'https://[^"]*calendly[^"]*api[^"]*',
    r'/api/[^"]+',
    r'event_types/[^/"]+',
]

for pattern in api_patterns:
    matches = re.findall(pattern, response.text)
    if matches:
        print(f"Pattern '{pattern}':")
        for match in list(set(matches))[:5]:
            print(f"  - {match}")
print("\nDone!")
