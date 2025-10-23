#!/usr/bin/env python3
"""
Free version using ntfy.sh - no account or payment required!
"""

import requests
from datetime import datetime
import re
import time
import calendar

CALENDLY_URLS = [
    "https://calendly.com/markzoril/50-minute-emoney-planning-session?back=1&month=2025-10",
    "https://calendly.com/markzoril/50-minute-emoney-planning-session?back=1&month=2025-11"
]

CUTOFF_DATE = datetime(2025, 11, 29)

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

        available_slots = []

        # Extract profile and event type from URL
        # URL format: https://calendly.com/markzoril/50-minute-emoney-planning-session?...
        profile_match = re.search(r'calendly\.com/([^/]+)/([^?]+)', url)
        if not profile_match:
            print(f"  ❌ Could not parse URL")
            return []

        profile_slug = profile_match.group(1)
        event_type_slug = profile_match.group(2)

        print(f"  → Looking up event type: {profile_slug}/{event_type_slug}")

        # Step 1: Get event type UUID
        lookup_url = f"https://calendly.com/api/booking/event_types/lookup?event_type_slug={event_type_slug}&profile_slug={profile_slug}"

        try:
            lookup_response = requests.get(lookup_url, headers=headers, timeout=30)
            lookup_response.raise_for_status()
            lookup_data = lookup_response.json()

            if 'resource' not in lookup_data or 'uuid' not in lookup_data['resource']:
                print(f"  ❌ No UUID found in lookup response")
                return []

            event_uuid = lookup_data['resource']['uuid']
            scheduling_link_uuid = lookup_data['resource'].get('scheduling_link_uuid', '')
            print(f"  ✓ Found event UUID: {event_uuid}")

        except Exception as e:
            print(f"  ❌ Lookup failed: {e}")
            return []

        # Step 2: Get availability for the month
        month_match = re.search(r'month=(\d{4}-\d{2})', url)
        if not month_match:
            print(f"  ❌ Could not extract month from URL")
            return []

        month = month_match.group(1)
        year, month_num = month.split('-')

        # Calculate last day of month
        import calendar
        last_day = calendar.monthrange(int(year), int(month_num))[1]

        availability_url = f"https://calendly.com/api/booking/event_types/{event_uuid}/calendar/range"
        params = {
            'timezone': 'America/Los_Angeles',
            'diagnostics': 'false',
            'range_start': f'{month}-01',
            'range_end': f'{month}-{last_day:02d}'
        }

        # Add scheduling_link_uuid if available
        if scheduling_link_uuid:
            params['scheduling_link_uuid'] = scheduling_link_uuid

        print(f"  → Checking availability for {month}...")

        try:
            avail_response = requests.get(availability_url, headers=headers, params=params, timeout=30)
            avail_response.raise_for_status()
            avail_data = avail_response.json()

            if 'days' in avail_data:
                for day in avail_data['days']:
                    if day.get('status') == 'available' and day.get('spots'):
                        date_str = day['date']
                        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                        if date_obj < CUTOFF_DATE and date_obj.date() >= datetime.now().date():
                            available_slots.append(date_str)
                            print(f"  ✓ Found available slot: {date_str} ({len(day['spots'])} spots)")
            else:
                print(f"  ⚠️  Unexpected response structure: {list(avail_data.keys())}")

        except Exception as e:
            print(f"  ❌ Availability check failed: {e}")

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
            title="Calendly Slot Available!",
            message=message
        )
    else:
        print(f"\n😔 No available slots found before {CUTOFF_DATE.strftime('%b %d, %Y')}")

    print(f"\n{'='*60}")
    print(f"Next check in 30 minutes...")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
