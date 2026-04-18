# .env.tpl — safe to commit
# Runtime: op run --env-file=.env.tpl -- <your command>
# Secrets stored in op://Agents2/frasier-env/<KEY>

# Supabase
SUPABASE_URL=https://juaekekwvcuyeleyvrvc.supabase.co
SUPABASE_SERVICE_KEY="op://Agents2/frasier-env/SUPABASE_SERVICE_KEY"

# Discord
DISCORD_BOT_TOKEN="op://Agents2/frasier-env/DISCORD_BOT_TOKEN"
DISCORD_ZERO_ID=771845444241981440
EXECUTIVE_CHANNEL_ID=
UPDATES_CHANNEL_ID=

# OpenRouter
OPENROUTER_API_KEY="op://Agents2/frasier-env/OPENROUTER_API_KEY"

# Manus API
MANUS_API_KEY="op://Agents2/frasier-env/MANUS_API_KEY"
MANUS_API_URL=

# Gmail SMTP (for alerts)
GMAIL_USER=extebarrri@gmail.com
GMAIL_APP_PASSWORD="op://Agents2/frasier-env/GMAIL_APP_PASSWORD"
ALERT_EMAIL=drew@epyon.capital

# GitHub (daily state push at 4am ET)
GITHUB_TOKEN="op://Agents2/frasier-env/GITHUB_TOKEN"
GITHUB_REPO=dhroovmehta/voxyz-agent-world

# Notion
NOTION_API_KEY="op://Agents2/frasier-env/NOTION_API_KEY"

# Google Drive (Workspace impersonation)
GOOGLE_IMPERSONATE_EMAIL=drew@epyon.capital
GOOGLE_DRIVE_ROOT_FOLDER_ID=1d4oa72wK4_yu0RMbqE9X0EX_zKjEBhRC
# Brave Search API (primary web search — structured JSON, 2000 free queries/month)
BRAVE_API_KEY="op://Agents2/frasier-env/BRAVE_API_KEY"

GOOGLE_SERVICE_ACCOUNT_KEY="op://Agents2/frasier-env/GOOGLE_SERVICE_ACCOUNT_KEY"
