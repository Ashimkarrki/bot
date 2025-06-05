# news-pasa

**news-pasa** is a Telegram bot that scrapes an online news portal every 10 minutes, summarizes the latest news using **Gemini 2.5 Flash**, and broadcasts the summary to all subscribed users.

## 🤖 Bot Access
- [Click here to try the bot on Telegram](https://t.me/nepaliiiiiiiii_newsssss_bot)


## ✨ Features

- Scrapes news from a predefined source every 10 minutes
- Summarizes articles using Google Gemini 2.5 Flash
- Automatically sends news summaries to all users who activated the bot
- Uses Redis to store and manage scraped data efficiently

## 💬 Telegram Bot Commands

- `/start` – Subscribes you to news broadcasts
- `/cancel` – Unsubscribes you from further broadcasts
- `/help` – Shows help and usage instructions

## 🚀 Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Ashimkarrki/bot.git
   cd news-pasa
   ```
2. **Set Up Environment Variables**
   
   Create a .env file in the root directory with the following content
   ```bash
    BOT_TOKEN="your-telegram-bot-token-from-botfather"
    GEMINI_API="your-gemini-api-key-from-google-ai-studio"
    DEV_HOST="localhost"  # Use if testing locally (requires Redis installed on host)
    PROD_HOST="redis"     # Use this when running inside Docker

   ```
4. **Run Docker**
   ```bash
   docker compose up 
   ```
5. **Initialize the Scraper**
   
   After containers are running, open a shell inside the Python container:
   ```bash
   docker exec -it <python_container_id> sh
   python3 extractLinks.py initial
   ```
   This prevents scraping of all existing news on the first run and sets a baseline for tracking new news.
   
## 📝 Logs

To view the cron job logs

```bash
docker exec -it <python_container_id> sh
cat /var/log/cron.log
```

## ⚙️ Tech Stack
Python – Core bot logic and scraping

Scrapy – For structured and efficient web scraping

Crontab – Schedules scraping every 10 minutes (modifiable via crontab file)

Redis – Lightweight key-value store for deduplication and user management

Docker – Containerized deployment and environment isolation


