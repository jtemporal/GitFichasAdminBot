# GitFichasAdminBot

This is the way.

## Running

```console
gunicorn main:server
```

## Set up

This bot was structured to be deployed to Heroku below you'll find the instructions for setting up everything you'll need for running your bot. 😉

### Development

Create an Python environment and install the dependencies:

```console
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
```

Then create your `.config` file by copying the example file and updating the values accordingly:

```console
cp .example.config .config
```

Here's a list of the variables in the `.config` file and what they mean:

```text
BOT_TOKEN         -> The Telegram bot token that you get from bot father
GITHUB_TOKEN      -> The GitHub personal access Token
TELEGRAM_USER_ID  -> Your user ID on Telegram
GITHUB_REPO       -> The repo on GitHub
HEROKU_URL        -> The app URL from the "Domains" section on settings
```

Here's some help for getting all those tokens:

1. [Go here to get an GitHub personal access token](https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token).
1. [Use the BotFather to enroll your bot and get a Telegram bot token](https://core.telegram.org/bots#3-how-do-i-create-a-bot).
1. While in development you'll won't need a Heroku URL so leave that as the provided value in the example file.

Then to run your server:

```console
gunicorn main:server
```

Access [localhost](http://localhost:8000) on your favorite browser, you'll see some worker timeouts in development but don't worry about that, that's because we are using webhooks for production and start a bot polling in development.

### Production

Login to your Heroku account and [create a new app](https://dashboard.heroku.com/new-app), follow the steps on the "Deploy" tab to deploy it (install the Heroku CLI, login to Heroku via CLI, push your code to Heroku), then navigate to the "Settings" tab.

For safety you don't want to commit the `.config` file, so to deploy this to Heroku you'll need to create the environment variables on the Heroku app settings.

Under "Config Vars" section click "Reveal Config Vars" button, then you'll be able to add variables. You can use the `.config` file as example for what variables you'll need and you'll also need an `ENV` variable set to `prod`.

While in the Settings tab, refer to the "Domains" section to grab the Heroku URL

Here's a list of all the variables you must set on Heroku and the descriptions:

```text
BOT_TOKEN         -> The Telegram bot token that you get from bot father
GITHUB_TOKEN      -> The GitHub personal access Token
TELEGRAM_USER_ID  -> Your user ID on Telegram
GITHUB_REPO       -> The repo on GitHub
HEROKU_URL        -> The app URL from the "Domains" section on settings
ENV               -> Environment, set it to something like `prod` or `production`
```
