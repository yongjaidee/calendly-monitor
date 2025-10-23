#!/usr/bin/env python3
"""
Quick test script to send a notification via ntfy.sh
"""

import requests

# Same topic as in your monitoring script
NTFY_TOPIC = "calendly-monitor-markzoril-2025"

def send_test_notification():
    """Send a test notification"""
    url = f"https://ntfy.sh/{NTFY_TOPIC}"

    message = """🧪 Test Notification from Claude Code!

This is a test to verify your ntfy setup is working.

If you received this notification on your iPhone, you're all set! ✅

The Calendly monitor will send similar notifications when slots become available.

Time: Just now
Topic: calendly-monitor-markzoril-2025"""

    try:
        response = requests.post(
            url,
            data=message.encode('utf-8'),
            headers={
                "Title": "🧪 Test Notification - ntfy Working!",
                "Priority": "high",
                "Tags": "white_check_mark,bell,test_tube"
            }
        )
        response.raise_for_status()
        print("✅ Test notification sent successfully!")
        print(f"📱 Check your iPhone ntfy app")
        print(f"📡 Topic: {NTFY_TOPIC}")
        return True
    except Exception as e:
        print(f"❌ Failed to send notification: {e}")
        return False

if __name__ == "__main__":
    print("🔔 Sending test notification to ntfy...")
    print(f"📱 Topic: {NTFY_TOPIC}")
    print("")
    send_test_notification()
