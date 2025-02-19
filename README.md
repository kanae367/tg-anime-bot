# Telegram Anime Bot

A Telegram bot that can give you information about an anime/manga or a specific character.

## Interaction with bot

1. Type /start to start conversation
2. Select needed option between anime/manga/character
3. Type the name of what you want to find

You can try it [here](https://t.me/anime367_bot)

## How to start

1. Clone the repository: `git clone https://github.com/kanae367/tg-anime-bot`
2. Install all dependencies: `pip install -r requirements.txt`
3. Open keys_public.env and replace 'yourtgbotkey' with your bot token then rename the file to keys.env
4. Run main.py

Or if you want to run bot on a server:

1.  `git clone https://github.com/kanae367/tg-anime-bot`
2.  `cd tg-anime-bot`
3.  `cp keys_public.env keys.env`
4.  Replace the API key inside keys.env with your key
5.  `docker build -t image_name .`
6.  `docker run -it -d --env-file keys.env --name image_name image_name`
