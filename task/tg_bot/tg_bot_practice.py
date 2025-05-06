import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ForceReply
import json
import time
import asyncio
import os
import random
import sys
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не найден в файле .env")

# Инициализация бота
bot = telebot.TeleBot(TOKEN)

# Путь к файлу players.json (относительный)
PLAYERS_FILE = os.path.join(os.path.dirname(__file__), 'players.json')

# Путь к папке с изображениями кубиков (относительный)
DICE_DIR = os.path.join(os.path.dirname(__file__), 'dice')

# Загрузка данных игроков
def load_players():
    try:
        with open(PLAYERS_FILE, 'r') as f:
            data = json.load(f)
            # Валидация и конвертация coins в int
            for player in data.values():
                if not isinstance(player, dict):
                    print(f"DEBUG: Некорректные данные игрока: {player}")
                    return {}
                player['coins'] = int(player.get('coins', 0))
                player['click_power'] = int(player.get('click_power', 1))
                player['autoclick'] = int(player.get('autoclick', 0))
                player['total_clicks'] = int(player.get('total_clicks', 0))
            print(f"DEBUG: Загружено из {PLAYERS_FILE}, игроков: {len(data)}")
            return data
    except FileNotFoundError:
        print(f"DEBUG: Файл {PLAYERS_FILE} не найден")
        return {}
    except json.JSONDecodeError as e:
        print(f"DEBUG: Ошибка формата JSON в {PLAYERS_FILE}: {e}")
        return {}
    except Exception as e:
        print(f"DEBUG: Ошибка загрузки {PLAYERS_FILE}: {e}")
        return {}

# Сохранение данных игроков
def save_players(players):
    try:
        # Валидация перед сохранением
        for user_id, player in players.items():
            if not isinstance(player, dict):
                print(f"DEBUG: Некорректные данные для игрока {user_id}: {player}")
                return
            player['coins'] = int(player.get('coins', 0))
        with open(PLAYERS_FILE, 'w') as f:
            json.dump(players, f, indent=4)
        print(f"DEBUG: Сохранено в {PLAYERS_FILE}, игроков: {len(players)}")
    except Exception as e:
        print(f"DEBUG: Ошибка сохранения {PLAYERS_FILE}: {e}")

# Инициализация игрока
def init_player_temp(user_id, username):
    return {
        'username': username or f"Player_{user_id}",
        'coins': 0,
        'click_power': 1,
        'autoclick': 0,
        'total_clicks': 0,
        'last_update': int(time.time()),
        'telegram_id': user_id
    }

# Сохранение игрока
def save_player(user_id, player_data):
    players = load_players()
    players[user_id] = player_data
    save_players(players)

# Обновление автоклика
def update_autoclick(player):
    current_time = int(time.time())
    seconds_passed = current_time - player['last_update']
    autoclick_coins = int(player['autoclick'] * seconds_passed)
    player['coins'] = int(player['coins'] + autoclick_coins)
    player['last_update'] = current_time
    print(f"DEBUG: Автоклик для {player['telegram_id']}, секунд прошло: {seconds_passed}, начислено: {autoclick_coins} монет")
    return autoclick_coins

# Клавиатура с командами
def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(KeyboardButton("Клик💰"))
    keyboard.row(KeyboardButton("Магазин🏪"), KeyboardButton("Испытать удачу🎲"))
    keyboard.row(KeyboardButton("Профиль📱"), KeyboardButton("Рейтинг👑"))
    return keyboard

# Inline-кнопки для профиля
def get_profile_buttons():
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("Изменить никнейм⚙️", callback_data="change_nickname"))
    markup.row(InlineKeyboardButton("Help❓", callback_data="show_help"))
    return markup

# Inline-кнопки для магазина
def get_shop_keyboard(user_id):
    players = load_players()
    player = players.get(user_id, {'coins': 0, 'click_power': 1, 'autoclick': 0})
    markup = InlineKeyboardMarkup()
    click_cost = 50 * (player['click_power'] ** 2)
    autoclick_cost = 100 * ((player['autoclick'] + 1) ** 2)
    markup.add(InlineKeyboardButton(f"Улучшить клик (+1 за {click_cost} монет)", callback_data="buy_click"))
    markup.add(InlineKeyboardButton(f"Автоклик (+1/с за {autoclick_cost} монет)", callback_data="buy_autoclick"))
    return markup

# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = str(message.from_user.id)
    username = message.from_user.username or message.from_user.first_name
    players = load_players()
    if user_id not in players:
        bot.reply_to(message, "Добро пожаловать в кликер! Введи свой никнейм:", reply_markup=ForceReply())
        bot.register_next_step_handler(message, handle_nickname, user_id, username)
    else:
        bot.reply_to(message, "С возвращением! Жми 'Клик💰', чтобы зарабатывать монеты!", reply_markup=get_main_keyboard())

# Обработка никнейма
def handle_nickname(message, user_id, default_username):
    nickname = message.text.strip()
    if not nickname or len(nickname) > 20:
        bot.reply_to(message, "‼️Никнейм должен быть от 1 до 20 символов. Попробуй ещё раз‼️", reply_markup=ForceReply())
        bot.register_next_step_handler(message, handle_nickname, user_id, default_username)
        return
    player_data = init_player_temp(user_id, default_username)
    player_data['username'] = nickname
    save_player(user_id, player_data)
    bot.reply_to(message, f"✅Никнейм установлен: {nickname}! Жми 'Клик💰', чтобы начать!", reply_markup=get_main_keyboard())

# Команда /click и кнопка "Клик💰"
@bot.message_handler(commands=['click'])
@bot.message_handler(func=lambda message: message.text == "Клик💰")
def click_command(message):
    user_id = str(message.from_user.id)
    players = load_players()
    player = players.get(user_id)
    if not player:
        bot.reply_to(message, "Сначала начни игру с /start!", reply_markup=get_main_keyboard())
        return
    
    autoclick_coins = update_autoclick(player)
    player['coins'] = int(player['coins'] + player['click_power'])
    player['total_clicks'] += 1
    save_players(players)
    
    print(f"DEBUG: Клик для {user_id}, монеты: {player['coins']}, автоклик начислил: {autoclick_coins}")
    bot.reply_to(message, f"+{player['click_power']} монет!\nТвой баланс: {player['coins']}💰", reply_markup=get_main_keyboard())

# Команда /shop и кнопка "Магазин🏪"
@bot.message_handler(commands=['shop'])
@bot.message_handler(func=lambda message: message.text == "Магазин🏪")
def shop_command(message):
    user_id = str(message.from_user.id)
    players = load_players()
    player = players.get(user_id)
    if not player:
        bot.reply_to(message, "Сначала начни игру с /start!", reply_markup=get_main_keyboard())
        return
    update_autoclick(player)
    save_players(players)
    bot.reply_to(message, f"Магазин 🏪\n💰Твой баланс: {player['coins']}\nВыбери улучшение:", reply_markup=get_shop_keyboard(user_id))

# Команда /profile и кнопка "Профиль📱"
@bot.message_handler(commands=['profile'])
@bot.message_handler(func=lambda message: message.text == "Профиль📱")
def profile_command(message):
    user_id = str(message.from_user.id)
    players = load_players()
    player = players.get(user_id)
    if not player:
        bot.reply_to(message, "Сначала начни игру с /start!", reply_markup=get_main_keyboard())
        return
    update_autoclick(player)
    save_players(players)

    sorted_players = sorted(players.items(), key=lambda x: x[1]['coins'], reverse=True)
    rank = next(i + 1 for i, (pid, _) in enumerate(sorted_players) if pid == user_id)

    profile_text = (
        f"👤 Твой профиль:\n\n"
        f"📎Никнейм: [{player['username']}](tg://user?id={player['telegram_id']})\n"
        f"💰Монеты: {player['coins']}\n"
        f"💎Сила клика: {player['click_power']}\n"
        f"⌛️Автоклик: {player['autoclick']}/с\n"
        f"🔸Всего кликов: {player['total_clicks']}\n"
        f"👑Место в рейтинге: {rank}"
    )
    bot.reply_to(message, profile_text, parse_mode='Markdown', reply_markup=get_profile_buttons())

# Команда /top и кнопка "Рейтинг👑"
@bot.message_handler(commands=['top'])
@bot.message_handler(func=lambda message: message.text == "Рейтинг👑")
def top_command(message):
    user_id = str(message.from_user.id)
    players = load_players()
    if not players:
        bot.reply_to(message, "Пока нет игроков в топе!", reply_markup=get_main_keyboard())
        return
    player = players.get(user_id)
    if player:
        update_autoclick(player)
        save_players(players)

    top_players = sorted(players.items(), key=lambda x: x[1]['coins'], reverse=True)[:10]
    top_text = "🏆 Топ-10 игроков:\n\n"
    for i, (pid, p) in enumerate(top_players, 1):
        if i == 1:
            top_text += f"🥇 [{p['username']}](tg://user?id={p['telegram_id']}) — {p['coins']} монет\n"
        elif i == 2:
            top_text += f"🥈 [{p['username']}](tg://user?id={p['telegram_id']}) — {p['coins']} монет\n"
        elif i == 3:
            top_text += f"🥉 [{p['username']}](tg://user?id={p['telegram_id']}) — {p['coins']} монет\n"
        else:
            top_text += f" {i}.  [{p['username']}](tg://user?id={p['telegram_id']}) — {p['coins']} монет\n"
    bot.reply_to(message, top_text, parse_mode='Markdown', reply_markup=get_main_keyboard())

# Команда /luck и кнопка "Испытать удачу🎲"
@bot.message_handler(commands=['luck'])
@bot.message_handler(func=lambda message: message.text == "Испытать удачу🎲")
def luck_command(message):
    user_id = str(message.from_user.id)
    players = load_players()
    player = players.get(user_id)
    if not player:
        bot.reply_to(message, "Сначала начни игру с /start!", reply_markup=get_main_keyboard())
        return
    update_autoclick(player)
    save_players(players)
    bot.reply_to(message, f"Испытать удачу 🎲\nТвой баланс: {player['coins']}💰\nВведи сумму ставки (минимум 100💰)\n\n⚠️Чтобы отменить ставку /cancel", reply_markup=ForceReply())
    bot.register_next_step_handler(message, handle_luck_bet, user_id)

# Команды /help и /menu
@bot.message_handler(commands=['help', 'menu'])
def help_command(message):
    help_text = (
        "Основные команды бота:\n"
        "/click — Нажми, чтобы заработать монеты!\n"
        "/shop — Открой магазин для покупки улучшений.\n"
        "/profile — Посмотри свой профиль и статистику.\n"
        "/top — Узнай, кто в топе игроков!\n"
        "/luck — Испытай удачу, ставь монеты и выигрывай!\n"
        "/help или /menu — Покажи это сообщение с командами."
    )
    bot.reply_to(message, help_text, reply_markup=get_main_keyboard())

# Команда /cancel
@bot.message_handler(commands=['cancel'])
def cancel_command(message):
    bot.reply_to(message, "⚠️Ставка отменена! Возвращаемся в главное меню.", reply_markup=get_main_keyboard())

# Обработка ставки
def handle_luck_bet(message, user_id):
    if message.text == "/cancel":
        bot.reply_to(message, "⚠️Ставка отменена! Возвращаемся в главное меню.", reply_markup=get_main_keyboard())
        return

    players = load_players()
    player = players.get(user_id)
    if not player:
        bot.reply_to(message, "Ошибка: профиль не найден. Попробуй /start.", reply_markup=get_main_keyboard())
        return

    try:
        bet = int(message.text.strip())
        if bet < 100:
            bot.reply_to(message, "⚠️Ставка должна быть минимум 100 монет. Попробуй ещё раз или введи /cancel:", reply_markup=ForceReply())
            bot.register_next_step_handler(message, handle_luck_bet, user_id)
            return
        if bet > player['coins']:
            bot.reply_to(message, "💵Недостаточно монет! Попробуй меньшую ставку или /cancel:", reply_markup=ForceReply())
            bot.register_next_step_handler(message, handle_luck_bet, user_id)
            return
    except ValueError:
        bot.reply_to(message, "Введи сумму ставки (минимум 100💰) или отмени - /cancel:", reply_markup=ForceReply())
        bot.register_next_step_handler(message, handle_luck_bet, user_id)
        return

    player['coins'] = int(player['coins'] - bet)
    save_players(players)
    bot.reply_to(message, f"✅Ставка {bet} монет принята! Выбери число от 1 до 6", reply_markup=ForceReply())
    bot.register_next_step_handler(message, handle_luck_number, user_id, bet)

# Обработка выбранного числа
def handle_luck_number(message, user_id, bet):
    if message.text == "/cancel":
        players = load_players()
        player = players.get(user_id)
        if player:
            player['coins'] = int(player['coins'] + bet)
            save_players(players)
        bot.reply_to(message, "❎Ставка отменена! Возвращаемся в главное меню.", reply_markup=get_main_keyboard())
        return

    players = load_players()
    player = players.get(user_id)
    if not player:
        bot.reply_to(message, "Ошибка: профиль не найден. Попробуй /start.", reply_markup=get_main_keyboard())
        return

    try:
        number = int(message.text.strip())
        if number < 1 or number > 6:
            bot.reply_to(message, "Выбери число от 1 до 6 или отмени - /cancel:", reply_markup=ForceReply())
            bot.register_next_step_handler(message, handle_luck_number, user_id, bet)
            return
    except ValueError:
        bot.reply_to(message, "Введи число от 1 до 6 или отмени - /cancel:", reply_markup=ForceReply())
        bot.register_next_step_handler(message, handle_luck_number, user_id, bet)
        return

    dice = random.randint(1, 6)
    dice_image = os.path.join(DICE_DIR, f"dice_{dice}.png")
    if os.path.exists(dice_image):
        with open(dice_image, 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    else:
        print(f"DEBUG: Изображение {dice_image} не найдено")

    if number == dice:
        winnings = bet * 5
        player['coins'] = int(player['coins'] + winnings)
        result = f"🎲 Кубик: {dice}\nПоздравляем🎉🎉🎉! Ты угадал!\n✅Выигрыш: {winnings} монет!"
    else:
        result = f"🎲 Кубик: {dice}\nУвы, не угадал😭😭😭"

    save_players(players)
    bot.reply_to(message, f"{result}\n\nТвой баланс: {player['coins']}💰", reply_markup=get_main_keyboard())

# Обработчик inline-кнопок
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = str(call.from_user.id)
    players = load_players()
    player = players.get(user_id)
    if not player:
        bot.answer_callback_query(call.id, "Сначала начни игру с /start!")
        return

    update_autoclick(player)

    if call.data == "buy_click":
        click_cost = 50 * (player['click_power'] ** 2)
        if player['coins'] >= click_cost:
            player['coins'] = int(player['coins'] - click_cost)
            player['click_power'] += 1
            save_players(players)
            bot.answer_callback_query(call.id, "💪Сила клика увеличена!")
            bot.edit_message_text(
                f"Магазин 🏪\nТвой баланс: {player['coins']}💰\nВыбери улучшение:",
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_shop_keyboard(user_id)
            )
        else:
            bot.answer_callback_query(call.id, "😪Недостаточно монет!")

    elif call.data == "buy_autoclick":
        autoclick_cost = 100 * ((player['autoclick'] + 1) ** 2)
        if player['coins'] >= autoclick_cost:
            player['coins'] = int(player['coins'] - autoclick_cost)
            player['autoclick'] += 1
            save_players(players)
            bot.answer_callback_query(call.id, "✨Автоклик увеличен!")
            bot.edit_message_text(
                f"Магазин 🏪\nТвой баланс: {player['coins']}💰\nВыбери улучшение:",
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_shop_keyboard(user_id)
            )
        else:
            bot.answer_callback_query(call.id, "😪Недостаточно монет!")

    elif call.data == "change_nickname":
        bot.answer_callback_query(call.id)
        msg = bot.send_message(call.message.chat.id, "Введи новый никнейм:", reply_markup=ForceReply())
        bot.register_next_step_handler(msg, handle_nickname_change, user_id)

    elif call.data == "show_help":
        bot.answer_callback_query(call.id)
        help_text = (
            "Основные команды бота:\n"
            "/click — Нажми, чтобы заработать монеты!\n"
            "/shop — Открой магазин для покупки улучшений.\n"
            "/profile — Посмотри свой профиль и статистику.\n"
            "/top — Узнай, кто в топе игроков!\n"
            "/luck — Испытай удачу, ставь монеты и выигрывай!\n"
            "/help или /menu — Покажи это сообщение с командами."
        )
        bot.send_message(call.message.chat.id, help_text, reply_markup=get_main_keyboard())

# Обработка смены никнейма
def handle_nickname_change(message, user_id):
    nickname = message.text.strip()
    if not nickname or len(nickname) > 20:
        bot.reply_to(message, "Никнейм должен быть от 1 до 20 символов. Попробуй ещё раз:", reply_markup=ForceReply())
        bot.register_next_step_handler(message, handle_nickname_change, user_id)
        return
    players = load_players()
    if user_id in players:
        players[user_id]['username'] = nickname
        save_players(players)
        bot.reply_to(message, f"Никнейм изменён на: {nickname}!", reply_markup=get_main_keyboard())
    else:
        bot.reply_to(message, "Ошибка: профиль не найден. Попробуй /start.", reply_markup=get_main_keyboard())

# Обработка неизвестных команд и текста
@bot.message_handler(content_types=['text'])
def handle_unknown(message):
    valid_buttons = ["Клик💰", "Магазин🏪", "Испытать удачу🎲", "Профиль📱", "Рейтинг👑"]
    if message.text.startswith('/') or message.text not in valid_buttons:
        bot.reply_to(message, "Список доступных команд: /help", reply_markup=get_main_keyboard())

# Глобальные переменные для управления ботом
bot_running = False
polling_task = None

# Запуск бота
async def start_bot():
    global bot_running, polling_task
    if not bot_running:
        bot_running = True
        print("DEBUG: Попытка запуска бота...")
        try:
            print("DEBUG: Инициализация polling...")
            polling_task = asyncio.create_task(bot.infinity_polling(timeout=10, skip_pending=True))
            print("DEBUG: Polling запущен")
            await polling_task
        except Exception as e:
            bot_running = False
            print(f"DEBUG: Ошибка при запуске polling: {e}")
            raise
        finally:
            print("DEBUG: Polling завершён")
    else:
        print("Бот уже запущен!")

# Остановка бота
async def stop_bot():
    global bot_running, polling_task
    if bot_running:
        bot_running = False
        print("DEBUG: Попытка остановки бота...")
        try:
            bot.stop_bot()  # Полностью останавливаем бота
            if polling_task:
                polling_task.cancel()
                try:
                    await polling_task
                except asyncio.CancelledError:
                    print("DEBUG: Polling задача отменена")
            print("Бот остановлен!")
        except Exception as e:
            print(f"DEBUG: Ошибка при остановке бота: {e}")
            raise
    else:
        print("Бот уже остановлен!")

if __name__ == "__main__":
    print(f"Текущая директория: {os.getcwd()}")
    print(f"Путь к players.json: {os.path.abspath(PLAYERS_FILE)}")
    asyncio.run(start_bot())