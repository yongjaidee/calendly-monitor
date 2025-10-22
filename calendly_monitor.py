#!/usr/bin/env python3
"""
Free version using ntfy.sh - no account or payment required!
"""

import requests
from datetime import datetime
from bs4 import BeautifulSoup
import re
import time

CALENDLY_URLS = [
    "https://calendly.com/markzoril/50-minute-emoney-planning-session?back=1&month=2025-10",
    "https://calendly.com/markzoril/50-minute-emoney-planning-session?back=1&month=2025-11"
]

CUTOFF_DATE = datetime(2025, 11, 19)

# Choose a unique topic name (this is your notification channel)
NTFY_TOPIC = "calendly-monitor-markzoril-2025"  # Change this to something unique!

def send_ntfy_notification(title, message):
    """
    Send FREE notification via ntfy.sh
    No account or API keys needed!
    """
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
        print(f"   Subscribe to '{NTFY_TOPIC}' in the ntfy app to receive it")
        return True
    except Exception as e:
        print(f"❌ Failed to send notification: {e}")
        return False

def check_calendly_availability(url):
    """Check Calendly page for available slots"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        scripts = soup.find_all('script')
        available_slots = []

        for script in scripts:
            if script.string and 'available' in script.string.lower():
                try:
                    date_pattern = r'(\d{4}-\d{2}-\d{2})'
                    dates = re.findall(date_pattern, script.string)

                    for date_str in dates:
                        try:
                            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                            if date_obj < CUTOFF_DATE and date_obj > datetime.now():
                                if date_str not in available_slots:
                                    available_slots.append(date_str)
                        except ValueError:
                            continue
                except Exception:
                    continue

        # Try API method
        calendly_api_pattern = r'https://calendly\.com/api/booking/event_types/([^/]+)/calendar/range'
        api_matches = re.findall(calendly_api_pattern, response.text)

        if api_matches and not available_slots:
            event_uuid = api_matches[0]
            month_match = re.search(r'month=(\d{4}-\d{2})', url)
            if month_match:
                month = month_match.group(1)
                api_url = f"https://calendly.com/api/booking/event_types/{event_uuid}/calendar/range?timezone=America/New_York&diagnostics=false&range_start={month}-01&range_end={month}-31"

                try:
                    api_response = requests.get(api_url, headers=headers, timeout=30)
                    api_data = api_response.json()

                    if 'days' in api_data:
                        for day in api_data['days']:
                            if day.get('status') == 'available' and day.get('spots'):
                                date_str = day['date']
                                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                                if date_obj < CUTOFF_DATE and date_obj > datetime.now():
                                    available_slots.append(date_str)
                except Exception as e:
                    print(f"API call failed: {e}")

        return sorted(list(set(available_slots)))

    except Exception as e:
        print(f"❌ Error checking {url}: {e}")
        return []

def main():
    """Main monitoring function"""
    print(f"\n{'='*60}")
    print(f"🔍 Calendly Monitor (FREE ntfy.sh) - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📱 Topic: {NTFY_TOPIC}")
    print(f"{'='*60}\n")

    all_available_slots = []

    for url in CALENDLY_URLS:
        month_match = re.search(r'month=(\d{4}-\d{2})', url)
        month_str = month_match.group(1) if month_match else "Unknown"

        print(f"📅 Checking {month_str}...")
        slots = check_calendly_availability(url)

        if slots:
            print(f"✅ Found {len(slots)} available slot(s): {', '.join(slots)}")
            all_available_slots.extend([(month_str, slot) for slot in slots])
        else:
            print(f"❌ No slots found for {month_str}")

        time.sleep(2)

    if all_available_slots:
        message = "🎉 CALENDLY SLOTS AVAILABLE!\n\n"
        message += "Available dates:\n"
        for month, slot in all_available_slots:
            message += f"• {slot}\n"
        message += f"\nBook now:\n{CALENDLY_URLS[0].split('?')[0]}"

        print(f"\n🔔 SLOTS AVAILABLE! Sending notification...")
        send_ntfy_notification(
            title="📅 Calendly Slot Available!",
            message=message
        )
    else:
        print("\n😔 No available slots found before Nov 19, 2025")

    print(f"\n{'='*60}")
    print(f"Next check in 30 minutes...")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
