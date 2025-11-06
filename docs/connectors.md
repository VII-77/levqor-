# Connectors Guide

Levqor provides pre-built connectors for popular external services. All connectors use a unified `run_task()` interface.

## Available Connectors

- **Gmail** - Google API Python Client
- **Notion** - Notion API
- **Slack** - Slack SDK
- **Telegram** - Telegram Bot API

## Usage

### Endpoint

```
POST /api/v1/connect/{connector_name}
```

**Authentication:** Required (X-Api-Key header)

### Request Format

All connectors accept:

```json
{
  "action": "action_name",
  "token": "api_token_or_credentials",
  "params": {
    "param1": "value1"
  }
}
```

---

## Gmail Connector

Uses Google OAuth2 for authentication.

### Actions

#### `list_labels`
List all Gmail labels.

**Request:**
```json
{
  "action": "list_labels",
  "credentials": {
    "token": "ya29...",
    "refresh_token": "1//...",
    "client_id": "xxx.apps.googleusercontent.com",
    "client_secret": "..."
  },
  "params": {}
}
```

**Response:**
```json
{
  "status": "ok",
  "connector": "gmail",
  "result": {
    "labels": ["INBOX", "SENT", "DRAFTS", "SPAM"]
  }
}
```

#### `list_messages`
List recent messages.

**Params:**
- `max_results` (int): Maximum messages to retrieve (default: 10)
- `query` (string): Gmail search query

#### `send_email`
Send an email.

**Params:**
- `to` (string, required): Recipient email
- `subject` (string, required): Email subject
- `body` (string): Email body

---

## Notion Connector

Uses Notion integration tokens.

### Actions

#### `search`
Search Notion pages.

**Request:**
```json
{
  "action": "search",
  "token": "secret_...",
  "params": {
    "query": "Meeting Notes"
  }
}
```

**Response:**
```json
{
  "status": "ok",
  "connector": "notion",
  "result": {
    "count": 5,
    "pages": [...]
  }
}
```

#### `query_database`
Query a Notion database.

**Params:**
- `database_id` (string, required): Database ID
- `page_size` (int): Results per page (default: 10)

#### `create_page`
Create a new page.

**Params:**
- `database_id` (string, required): Parent database
- `properties` (object, required): Page properties

---

## Slack Connector

Uses Slack bot tokens.

### Actions

#### `post_message`
Post a message to a channel.

**Request:**
```json
{
  "action": "post_message",
  "token": "xoxb-...",
  "params": {
    "channel": "#general",
    "text": "Hello from Levqor!"
  }
}
```

**Response:**
```json
{
  "status": "ok",
  "connector": "slack",
  "result": {
    "message_ts": "1699276800.123456",
    "channel": "C01234567",
    "status": "sent"
  }
}
```

#### `list_channels`
List available channels.

**Params:**
- `limit` (int): Maximum channels (default: 100)

#### `upload_file`
Upload a file to Slack.

**Params:**
- `channel` (string, required): Target channel
- `content` (string, required): File content
- `filename` (string): File name (default: "file.txt")

---

## Telegram Connector

Uses Telegram bot tokens.

### Actions

#### `send_message`
Send a message to a chat.

**Request:**
```json
{
  "action": "send_message",
  "token": "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz",
  "params": {
    "chat_id": "123456789",
    "text": "Hello from Levqor!"
  }
}
```

**Response:**
```json
{
  "status": "ok",
  "connector": "telegram",
  "result": {
    "message_id": 42,
    "chat_id": 123456789,
    "status": "sent"
  }
}
```

#### `get_me`
Get bot information.

**Params:** None

#### `get_updates`
Get pending updates.

**Params:**
- `limit` (int): Maximum updates (default: 10)

---

## Error Handling

All connectors return errors in this format:

```json
{
  "error": "error_description"
}
```

**Common errors:**
- `action required` - Missing action parameter
- `token required` - Missing authentication token
- `unknown action: xyz` - Invalid action name
- `connector_error: ...` - Execution failure

---

## Best Practices

1. **Credentials**: Store API tokens securely in environment variables
2. **Error Handling**: Always check for `error` field in responses
3. **Rate Limits**: Respect external API rate limits
4. **Retries**: Implement exponential backoff for transient failures
5. **Timeouts**: Set reasonable timeouts for connector requests

---

## Getting Credentials

### Gmail
1. Create Google Cloud project
2. Enable Gmail API
3. Create OAuth 2.0 credentials
4. Authorize and obtain tokens

### Notion
1. Create Notion integration at [notion.so/my-integrations](https://notion.so/my-integrations)
2. Copy integration token
3. Share databases with integration

### Slack
1. Create Slack app at [api.slack.com/apps](https://api.slack.com/apps)
2. Enable bot token scopes
3. Install app to workspace
4. Copy bot token (starts with `xoxb-`)

### Telegram
1. Message [@BotFather](https://t.me/botfather)
2. Create new bot with `/newbot`
3. Copy HTTP API token

---

## Support

Questions? Email: support@levqor.ai
