import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (ApplicationBuilder, CommandHandler, ContextTypes,
                          MessageHandler, filters)
from groq import Groq
from openai import OpenAI
from asknews_sdk import AskNewsSDK

load_dotenv()

TELEGRAM_API_TOKEN=os.getenv("TELEGRAM_API_TOKEN")
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
GROQ_API_KEY=os.getenv("GROQ_API_KEY")
ASKNEWS_CLIENT_ID=os.getenv("ASKNEWS_CLIENT_ID")
ASKNEWS_CLIENT_SECRET=os.getenv("ASKNEWS_CLIENT_SECRET")
GROQ_GPT_MODEL = "llama-3.3-70b-versatile"
OPENAI_GPT_MODEL = "gpt-4o"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

openai_client = OpenAI()

groq_client = Groq(
    api_key=os.environ.get(GROQ_API_KEY),
)

ask = AskNewsSDK(
        client_id=ASKNEWS_CLIENT_ID,
        client_secret=ASKNEWS_CLIENT_SECRET,
        scopes=["news"]
)

async def chat_completion_request(messages):
    #print(messages)
    try:
        response = groq_client.chat.completions.create(
            model=GROQ_GPT_MODEL,
            messages=messages,
            max_tokens=250
        )
        #print("Groq: " + str(response))
        return response.choices[0].message.content
    except:
        #print("Unable to generate ChatCompletion response")
        #print(f"Exception: {e}")
        response = openai_client.chat.completions.create(
           model=OPENAI_GPT_MODEL,
           messages=messages,
           max_tokens=250,
           temperature=0.3
        )
        #print("OpenAI: " + str(response))
        return response.choices[0].message.content


async def reply(text):
    context = ""
    match = text
    messages = []
    messages.append({"role": "system", "content": "You are the worlds best AI Sports Handicapper and sportswriter. You are smart, funny and accurate."})
    messages.append({"role": "user", "content": match})
    try:
      #newsArticles = ask.news.search_news("best prop bets for the text " + match, method='kw', return_type='dicts', n_articles=3, categories=["Sports"], premium=True, start_timestamp=int(start), end_timestamp=int(end)).as_dicts
      newsArticles = ask.news.search_news("best bet for the following matchup " + match, method='kw', return_type='dicts', n_articles=3, hours_back=24, categories=["Sports"], premium=True).as_dicts
      context = ""
      for article in newsArticles:
        context += article.summary
      #print(context)
    except:
      context = ""
    messages.append({"role": "user", "content": "Write a brief outlining following matchup. List the odds and probability.  Give your best bet based on the context provided only mention bets and odds that are referenced in the context. " + context + " " + match})
    reply = await chat_completion_request(messages)
    return reply

async def replyTopNews(text):
    context = ""
    league = text
    messages = []
    messages.append({"role": "system", "content": "You are the worlds best AI Sports Handicapper and sportswriter. You are smart, funny and accurate."})
    messages.append({"role": "user", "content": league})
    try:
      #newsArticles = ask.news.search_news("best prop bets for the text " + match, method='kw', return_type='dicts', n_articles=3, categories=["Sports"], premium=True, start_timestamp=int(start), end_timestamp=int(end)).as_dicts
      newsArticles = ask.news.search_news("top news" + league, method='kw', return_type='dicts', n_articles=3, categories=["Sports"], hours_back=1, premium=True).as_dicts
      context = ""
      for article in newsArticles:
        context += article.summary
      #print(context)
    except:
      context = ""
    messages.append({"role": "user", "content": "Write a brief outlining the following articles. Only mention teams, players or stats referenced in the context. " + context + " " + league})
    reply = await chat_completion_request(messages)
    return reply

async def replyRecap(text):
    context = ""
    game = text
    messages = []
    messages.append({"role": "system", "content": "You are the worlds best AI Sports Handicapper and sportswriter. You are smart, funny and accurate."})
    messages.append({"role": "user", "content": game})
    try:
      #newsArticles = ask.news.search_news("best prop bets for the text " + match, method='kw', return_type='dicts', n_articles=3, categories=["Sports"], premium=True, start_timestamp=int(start), end_timestamp=int(end)).as_dicts
      newsArticles = ask.news.search_news("recap" + game, method='kw', return_type='dicts', n_articles=3, categories=["Sports"], hours_back=47, premium=True).as_dicts
      context = ""
      for article in newsArticles:
        context += article.summary
      #print(context)
    except:
      context = ""
    messages.append({"role": "user", "content": "Write a brief outlining the following articles. Only mention teams, players or stats referenced in the context. " + context + " " + league})
    reply = await chat_completion_request(messages)
    return reply

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def prediction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
    response = await reply(update.message.text)
    response = response + "\n\nBetUS - 125% Sign Up Bonus! - https://record.revmasters.com/_8ejz3pKmFDsdHrf4TDP9mWNd7ZgqdRLk/1/"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)

async def topnews(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
    response = await replyTopNews(update.message.text)
    response = response + "\n\nBetUS - 125% Sign Up Bonus! - https://record.revmasters.com/_8ejz3pKmFDsdHrf4TDP9mWNd7ZgqdRLk/1/"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)

async def recap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
    response = await replyRecap(update.message.text)
    response = response + "\n\nBetUS - 125% Sign Up Bonus! - https://record.revmasters.com/_8ejz3pKmFDsdHrf4TDP9mWNd7ZgqdRLk/1/"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)


if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_API_TOKEN).build()

    start_handler = CommandHandler('start', start)
    prediction_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), prediction)
    topnews_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), topnews)
    recap_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), recap)
    application.add_handler(start_handler)
    application.add_handler(prediction_handler)
    application.add_handler(topnews_handler)
    application.add_handler(recap_handler)

    application.run_polling()