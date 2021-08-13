import os
import telebot

from configparser import ConfigParser
from flask import Flask, request
from github import Github
from github.GithubException import UnknownObjectException


server = Flask(__name__)
env = os.getenv("ENV", "dev")

if env == "dev":
    config = ConfigParser()
    config.read(".config")
    config = config["BOT"]
else:
    config = {
        "BOT_TOKEN": os.getenv("BOT_TOKEN", "your_bot_token"),
        "GITHUB_TOKEN": os.getenv("GITHUB_TOKEN", "your_github_token"),
        "TELEGRAM_USER_ID": os.getenv("TELEGRAM_USER_ID", "42"),
        "GITHUB_REPO": os.getenv("GITHUB_REPO", "your_repo"),
        "HEROKU_URL": os.getenv("HEROKU_URL", "localhost:5000")
    }


bot = telebot.TeleBot(config["BOT_TOKEN"], parse_mode=None)


def set_up():
    github = Github(config["GITHUB_TOKEN"])
    repository = github.get_user().get_repo(config["GITHUB_REPO"])
    return repository


def format_pull_request_details(pr: str) -> str:
    return f"Título do PR: {pr.title}\nNúmero do PR:{pr.number}\n\n"


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Ola {message.from_user.first_name}')


@bot.message_handler(commands=['list_pulls'])
def list_pull_requests(message):
    bot.send_chat_action(message.chat.id, 'typing')

    if message.from_user.id != int(config["TELEGRAM_USER_ID"]):
        bot.send_message(message.chat.id, '🚨 Glu glu yeah yeah 🚨')
        return

    repository = set_up()
    pull_requests = repository.get_pulls().get_page(0)

    msg = str()
    for pull_request in pull_requests:
        msg = msg + format_pull_request_details(pull_request)

    bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=['merge'])
def merge_pull_request(message):
    bot.send_chat_action(message.chat.id, 'typing')

    if message.from_user.id != int(config["TELEGRAM_USER_ID"]):
        bot.send_message(message.chat.id, '🚨 Glu glu yeah yeah 🚨')
        return

    pull_id = message.text.strip('/merge ')

    if pull_id == '':
        bot.send_message(message.chat.id, '❌ Faltou o ID do pull request')
        return

    repository = set_up()

    try:
        repository.get_pull(int(pull_id)).merge()
    except UnknownObjectException:
        msg = f'❌ O merge falhou! Pull request #{pull_id} não encontrado'
        bot.send_message(message.chat.id, msg)
        return

    msg = f'✅ Merge do pull request #{pull_id} feito com sucesso!'

    bot.send_message(message.chat.id, msg)


@bot.message_handler(func=lambda m: True)
def ping(message):

    # Only reply to me
    if message.from_user.id != int(config["TELEGRAM_USER_ID"]):
        bot.send_message(message.chat.id, '🚨 Glu glu yeah yeah 🚨')
        return

    bot.send_message(message.chat.id, f' Olá {message.from_user.first_name}')


@server.post('/')
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@server.get("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=config["HEROKU_URL"])
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
