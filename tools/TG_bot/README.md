# Telegram bot with AI to predict type of unknown functions


This Telegram bot will extract the binary content of an bin given file in ELF format and predict it's functions destination.

## Usage

1. Create a Telegram bot with [BotFather](https://t.me/botfather)
2. Run the bot locally or deploy with Docker
3. Send a binary file you want to predict to the bot
4. Receive predictions!

## How to run

### Environment variables

1. `BOT_TOKEN` - Telegram bot token. Get it by creating in [@BotFather](https://t.me/BotFather)
2. `MODEL_NAME` -  model name (options: `DecisionTree`, `LGBMClassifier`, `RandomForest`, `XGBClassifier` or `StackingClassifier` ). By default `XGBClassifier`
3. `LOG_LEVEL` - Logging level (options: "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"). By default "INFO"
4. `FROM_DOCKER` - If the app is running in Docker (options: 1, 0). By default 0
5. Additional settings in [settings](./bot/settings.py)

### Run locally

Clone the repo

```shell
git clone
cd ./WhatDoesThisFuncDo
export BOT_TOKEN=<YOUR_TOKEN>
python -m venv venv
source venv/bin/activate
pip install -r ./tools/TG_bot/requirements.txt
pip install -e ./tools/TG_bot/.
```

Run tests 

```shell
pytest ./tools/TG_bot/bot/
```

Run the bot

```shell
python ./tools/TG_bot/bot/bot.py
```

Send to your Telegram bot a ELF file and get predictions!

### Run with Docker

It works on Alpine.

```shell
docker build -f ./tools/TG_bot/Dockerfile -t elf_bot:latest ./tools/TG_bot/ 
docker run --rm --init -it --name elf_bot \
  --env BOT_TOKEN2="<YOUR_TOKEN>" \
  --env FROM_DOCKER=1 \
  elf_bot:latest
```