import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Function to fetch latest blog data
def fetch_latest_blog_from_api():
    url = "https://api-web.eventure.com.my/blog"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        latest_blog = data['items'][0]  # assuming the latest blog is the first item
        return latest_blog
    return None

# Telegram bot command to show latest blog
def latest_blog(update: Update, context: CallbackContext) -> None:
    latest_blog_data = fetch_latest_blog_from_api()
    if latest_blog_data:
        blog_url = f"https://www.eventure.com.my/blog/{latest_blog_data['slug']}"
        update.message.reply_text(f"Title: {latest_blog_data['title']}\n\n"
                                  f"{latest_blog_data['short_description']}\n\n"
                                  f"Read More: {blog_url}\n")
    else:
        update.message.reply_text("Could not fetch the latest blog.")

# Function to fetch articles by tag
def fetch_article_by_tag(tag):
    url = "https://api-web.eventure.com.my/blog"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        articles_with_tag = [article for article in data['items'] if any(tag.upper() == t['title'].upper() for t in article['tags'])]

        if articles_with_tag:
            return articles_with_tag[0]  # return the latest one, assuming the list is sorted by date
    return None

def article_by_tag(update: Update, context: CallbackContext) -> None:
    tag = ' '.join(context.args)
    print("Searching for tag:", tag)
    article_data = fetch_article_by_tag(tag)
    if article_data:
        blog_url = f"https://www.eventure.com.my/blog/{article_data['slug']}"
        update.message.reply_text(f"Title: {article_data['title']}\n\n"
                                  f"{article_data['short_description']}\n\n"
                                  f"Read More: {blog_url}\n")
    else:
        update.message.reply_text(f"Could not fetch articles for tag: {tag}")


# Function to fetch latest 3 articles by stock code
def fetch_latest_articles_by_stock_code(stock_code):
    url = f"https://api-web.eventure.com.my/blog"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        articles_with_stock_code = [article for article in data['items'] if
                                    any(stock_code == stock['code'] for stock in article['stocks'])]

        # Sort the articles by created_at date and take the latest 3
        articles_with_stock_code.sort(key=lambda x: x['created_at'], reverse=True)
        return articles_with_stock_code[:3]
    return None


# Telegram bot command to show latest 3 articles by stock code
def article_by_stock_code(update: Update, context: CallbackContext) -> None:
    stock_code = ' '.join(context.args)
    print(f"Searching for stock code: {stock_code}")

    article_data_list = fetch_latest_articles_by_stock_code(stock_code)

    if article_data_list:
        for article_data in article_data_list:
            blog_url = f"https://www.eventure.com.my/blog/{article_data['slug']}"
            update.message.reply_text(f"Title: {article_data['title']}\n\n"
                                      f"{article_data['short_description']}\n\n"
                                      f"Read More: {blog_url}\n")
    else:
        update.message.reply_text(f"Could not fetch articles for stock code: {stock_code}")


# Function to fetch latest 3 articles by stock name
def fetch_latest_articles_by_stock_name(stock_name):
    url = f"https://api-web.eventure.com.my/blog"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        articles_with_stock_name = [article for article in data['items'] if
                                    any(stock_name.upper() == stock['name'].upper() for stock in article['stocks'])]

        # Sort the articles by created_at date and take the latest 3
        articles_with_stock_name.sort(key=lambda x: x['created_at'], reverse=True)
        return articles_with_stock_name[:3]
    return None

# Telegram bot command to show latest 3 articles by stock name
def article_by_stock_name(update: Update, context: CallbackContext) -> None:
    stock_name = ' '.join(context.args)
    print(f"Searching for stock name: {stock_name}")

    article_data_list = fetch_latest_articles_by_stock_name(stock_name)

    if article_data_list:
        for article_data in article_data_list:
            blog_url = f"https://www.eventure.com.my/blog/{article_data['slug']}"
            update.message.reply_text(f"Title: {article_data['title']}\n\n"
                                      f"{article_data['short_description']}\n\n"
                                      f"Read More: {blog_url}\n")
    else:
        update.message.reply_text(f"Could not fetch articles for stock name: {stock_name}")

# Initialize the Updater
updater = Updater("6499192108:AAFp7cEPKfk-PxrsuP7Iuu9zXtgvObHZTHY", use_context=True)

# Get the dispatcher to register handlers
dp = updater.dispatcher

# Add command handlers
dp.add_handler(CommandHandler('latest_blog', latest_blog))
dp.add_handler(CommandHandler('tag', article_by_tag))
dp.add_handler(CommandHandler('stock_code', article_by_stock_code))
dp.add_handler(CommandHandler('stock_name', article_by_stock_name))  # new command handler# new command handler

# Run the bot until the user sends a signal with Ctrl-C
updater.start_polling()
updater.idle()
