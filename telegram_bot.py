from aiogram import Bot, Dispatcher, executor, types
from db_csv_manager import DBManager
from articles_queue import ArticlesQueue
from work_with_static_api import draw_map
from telegram_token import TOKEN  # токен скрыт в целях безопасности

START_TEXT = "Привет. Я бот, который может найти ближайшие к вам достопримечательности. Для этого скиньте мне свою геопозицию. Используйте команду /help, если возникнут вопросы"
HELP_TEXT = """Для работы бота необходимо скинуть ему свою геопозицию. Для этого нажмите на значок скрепки (рядом с микрофоном) и выберете геопозицию.
Если хотите сменить геопозицию - просто пришлите новую аналогичным способом.

/next - перейти к следующей достопримечательности
/prev - перейти к предыдущей достопримечательности
/top_5 - выдать список из 5 ближайших к вам достопримечательностей
/show_map - показать текущую достопримечательность на карте (или 5 ближайших, если выбран /top_5)
/help - помощь"""

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

db_manager = DBManager('attractions_list.csv')

users_queue = dict()


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, START_TEXT)


@dp.message_handler(commands=["help"])
async def bot_help(message: types.Message):
    await bot.send_message(message.from_user.id, HELP_TEXT)


@dp.message_handler(content_types=["location"])
async def get_location(message: types.Message):
    result_list = db_manager.sort_by_distance(message.location.latitude, message.location.longitude)
    users_queue[message.from_user.id] = ArticlesQueue(result_list, message.location.latitude,
                                                      message.location.longitude)
    element = users_queue[message.from_user.id].get_current_element()
    distance = round(element['dist'] * 1000.0)
    article_name = element['title']
    article_url = element['url'].replace('"', '&apos;')
    await bot.send_message(message.from_user.id,
                           f'<a href="{article_url}">{article_name}</a>' + '\n' + f'{str(distance)} метров от вас',
                           parse_mode=types.ParseMode.HTML)


@dp.message_handler(commands=["next"])
async def get_next(message: types.Message):
    if message.from_user.id not in users_queue:
        await bot.send_message(message.from_user.id, "Вы не дали свою геопозицию")
    elif users_queue[message.from_user.id].is_last():
        await bot.send_message(message.from_user.id, "Это последний известный мне объект")
    else:
        element = users_queue[message.from_user.id].next_element()
        distance = round(element['dist'] * 1000.0)
        article_name = element['title']
        article_url = element['url'].replace('"', '&apos;')
        await bot.send_message(message.from_user.id,
                               f'<a href="{article_url}">{article_name}</a>' + '\n' + f'{str(distance)} метров от вас',
                               parse_mode=types.ParseMode.HTML)


@dp.message_handler(commands=["prev"])
async def get_prev(message: types.Message):
    if message.from_user.id not in users_queue:
        await bot.send_message(message.from_user.id, "Вы не дали свою геопозицию")
    elif users_queue[message.from_user.id].is_first():
        await bot.send_message(message.from_user.id, "Перед этим объектом в списке ничего нет")
    else:
        element = users_queue[message.from_user.id].prev_element()
        distance = round(element['dist'] * 1000.0)
        article_name = element['title']
        article_url = element['url'].replace('"', '&apos;')
        await bot.send_message(message.from_user.id,
                               f'<a href="{article_url}">{article_name}</a>' + '\n' + f'{str(distance)} метров от вас',
                               parse_mode=types.ParseMode.HTML)


@dp.message_handler(commands=["top_5"])
async def top_5(message: types.Message):
    if message.from_user.id not in users_queue:
        await bot.send_message(message.from_user.id, "Вы не дали свою геопозицию")
    else:
        articles_list = []
        for element in users_queue[message.from_user.id].get_top_articles(5):
            distance = round(element['dist'] * 1000.0)
            article_name = element['title']
            article_url = element['url'].replace('"', '&apos;')
            articles_list.append(
                f'<a href="{article_url}">{article_name}</a>' + ' - ' + f'{str(distance)} метров от вас'
            )
        await bot.send_message(message.from_user.id, '\n'.join(articles_list), parse_mode=types.ParseMode.HTML)


@dp.message_handler(commands=["show_map"])
async def show_map(message: types.Message):
    if message.from_user.id not in users_queue:
        await bot.send_message(message.from_user.id, "Вы не дали свою геопозицию")
    elif users_queue[message.from_user.id].is_top_last():
        articles_cords = []
        for element in users_queue[message.from_user.id].get_top_articles(5):
            articles_cords.append((element['latitude'], element['longitude']))
        photo = draw_map(users_queue[message.from_user.id].get_user_cords(), *articles_cords)
        await bot.send_photo(message.from_user.id, photo)
    else:
        element = users_queue[message.from_user.id].get_current_element()
        photo = draw_map(users_queue[message.from_user.id].get_user_cords(),
                         (element['latitude'], element['longitude']))
        await bot.send_photo(message.from_user.id, photo)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
