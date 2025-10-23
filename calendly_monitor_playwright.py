#!/usr/bin/env python3
"""
Calendly Monitor using Playwright to handle JavaScript rendering
"""

import asyncio
from playwright.async_api import async_playwright
from datetime import datetime
import requests
import re

CALENDLY_URLS = [
    "https://calendly.com/markzoril/50-minute-emoney-planning-session?back=1&month=2025-10",
    "https://calendly.com/markzoril/50-minute-emoney-planning-session?back=1&month=2025-11"
]

CUTOFF_DATE = datetime(2025, 11, 29)
NTFY_TOPIC = "calendly-monitor-markzoril-2025"

def send_ntfy_notification(title, message):
    """Send FREE notification via ntfy.sh"""
    url = f"https://ntfy.sh/{NTFY_TOPIC}"

    try:
        response = requests.post(
            url,
            data=message.encode('utf-8'),
            headers={
                "Title": title,
                "Priority": "high",
                "Tags": "calendar,alarm_clock,white_check_mark"
            }
        )
        response.raise_for_status()
        print(f"✅ Notification sent via ntfy.sh!")
        return True
    except Exception as e:
        print(f"❌ Failed to send notification: {e}")
        return False

async def check_calendly_with_playwright(url):
    """Check Calendly using Playwright to render JavaScript"""
    print(f"  → Loading page with JavaScript rendering...")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            # Go to the page
            await page.goto(url, wait_until="networkidle", timeout=60000)

            # Wait for calendar to load
            await page.wait_for_timeout(3000)

            # Look for available date buttons/elements
            # Calendly typically marks available dates with specific classes or data attributes
            available_slots = []

            # Try to find clickable date elements
            date_elements = await page.query_selector_all('[data-container="spot-date-wrapper"]')

            for element in date_elements:
                date_str = await element.get_attribute('data-date')
                if date_str:
                    try:
                        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                        if date_obj < CUTOFF_DATE and date_obj.date() >= datetime.now().date():
                            available_slots.append(date_str)
                            print(f"  ✓ Found available slot: {date_str}")
                    except ValueError:
                        pass

            # Alternative: Look in the page content after JavaScript runs
            if not available_slots:
                content = await page.content()
                # Look for date patterns with available status
                pattern = r'"date":"(2025-\d{2}-\d{2})"[^}]*"status":"available"'
                matches = re.findall(pattern, content)

                for date_str in matches:
                    try:
                        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                        if date_obj < CUTOFF_DATE and date_obj.date() >= datetime.now().date():
                            if date_str not in available_slots:
                                available_slots.append(date_str)
                                print(f"  ✓ Found available slot: {date_str}")
                    except ValueError:
                        pass

            await browser.close()
            return sorted(list(set(available_slots)))

        except Exception as e:
            print(f"  ❌ Error: {e}")
            await browser.close()
            return []

async def main():
    """Main monitoring function"""
    print(f"\n{'='*60}")
    print(f"🔍 Calendly Monitor (Playwright) - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📱 Topic: {NTFY_TOPIC}")
    print(f"{'='*60}\n")

    all_available_slots = []

    for url in CALENDLY_URLS:
        month_match = re.search(r'month=(\d{4}-\d{2})', url)
        month_str = month_match.group(1) if month_match else "Unknown"

        print(f"📅 Checking {month_str}...")
        slots = await check_calendly_with_playwright(url)

        if slots:
            print(f"✅ Found {len(slots)} available slot(s): {', '.join(slots)}")
            all_available_slots.extend([(month_str, slot) for slot in slots])
        else:
            print(f"❌ No slots found for {month_str}")

        await asyncio.sleep(2)

    if all_available_slots:
        message = "🎉 CALENDLY SLOTS AVAILABLE!\n\n"
        message += "Available dates:\n"
        for month, slot in all_available_slots:
            message += f"• {slot}\n"
        message += f"\nBook now:\n{CALENDLY_URLS[0].split('?')[0]}"

        print(f"\n🔔 SLOTS AVAILABLE! Sending notification...")
        send_ntfy_notification(
            title="Calendly Slot Available!",
            message=message
        )
    else:
        print(f"\n😔 No available slots found before {CUTOFF_DATE.strftime('%b %d, %Y')}")

    print(f"\n{'='*60}")
    print(f"Next check in 30 minutes...")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    asyncio.run(main())
