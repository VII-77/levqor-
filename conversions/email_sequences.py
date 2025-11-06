"""
Free-trial conversion email sequences and nudges
Sends automated emails based on user behavior and credit usage
"""

import os
import json
from datetime import datetime, timedelta
from time import time
import sqlite3

# Import notifier if available
try:
    from notifier import send_email
except ImportError:
    def send_email(to, subject, text, from_addr=None):
        print(f"MOCK EMAIL: To={to}, Subject={subject}")
        return True

def get_db():
    """Get database connection"""
    db = sqlite3.connect("data/levqor.db")
    db.row_factory = sqlite3.Row
    return db

def get_user_state(user_id):
    """Get user's current state for conversion tracking"""
    db = get_db()
    
    user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    if not user:
        return None
    
    days_since_signup = (time() - user['created_at']) / 86400
    credits_used = 50 - user['credits_remaining']
    has_purchased = user['credits_remaining'] != 50 or credits_used > 50
    
    return {
        'user_id': user_id,
        'email': user['email'],
        'name': user.get('name') or user['email'].split('@')[0],
        'days_since_signup': int(days_since_signup),
        'credits_remaining': user['credits_remaining'],
        'credits_used': credits_used,
        'has_purchased': has_purchased,
        'created_at': user['created_at']
    }

def get_email_history(user_id):
    """Get list of conversion emails already sent to user"""
    db = get_db()
    
    user = db.execute("SELECT meta FROM users WHERE id = ?", (user_id,)).fetchone()
    if not user or not user['meta']:
        return []
    
    try:
        meta = json.loads(user['meta'])
        return meta.get('conversion_emails', [])
    except:
        return []

def mark_email_sent(user_id, email_type):
    """Mark that a conversion email was sent"""
    db = get_db()
    
    user = db.execute("SELECT meta FROM users WHERE id = ?", (user_id,)).fetchone()
    meta = {}
    
    if user and user['meta']:
        try:
            meta = json.loads(user['meta'])
        except:
            pass
    
    if 'conversion_emails' not in meta:
        meta['conversion_emails'] = []
    
    meta['conversion_emails'].append({
        'type': email_type,
        'sent_at': time()
    })
    
    db.execute(
        "UPDATE users SET meta = ? WHERE id = ?",
        (json.dumps(meta), user_id)
    )
    db.commit()

def send_day_1_welcome(user_state):
    """Day 1: Welcome email with quick start guide"""
    subject = "Welcome to Levqor! Get started in 2 minutes ⚡"
    
    message = f"""Hi {user_state['name']}!

Thanks for signing up for Levqor. You've got 50 free credits to explore AI-powered automation.

🚀 Quick Start (takes 2 minutes):

1. Try our AI workflow builder:
   → Describe what you want to automate in plain English
   → Our AI generates the workflow for you
   → One-click deploy

2. Or browse pre-built templates:
   → Daily HN digest to Slack
   → Contact form to Notion + Slack
   → Weekly email summary

3. Connect your first integration:
   → Slack, Notion, Gmail, or Telegram
   → Takes 30 seconds with OAuth

Your dashboard: https://levqor.ai/dashboard
Template library: https://levqor.ai/builder

Questions? Just reply to this email.

Best,
The Levqor Team

P.S. Each automation costs 1 credit. You have {user_state['credits_remaining']} credits remaining.
"""
    
    try:
        send_email(
            to=user_state['email'],
            subject=subject,
            text=message,
            from_addr="onboarding@levqor.ai"
        )
        mark_email_sent(user_state['user_id'], 'day_1_welcome')
        return True
    except Exception as e:
        print(f"Failed to send day 1 email: {e}")
        return False

def send_day_3_usage_nudge(user_state):
    """Day 3: Encourage usage if credits haven't been used"""
    if user_state['credits_used'] > 10:
        return False  # Already active, skip
    
    subject = "You still have 50 free credits! Here's how to use them 💡"
    
    message = f"""Hi {user_state['name']},

I noticed you haven't used many of your free credits yet. Let me show you how easy it is:

🎯 3 Workflows You Can Build Right Now:

1. "Every morning at 9am, send top HN posts to my Slack"
   → Type this in the AI builder
   → Done in 30 seconds

2. "When someone fills my contact form, create a Notion task and notify me"
   → Use our Contact Form Handler template
   → Add your Notion database ID

3. "Summarize my important emails every Friday"
   → Email Digest template
   → Set your filter preferences

💡 Pro tip: Start with templates, then customize with AI.

Get started: https://levqor.ai/builder

Still have {user_state['credits_remaining']} credits to explore!

Best,
The Levqor Team
"""
    
    try:
        send_email(
            to=user_state['email'],
            subject=subject,
            text=message,
            from_addr="onboarding@levqor.ai"
        )
        mark_email_sent(user_state['user_id'], 'day_3_usage_nudge')
        return True
    except Exception as e:
        print(f"Failed to send day 3 email: {e}")
        return False

def send_day_7_conversion_push(user_state):
    """Day 7: Strong conversion push with social proof"""
    if user_state['has_purchased']:
        return False  # Already converted
    
    subject = "You're running low on credits (upgrade for just $9) 💳"
    
    credits_left = user_state['credits_remaining']
    credits_used = user_state['credits_used']
    
    message = f"""Hi {user_state['name']},

You've used {credits_used} of your 50 free credits - nice work! 🎉

You have {credits_left} credits left. Here's what happens next:

When you run out, upgrade to keep your automations running:
→ $9 for 100 credits (that's $0.09 per automation)
→ Credits never expire
→ No monthly subscription

📊 Why users love it:

"Saved me 5 hours per week automating email summaries and Slack updates" - Sarah K.

"Cheaper than Zapier and WAY easier to set up with AI" - Mike R.

"The template library is gold. Set up 3 workflows in 10 minutes" - Jessica L.

🎁 Limited time: Get 20% off your first credit pack with code EARLYBIRD

Upgrade now: https://levqor.ai/pricing

Questions? Just reply to this email.

Best,
The Levqor Team

P.S. Your automations pause when you hit 0 credits. Upgrade anytime to resume.
"""
    
    try:
        send_email(
            to=user_state['email'],
            subject=subject,
            text=message,
            from_addr="billing@levqor.ai"
        )
        mark_email_sent(user_state['user_id'], 'day_7_conversion_push')
        return True
    except Exception as e:
        print(f"Failed to send day 7 email: {e}")
        return False

def send_day_14_churn_prevention(user_state):
    """Day 14: Last chance conversion email"""
    if user_state['has_purchased']:
        return False
    
    if user_state['credits_used'] < 5:
        return False  # Not engaged enough
    
    subject = "Don't lose your workflows! (Special offer inside) 🎁"
    
    message = f"""Hi {user_state['name']},

I wanted to reach out personally. You set up some great automations, and I'd hate to see them stop working.

Here's where you're at:
→ {user_state['credits_remaining']} credits remaining
→ {user_state['credits_used']} automations run
→ Account active for {user_state['days_since_signup']} days

🎁 SPECIAL OFFER: 30% off your first credit pack
Use code KEEPGOING at checkout

That's 100 credits for just $6.30 (normally $9).

This offer expires in 48 hours.

Upgrade now: https://levqor.ai/pricing?code=KEEPGOING

Not ready yet? No problem. Your account stays active, automations just pause at 0 credits.

Want to chat? Book a 15-min call: https://cal.com/levqor

Best,
The Levqor Team
"""
    
    try:
        send_email(
            to=user_state['email'],
            subject=subject,
            text=message,
            from_addr="team@levqor.ai"
        )
        mark_email_sent(user_state['user_id'], 'day_14_churn_prevention')
        return True
    except Exception as e:
        print(f"Failed to send day 14 email: {e}")
        return False

def process_conversion_sequences():
    """Run daily to send appropriate conversion emails to users"""
    db = get_db()
    
    all_users = db.execute("""
        SELECT id FROM users 
        WHERE created_at > ?
        ORDER BY created_at DESC
    """, (time() - (30 * 86400),)).fetchall()  # Last 30 days
    
    results = {
        'day_1': 0,
        'day_3': 0,
        'day_7': 0,
        'day_14': 0,
        'skipped': 0
    }
    
    for user_row in all_users:
        user_state = get_user_state(user_row['id'])
        if not user_state:
            continue
        
        email_history = get_email_history(user_state['user_id'])
        sent_types = [e.get('type') for e in email_history]
        
        days = user_state['days_since_signup']
        
        # Day 1: Welcome
        if days >= 0 and 'day_1_welcome' not in sent_types:
            if send_day_1_welcome(user_state):
                results['day_1'] += 1
        
        # Day 3: Usage nudge
        elif days >= 3 and 'day_3_usage_nudge' not in sent_types:
            if send_day_3_usage_nudge(user_state):
                results['day_3'] += 1
        
        # Day 7: Conversion push
        elif days >= 7 and 'day_7_conversion_push' not in sent_types:
            if send_day_7_conversion_push(user_state):
                results['day_7'] += 1
        
        # Day 14: Churn prevention
        elif days >= 14 and 'day_14_churn_prevention' not in sent_types:
            if send_day_14_churn_prevention(user_state):
                results['day_14'] += 1
        
        else:
            results['skipped'] += 1
    
    print(f"Conversion email batch complete: {results}")
    return results

if __name__ == "__main__":
    results = process_conversion_sequences()
    print(json.dumps(results, indent=2))
