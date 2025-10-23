#!/usr/bin/env python3
"""
Test version - ALWAYS sends a notification to verify GitHub Actions → ntfy works
"""

import requests
from datetime import datetime

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
                "Tags": "test_tube,bell,white_check_mark"
            }
        )
        response.raise_for_status()
        print(f"✅ Notification sent via ntfy.sh!")
        print(f"   Subscribe to '{NTFY_TOPIC}' in the ntfy app to receive it")
        return True
    except Exception as e:
        print(f"❌ Failed to send notification: {e}")
        return False

def main():
    """Main test function - always sends a notification"""
    print(f"\n{'='*60}")
    print(f"🧪 TEST MODE - GitHub Actions → ntfy.sh")
    print(f"📱 Topic: {NTFY_TOPIC}")
    print(f"🕐 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    # Always send a test notification
    message = f"""🧪 GitHub Actions Test Notification

This is a test run from GitHub Actions to verify the notification system is working correctly.

✅ If you received this on your iPhone, the connection between GitHub Actions and ntfy.sh is working!

Run time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
Topic: {NTFY_TOPIC}

The actual Calendly monitor will check for available slots and notify you when found.

This test will be removed after successful verification."""

    print("🔔 Sending test notification...")
    send_ntfy_notification(
        title="GitHub Actions to ntfy Test",
        message=message
    )

    print(f"\n{'='*60}")
    print(f"✅ Test complete!")
    print(f"📱 Check your iPhone ntfy app for the notification")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
