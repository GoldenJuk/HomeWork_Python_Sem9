from aiogram import Bot, Dispatcher

import os

bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot)    # Это диспетчер. Он отвечает за те сообщения,
                        # которые отлавливает. У диспатчера есть мрного хендлеров.
