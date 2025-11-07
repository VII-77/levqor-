# Get Your Telegram Chat ID (30 seconds)

## Method 1: Quick Way (Easiest)

1. **Send a message** to your bot in Telegram (any message like "hello")

2. **Open this URL** in your browser (replace `YOUR_BOT_TOKEN` with your actual token):
   ```
   https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates
   ```

3. **Find your chat ID** in the response - look for:
   ```json
   "chat": {
     "id": 123456789,
     ...
   }
   ```

4. **Copy that number** (e.g., `123456789`)

5. **Add to Replit Secrets**:
   - Key: `TELEGRAM_CHAT_ID_DEFAULT`
   - Value: Your chat ID number

✅ Done!

---

## Method 2: Use a Bot

1. In Telegram, message: **@userinfobot**
2. It will reply with your user ID
3. Use that as your chat ID

---

## Test After Adding

```bash
# This will work now (uses default chat ID)
curl -X POST http://localhost:5000/actions/telegram.send \
  -H "Content-Type: application/json" \
  -d '{"text":"✅ Telegram working with default chat ID!"}'

# Or specify chat_id in request
curl -X POST http://localhost:5000/actions/telegram.send \
  -H "Content-Type: application/json" \
  -d '{"text":"Test","chat_id":"YOUR_CHAT_ID"}'
```
