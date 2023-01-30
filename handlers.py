from loader import dp, bot
from aiogram import types
from aiogram.types import Message
from random import choice,randint
from data import start_sweets, one_move, game


@dp.message_handler(commands=['start'])
async def mes_start(message: types.Message):
    global game
    game = False
    await message.answer(f'Привет, {message.from_user.first_name}!!!\n\n'
                         f'Мои команды:\n\n /start\n /new_game\n /set \n/help')

@dp.message_handler(commands=['new_game'])
async def mes_new(message: types.Message):
    global start_sweets
    global one_move
    global game
    global total
    game = True

    total = start_sweets
    await bot.send_message(message.from_user.id, f'Началась новая игра.\nНа столе {total} конфет. '
                                                 f'За один ход можно взять не более {one_move}.\n\n  Выбираю очередность!\n'
                                                 f'----------------------------------------\n')
    first = message.from_user.first_name
    second = 'Bot'
    player = choice([first, second])
    await bot.send_message(message.from_user.id, f'Первым ходит {player}')

    if player == second:
        if total > one_move:
            await bot_takes_sweets(message)
    else:
        await player_takes_sweets(message)


@dp.message_handler(commands=['set'])
async def mes_set(message: types.Message):
    global start_sweets
    global game
    global total
    if len (message.text.split()) > 1:
        if int(message.text.split()[1]) > 28:
            count = message.text.split()[1]
            start_sweets = int(count)
            await message.answer(f'Установили новое количество конфет = {start_sweets}')
            total = start_sweets
            game = False
        else:
            await message.answer(f'Попробуй еще раз. Количество должно быть больше 28 штук.')
    else:
        await message.answer('Не указано количество конфет. Введите /set "количество конфет". Например: /set 500')

@dp.message_handler(commands=['help'])
async def mes_help(message: types.message):
    global game
    game = False
    await message.answer(f'Мои команды:\n\n /start\n /new_game\n /set \n/help')


async def bot_takes_sweets(message: Message):
    global total
    global one_move
    global game
    game = True

    if total > one_move:
        sweets = total % (one_move + 1)
        if sweets == 0: sweets = randint(1, one_move)
        total -= sweets
        await message.answer(f'Я взял {sweets} конфет. На столе осталось: {total}')
        await player_takes_sweets(message)
    else:
        await message.answer(f'Осталось {total} конфет, я их забираю. Я выйграл!!!')
        game = False

async def player_takes_sweets(message: Message):
    global total
    global one_move
    global game

    if total > one_move:
        await message.answer(f'{message.from_user.first_name}, ходи! Сколько берешь конфет?')
    else:
        await message.answer(f'Выйграл, {message.from_user.first_name}!!!')
        game = False

@dp.message_handler()
async def take_sweets(message:Message):
    global total
    global game
    if game:
        if message.text.isdigit():
            if 0 < int(message.text) < 29:
                total -= int(message.text)
                await bot.send_message(message.from_user.id, f'Осталось конфет - {total}')
                await bot_takes_sweets(message)
            else:
                await message.answer(f'{message.from_user.first_name}, неправильно ты взял!!! Можно брать от 1 до 28 конфет.')
        else:
            await bot.send_message(message.from_user.id, f'Всего {total} конфет. Введи число!\n '
                                                         f'Если хотите установить новое количество конфет, наберите, например: /set 500')