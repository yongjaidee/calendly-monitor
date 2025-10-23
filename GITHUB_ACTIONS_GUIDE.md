# GitHub Actions Monitoring Guide

## How to Monitor Your GitHub Actions

### Method 1: Via GitHub Website (Easiest)

1. **Go to your repository:**
   - URL: https://github.com/yongjaidee/calendly-monitor

2. **Click on the "Actions" tab** (top navigation bar)

3. **You'll see:**
   - List of all workflow runs
   - Status of each run (✅ success, ❌ failed, 🟡 in progress)
   - When each run started
   - How long it took

4. **Click on any run to see details:**
   - View the full output/logs
   - See what the script found
   - Check for any errors

### Method 2: Enable GitHub Notifications

**Get notified when workflows fail:**

1. Go to: https://github.com/settings/notifications
2. Scroll to **"Actions"**
3. Check: **"Send notifications for failed workflows only"**
4. Choose: **Email** or **Web + Mobile**

Now you'll get alerts if the monitoring script fails!

### Method 3: Using GitHub CLI (Advanced)

View workflow runs from terminal:

```bash
# View recent workflow runs
GH_HOST=github.com gh run list --repo yongjaidee/calendly-monitor

# Watch a specific run in real-time
GH_HOST=github.com gh run view --repo yongjaidee/calendly-monitor --log

# View latest run
GH_HOST=github.com gh run view --repo yongjaidee/calendly-monitor $(GH_HOST=github.com gh run list --repo yongjaidee/calendly-monitor --limit 1 --json databaseId --jq '.[0].databaseId')
```

### Method 4: GitHub Mobile App

1. Download **GitHub** app from App Store
2. Sign in with your personal account (yongjaidee)
3. Go to your repository
4. Tap **"Actions"** tab
5. See all runs and their status

## Understanding the Workflow Schedule

Your workflow runs **every 30 minutes** based on this schedule:

```yaml
on:
  schedule:
    - cron: '*/30 * * * *'  # Every 30 minutes
```

**Important Notes:**

1. **First run might be delayed** - GitHub Actions for scheduled workflows can be delayed by up to 15 minutes during high load
2. **Timezone**: Cron runs in UTC time
3. **Manual trigger**: You can also run it manually (see below)

## How to Manually Trigger a Test Run

### Via GitHub Website:

1. Go to: https://github.com/yongjaidee/calendly-monitor/actions
2. Click on **"Calendly Monitor"** workflow (left sidebar)
3. Click **"Run workflow"** dropdown (top right)
4. Click the green **"Run workflow"** button

### Via GitHub CLI:

```bash
GH_HOST=github.com gh workflow run monitor.yml --repo yongjaidee/calendly-monitor
```

## What to Look For in the Logs

When you view a workflow run, you'll see output like:

```
🔍 Calendly Monitor (FREE ntfy.sh) - 2025-10-22 14:30:00
📱 Topic: calendly-monitor-markzoril-2025
==============================================================

📅 Checking 2025-10...
❌ No slots found for 2025-10

📅 Checking 2025-11...
✅ Found 2 available slot(s): 2025-11-10, 2025-11-15

🔔 SLOTS AVAILABLE! Sending notification...
✅ Notification sent via ntfy.sh!
```

## Troubleshooting GitHub Actions

### Workflow isn't running?

**Check if it's enabled:**
1. Go to Actions tab
2. If you see "Workflows disabled" banner, click **"Enable workflows"**

**Check the workflow file:**
```bash
cd ~/git/yong/calendly-monitor
cat .github/workflows/monitor.yml
```

Should have:
```yaml
on:
  schedule:
    - cron: '*/30 * * * *'
  workflow_dispatch:  # Allows manual runs
```

### Workflow is failing?

**Common issues:**

1. **Missing dependencies:**
   - Check `calendly_requirements.txt` is in the repo
   - View the logs to see the error

2. **Python errors:**
   - Check the script runs locally first:
     ```bash
     cd ~/git/yong/calendly-monitor
     pip3 install -r calendly_requirements.txt
     python3 calendly_monitor.py
     ```

3. **Calendly blocking requests:**
   - GitHub Actions uses shared IPs that might be rate-limited
   - Check the logs for HTTP errors

### View detailed logs:

1. Click on the failed workflow run
2. Click on the **"monitor"** job
3. Expand **"Run monitor"** step
4. Read the error message

## Monitoring Best Practices

### 1. Check Status Periodically

Visit https://github.com/yongjaidee/calendly-monitor/actions once a day to ensure it's running smoothly.

### 2. Test the Notification System

Run a manual test:
```bash
cd ~/git/yong/calendly-monitor
python3 calendly_monitor.py
```

You should get a test notification on your phone (if you're subscribed to the ntfy topic).

### 3. Watch for GitHub Actions Limits

**Free tier limits:**
- ✅ 2,000 minutes/month for public repos
- ✅ Unlimited for public repos (actually free!)

Your workflow uses ~1-2 minutes per run:
- 48 runs/day × 30 days = 1,440 runs/month
- ~2 minutes each = ~2,880 minutes
- **Still well within limits for public repos!**

### 4. Set Up Email Notifications

Go to https://github.com/settings/notifications and enable:
- ✅ Actions: "Send notifications for failed workflows only"

## Quick Reference Commands

```bash
# View recent runs
GH_HOST=github.com gh run list --repo yongjaidee/calendly-monitor --limit 10

# Manually trigger workflow
GH_HOST=github.com gh workflow run monitor.yml --repo yongjaidee/calendly-monitor

# Watch latest run logs
GH_HOST=github.com gh run watch --repo yongjaidee/calendly-monitor

# Download logs from a specific run
GH_HOST=github.com gh run download RUN_ID --repo yongjaidee/calendly-monitor
```

## Testing Everything End-to-End

1. **Manually trigger a workflow run:**
   - https://github.com/yongjaidee/calendly-monitor/actions
   - Click "Run workflow"

2. **Watch the run in real-time:**
   - Click on the running workflow
   - Watch the logs appear

3. **Check your phone:**
   - You should get a notification via ntfy app
   - If slots are available, you'll see them listed

4. **Verify automatic scheduling:**
   - Wait 30 minutes
   - Check if a new run appears automatically

## Dashboard View

**Quick status check:**

Visit: https://github.com/yongjaidee/calendly-monitor

Look for:
- ✅ Green checkmark next to latest commit = last run succeeded
- ❌ Red X = last run failed
- 🟡 Yellow dot = run in progress

## Email Digest (Optional)

Set up weekly summaries:

1. Go to: https://github.com/settings/notifications
2. Scroll to **"Email notification preferences"**
3. Check: **"Include your own updates"**
4. Choose frequency: **Weekly**

## Mobile Monitoring

**GitHub Mobile App:**
- ✅ Push notifications for failed workflows
- ✅ View workflow runs on the go
- ✅ Read logs from your phone
- ✅ Manually trigger workflows

**Download:** Search "GitHub" in App Store

## What Success Looks Like

**Healthy workflow:**
- ✅ Runs every ~30 minutes
- ✅ Completes in 1-2 minutes
- ✅ Green checkmarks on all runs
- ✅ Notifications arriving on your phone when slots appear

**If you see failures:**
- Check the logs in the Actions tab
- Look for error messages
- Test the script locally
- Check if Calendly changed their website structure

## Next Steps

1. **Enable the workflow** (if not already enabled)
2. **Run a manual test** to verify it works
3. **Subscribe to the ntfy topic** on your iPhone
4. **Enable failure notifications** in GitHub settings
5. **Check back in 30 minutes** to see the first automatic run

---

**Repository:** https://github.com/yongjaidee/calendly-monitor
**Actions:** https://github.com/yongjaidee/calendly-monitor/actions
**Settings:** https://github.com/yongjaidee/calendly-monitor/settings
