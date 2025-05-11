# Создание Telegram Clicker Bot: Исследование и Техническое Руководство

![ВИТРИНА](https://github.com/user-attachments/assets/12aa6556-c165-4a9c-a957-7e0025f3c7e1)

## Введение
Этот документ описывает процесс исследования и разработки мини-игры в виде Telegram-бота, представляющего собой кликер. Кликер — это простая игра, где пользователь зарабатывает виртуальные монеты, нажимая на кнопки, покупает улучшения и соревнуется с другими игроками. Бот также включает механику азартной игры (ставки на кубик) и систему рейтинга. Документ состоит из двух частей:
  ### 1. **Исследование предметной области и последовательность действий** — как была изучена тема и разработана технология.
  ### 2. **Техническое руководство для новичков** — пошаговые инструкции по созданию бота с примерами кода и иллюстрациями.


## Часть 1: Исследование предметной области и создание технологии

### 1.1 Исследование предметной области
Перед созданием бота было проведено исследование, чтобы понять, как работают Telegram-боты, какие библиотеки использовать и какие функции включить в игру. Основные этапы:
1. **Изучение Telegram Bot API:**
   * Telegram предоставляет API для создания ботов. Было изучено, как отправлять сообщения, обрабатывать команды, использовать клавиатуры (inline и reply) и управлять чатами.
   * Использована документация Telegram: https://core.telegram.org/bots/api.
2. **Анализ существующих кликер-игр:**
   * Изучены популярные кликер-игры, такие как Cookie Clicker и Telegram-боты вроде Notcoin.
   * Выделены ключевые механики: клики для заработка монет, улучшения (сила клика, автоклик), рейтинг игроков, азартные элементы.
3. **Выбор технологий:**
   * **Язык программирования:** Python, из-за простоты и наличия библиотек для Telegram.
   * **Библиотека:** python-telegram-bot (Telebot), так как она упрощает работу с Telegram API.
   * **Хранение данных:** JSON-файл для сохранения информации об - простое и надёжное решение для хранения профилей игроков.
   * **GUI:** PyQt5 для создания интерфейса управления ботом.
   * **Асинхронное программирование:** asyncio для обработки запросов бота.
4. **Определение функционала:**
   * Основные функции: клики для заработка монет, магазин улучшений, профиль игрока, рейтинг, игра на удачу (кубик).
   * Дополнительно: интерфейс для администрирования (Bot Manager) для управления игроками.
5. **Прототипирование:**
   * Создан прототип бота с минимальной функциональностью (команда _/start_, клик, сохранение данных).
   * Протестированы базовые механики и выявлены проблемы, такие как синхронизация данных и обработка ошибок.
  
### 1.2 Последовательность действий по созданию технологии
1. **Настройка окружения:**
   * Установлены Python, библиотеки (telebot, PyQt5, python-dotenv) и созданы файлы окружения (.env).
   * Зарегистрирован бот через BotFather в Telegram для получения токена.
2. **Разработка ядра бота:**
   * Реализована основная логика в tg_bot_practice.py: обработка команд, сохранение данных, автоклик, магазин, рейтинг, игра на удачу.
   * Добавлена обработка ошибок и отладочные сообщения.
3. **Создание интерфейса управления:**
   * Разработан GUI в bot_manager.py с использованием PyQt5.
   * Реализованы функции просмотра, редактирования и удаления данных игроков.
4. **Тестирование:**
   * Проведено тестирование бота в Telegram: проверены все команды, клавиатуры, обработка некорректных данных.
   * Тестирование GUI: проверка обновления таблицы, логирование, корректность изменений.
5. **Оптимизация:**
   * Улучшена производительность автоклика (оптимизация расчётов).
   * Добавлены проверки валидности данных перед сохранением.
   * Улучшен дизайн интерфейса GUI (тёмная тема, стилизация).
6. **Документирование:**
   * Составлена документация для пользователей и разработчиков.
   * Подготовлены иллюстрации и диаграммы для наглядности.

## Часть 2: Техническое руководство для новичков
Это руководство поможет вам создать Telegram-бот кликер с нуля. Оно ориентировано на начинающих разработчиков, знакомых с основами Python.

### 2.1 Предварительные требования
* **Python 3.8+:** Установите Python с официального сайта.
* **Редактор кода:** Рекомендуется Visual Studio Code.
* **Telegram:** Аккаунт в Telegram для создания бота.
* **Базовые знания:** Python, JSON, основы работы с файлами.
### 2.2 Пошаговые инструкции
### Шаг 1: Настройка окружения
1. **Установите Python:**
   * Скачайте и установите Python с python.org.
   * Проверьте установку командой в консоли: <br>
     ```python --version```
2. **Создайте проект:**
   * Создайте папку для проекта, например, telegram_clicker_bot.
   * Откройте терминал в этой папке.
3. **Установите зависимости:**
   * Установите необходимые библиотеки: <br>
     ```pip install python-telegram-bot PyQt5 python-dotenv```
4. **Создайте бота в Telegram:**
   * Откройте Telegram, найдите @BotFather.
   * Отправьте команду /start, затем /newbot.
   * Следуйте инструкциям: задайте имя и username бота (например, @MyClickerBot).
   * Сохраните полученный токен (например, ```123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11```). <br>
   
   ![1](https://github.com/user-attachments/assets/3764ee8b-8107-4e7c-9f37-7c6aa9329a76)
   
5. **Создайте файл .env:**
   * В папке проекта создайте файл .env и добавьте токен: <br>
```TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11```

### Шаг 2: Создание основного кода бота
1. **Создайте файл tg_bot_practice.py:**
   * В папке проекта создайте файл tg_bot_practice.py
2. **Перейдите в Visual Studio Code и напишите базовый код:**

![2](https://github.com/user-attachments/assets/ee5f18c4-490d-4f43-aa0d-d5834a880c36)

```
import telebot
from dotenv import load_dotenv
import os

# Загружаем токен из .env
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать в кликер! Нажми /click, чтобы начать!")

# Команда /click
@bot.message_handler(commands=['click'])
def click_command(message):
    bot.reply_to(message, "Ты заработал 1 монету!")

# Запуск бота
bot.infinity_polling()
```
3. **Протестируйте бота:**
   * Запустите файл.
   * В Telegram отправьте боту команды _/start_ и _/click_. Вы должны увидеть ответы.

![3](https://github.com/user-attachments/assets/cdc9586b-60f6-4242-9445-b1be86e68ac8)

![4](https://github.com/user-attachments/assets/31769b68-806b-431a-ad16-14b23e359b4c)

### Шаг 3: Добавление хранения данных
1. **Создайте функции для работы с JSON:**
   * Добавьте в tg_bot_practice.py код для сохранения данных игроков:

```
import json

PLAYERS_FILE = 'players.json'

def load_players():
    try:
        with open(PLAYERS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_players(players):
    with open(PLAYERS_FILE, 'w') as f:
        json.dump(players, f, indent=4)

def init_player(user_id, username):
    return {
        'username': username,
        'coins': 0,
        'click_power': 1,
        'autoclick': 0,
        'total_clicks': 0
    }
```

2. **Обновите команду _/start_:**
   * Добавьте регистрацию игрока:

```
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = str(message.from_user.id)
    username = message.from_user.username or message.from_user.first_name
    players = load_players()
    if user_id not in players:
        players[user_id] = init_player(user_id, username)
        save_players(players)
    bot.reply_to(message, "Добро пожаловать в кликер! Нажми /click, чтобы начать!")
```

3. **Обновите команду _/click_:**
   * Добавьте начисление монет:

```
@bot.message_handler(commands=['click'])
def click_command(message):
    user_id = str(message.from_user.id)
    players = load_players()
    if user_id in players:
        players[user_id]['coins'] += players[user_id]['click_power']
        players[user_id]['total_clicks'] += 1
        save_players(players)
        bot.reply_to(message, f"+{players[user_id]['click_power']} монет! Баланс: {players[user_id]['coins']}")
    else:
        bot.reply_to(message, "Сначала начни игру с /start!")
```

### Шаг 4: Добавление клавиатур и магазина
1. **Создайте клавиатуру:**
   * Добавьте функцию для создания клавиатуры:

```
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(KeyboardButton("Клик💰"))
    keyboard.row(KeyboardButton("Магазин🏪"), KeyboardButton("Профиль📱"))
    return keyboard
```

2. **Обновите команду _/start_:**
   * Добавьте клавиатуру:

```
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = str(message.from_user.id)
    username = message.from_user.username or message.from_user.first_name
    players = load_players()
    if user_id not in players:
        players[user_id] = init_player(user_id, username)
        save_players(players)
    bot.reply_to(message, "Добро пожаловать в кликер! Жми 'Клик💰', чтобы начать!", reply_markup=get_main_keyboard())
```

3. **Добавьте магазин:**
   * Создайте команду _/shop_ и inline-клавиатуру:

```
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_shop_keyboard(user_id):
    players = load_players()
    player = players.get(user_id, {'click_power': 1})
    markup = InlineKeyboardMarkup()
    click_cost = 50 * (player['click_power'] ** 2)
    markup.add(InlineKeyboardButton(f"Улучшить клик (+1 за {click_cost} монет)", callback_data="buy_click"))
    return markup

@bot.message_handler(commands=['shop'])
def shop_command(message):
    user_id = str(message.from_user.id)
    players = load_players()
    player = players.get(user_id)
    if not player:
        bot.reply_to(message, "Сначала начни игру с /start!", reply_markup=get_main_keyboard())
        return
    bot.reply_to(message, f"Магазин 🏪\n💰Твой баланс: {player['coins']}\nВыбери улучшение:", reply_markup=get_shop_keyboard(user_id))

@bot.callback_query_handler(func=lambda call: call.data == "buy_click")
def handle_callback(call):
    user_id = str(call.from_user.id)
    players = load_players()
    player = players.get(user_id)
    click_cost = 50 * (player['click_power'] ** 2)
    if player['coins'] >= click_cost:
        player['coins'] -= click_cost
        player['click_power'] += 1
        save_players(players)
        bot.answer_callback_query(call.id, "💪Сила клика увеличена!")
    else:
        bot.answer_callback_query(call.id, "😪Недостаточно монет!")
```

![5](https://github.com/user-attachments/assets/7c4d7ef6-181c-4f71-bdcf-337cee9ca57d)

### Шаг 5: Добавление игры на удачу
1. **Создайте команду _/luck_:**
   * Добавьте обработку ставки и выбор числа:

```
from telebot.types import ForceReply
import random

@bot.message_handler(commands=['luck'])
def luck_command(message):
    user_id = str(message.from_user.id)
    players = load_players()
    player = players.get(user_id)
    if not player:
        bot.reply_to(message, "Сначала начни игру с /start!", reply_markup=get_main_keyboard())
        return
    bot.reply_to(message, f"Испытать удачу 🎲\nТвой баланс: {player['coins']}💰\nВведи сумму ставки (минимум 100💰):", reply_markup=ForceReply())
    bot.register_next_step_handler(message, handle_luck_bet, user_id)

def handle_luck_bet(message, user_id):
    players = load_players()
    player = players.get(user_id)
    try:
        bet = int(message.text.strip())
        if bet < 100:
            bot.reply_to(message, "⚠️Ставка должна быть минимум 100 монет. Попробуй ещё раз:", reply_markup=ForceReply())
            bot.register_next_step_handler(message, handle_luck_bet, user_id)
            return
        if bet > player['coins']:
            bot.reply_to(message, "💵Недостаточно монет! Попробуй меньшую ставку:", reply_markup=ForceReply())
            bot.register_next_step_handler(message, handle_luck_bet, user_id)
            return
    except ValueError:
        bot.reply_to(message, "Введи число:", reply_markup=ForceReply())
        bot.register_next_step_handler(message, handle_luck_bet, user_id)
        return
    player['coins'] -= bet
    save_players(players)
    bot.reply_to(message, f"✅Ставка {bet} монет принята! Выбери число от 1 до 6:", reply_markup=ForceReply())
    bot.register_next_step_handler(message, handle_luck_number, user_id, bet)

def handle_luck_number(message, user_id, bet):
    players = load_players()
    player = players.get(user_id)
    try:
        number = int(message.text.strip())
        if number < 1 or number > 6:
            bot.reply_to(message, "Выбери число от 1 до 6:", reply_markup=ForceReply())
            bot.register_next_step_handler(message, handle_luck_number, user_id, bet)
            return
    except ValueError:
        bot.reply_to(message, "Введи число от 1 до 6:", reply_markup=ForceReply())
        bot.register_next_step_handler(message, handle_luck_number, user_id, bet)
        return
    dice = random.randint(1, 6)
    if number == dice:
        winnings = bet * 5
        player['coins'] += winnings
        result = f"🎲 Кубик: {dice}\nПоздравляем🎉! Ты угадал!\n✅Выигрыш: {winnings} монет!"
    else:
        result = f"🎲 Кубик: {dice}\nУвы, не угадал😭"
    save_players(players)
    bot.reply_to(message, f"{result}\n\nТвой баланс: {player['coins']}💰", reply_markup=get_main_keyboard())
```

Также создадим папку в проекте /dice и поместим туда картинки игральных костей от 1 до 6:

![6](https://github.com/user-attachments/assets/9a0bc82f-2ce9-42f0-8c50-393b1bd72466)

### Шаг 6: Создание интерфейса управления
На этом этапе разработаем админ-панель, с помощью которой мы сможем отслеживать данные пользователей в режиме реального времени.

1. **Создайте файл bot_manager.py:**
   * Добавьте код для GUI с использованием PyQt5:

```
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QTextEdit,彼此

class BotManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Telegram Bot Manager")
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)
        start_button = QPushButton("Старт")
        layout.addWidget(start_button)

if __name__ == "__main__":
    app = QApplication([])
    window = BotManager()
    window.show()
    app.exec_()
```

2. **Добавьте таблицу игроков:**
   * Обновите init_ui для добавления таблицы:

```
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

def init_ui(self):
    central_widget = QWidget()
    self.setCentralWidget(central_widget)
    layout = QVBoxLayout(central_widget)
    self.table = QTableWidget()
    self.table.setColumnCount(2)
    self.table.setHorizontalHeaderLabels(["User ID", "Username"])
    layout.addWidget(self.table)
    start_button = QPushButton("Старт")
    layout.addWidget(start_button)
    self.log_text = QTextEdit()
    self.log_text.setReadOnly(True)
    layout.addWidget(self.log_text)
```

3. **Добавьте загрузку данных:**
   * Реализуйте функцию load_players:

```
import json

def load_players(self):
    try:
        with open('players.json', 'r') as f:
            players = json.load(f)
        self.table.setRowCount(len(players))
        for row, (user_id, player) in enumerate(players.items()):
            self.table.setItem(row, 0, QTableWidgetItem(user_id))
            self.table.setItem(row, 1, QTableWidgetItem(player['username']))
    except Exception as e:
        self.log_text.append(f"Ошибка загрузки: {e}")
```

![7](https://github.com/user-attachments/assets/e8ea4077-9366-40a6-9118-316cb81b719b)

### Шаг 7: Тестирование и отладка
1. **Протестируйте бота:**
   * Запустите tg_bot_practice.py и проверьте все команды (_/start_, _/click_, _/shop_, _/luck_).
   * Убедитесь, что данные сохраняются в players.json.
2. **Протестируйте GUI:**
   * Запустите bot_manager.py и проверьте:
       * Загрузку данных в таблицу.
       * Редактирование и удаление игроков.
       * Логирование.
3. **Исправьте ошибки:**
   * Добавьте обработку исключений в коде (например, проверка существования файла).
   * Используйте отладочные сообщения (print или логи в GUI).

### 2.3 Советы для новичков
* **Изучайте ошибки:** Если бот не работает, проверьте логи в консоли или GUI.
* **Разделяйте код:** Используйте функции для разделения логики (например, load_players, save_players).
* **Тестируйте постепенно:** Добавляйте функции по одной и проверяйте их работу.
* **Используйте документацию:** Читайте документацию _python-telegram-bot_.

### 2.4 Возможности для расширения проекта
* Добавьте авторизацию для GUI (логин/пароль).
* Реализуйте ежедневные бонусы для игроков.
* Добавьте мультимедиа (например, отправку анимаций при выигрыше в /luck).
* Разверните бота на сервере для круглосуточной работы.

## Заключение
**Создание Telegram-бота кликера** — это отличный проект для изучения Python, работы с API и разработки игр. В ходе исследования были изучены Telegram Bot API, механики кликер-игр и выбраны подходящие технологии (Python, Telebot, PyQt5). Техническое руководство предоставляет пошаговые инструкции, примеры кода и иллюстрации, чтобы помочь новичкам создать собственный бот. Проект можно расширить, добавив новые функции, такие как ежедневные бонусы или мультимедиа, чтобы сделать игру ещё увлекательнее.
