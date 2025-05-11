import sys
import json
import os
import asyncio
import threading
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QTableWidget, QTableWidgetItem, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal, QMetaObject, Q_ARG
from PyQt5.QtGui import QFont
import tg_bot_practice
import io

# Путь к players.json (относительный)
PLAYERS_FILE = os.path.join(os.path.dirname(__file__), 'players.json')

class BotManager(QMainWindow):
    # Сигнал для логирования
    log_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Telegram Bot Manager")
        self.setGeometry(100, 100, 1150, 600)
        self.bot_thread = None
        self.is_updating = False
        self.init_ui()
        self.load_players()

        # Подключаем сигнал логирования
        self.log_signal.connect(self.append_log)

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_panel.setFixedWidth(300)

        self.start_button = QPushButton("Старт")
        self.start_button.clicked.connect(self.start_bot)
        left_layout.addWidget(self.start_button)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(QFont("Courier New", 11))  # Увеличиваем шрифт лога
        left_layout.addWidget(self.log_text)

        main_layout.addWidget(left_panel)

        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "User ID", "Username", "Coins", "Click Power", "Autoclick", "Total Clicks", "Rank"
        ])
        self.table.setEditTriggers(QTableWidget.DoubleClicked)
        self.table.cellChanged.connect(self.save_player_changes)
        self.table.setMinimumSize(600, 400)
        right_layout.addWidget(self.table)

        table_buttons = QHBoxLayout()
        self.refresh_button = QPushButton("Обновить")
        self.refresh_button.clicked.connect(self.load_players)
        table_buttons.addWidget(self.refresh_button)

        self.delete_button = QPushButton("Удалить выбранное")
        self.delete_button.clicked.connect(self.delete_player)
        table_buttons.addWidget(self.delete_button)

        right_layout.addLayout(table_buttons)
        main_layout.addWidget(right_panel)

        # Перенаправление stdout и stderr
        sys.stdout = StreamRedirector(self.safe_log)
        sys.stderr = StreamRedirector(self.safe_log)

        self.apply_styles()

    def apply_styles(self):
        qss = """
        /* Основное окно */
        QMainWindow {
            background-color: #212121;  /* Тёмно-серый фон */
        }

        /* Кнопки */
        QPushButton {
            background-color: #388E3C;  /* Мягкий зелёный */
            color: #ffffff;
            border-radius: 4px;  /* Более скругленные углы */
            padding: 10px;
            font-size: 17px;
            font-family: "Arial";
            border: 1px solid #2E7D32;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);  /* Тень */
        }
        QPushButton:hover {
            background-color: #34cb3b;  /* Светлее при наведении */
        }
        QPushButton:pressed {
            background-color: #2E7D32;  /* Темнее при нажатии */
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);  /* Уменьшенная тень */
        }

        /* Лог (QTextEdit) */
        QTextEdit {
            background-color: #181818;  /* Чуть темнее фон */
            color: #E0E0E0;  /* Светло-серый текст */
            border: 1px solid #424242;
            border-radius: 8px;  /* Скругленные углы */
            font-family: "Courier New";
            font-size: 11px;
            padding: 5px;
        }

        /* Таблица */
        QTableWidget {
            background-color: #181818;  /* Тёмный фон таблицы */
            color: #ffffff;  /* Светло-серый текст */
            gridline-color: #8f8f8f;  /* Серые линии сетки */
            selection-background-color: #388E3C;  /* Зелёный фон выделения */
            selection-color: #ffffff;
            border: 1px solid #424242;
            border-radius: 3px;  /* Скругленные углы */
            font-family: "Arial";
            font-size: 13px;  /* Увеличенный шрифт */
        }
        QTableWidget::item {
            padding: 4px;  /* Уменьшенные отступы в ячейках */
            border: none;  /* Убираем границы ячеек */
        }
        QTableWidget::item:selected {
            background-color: #24a32a;  /* Зелёный фон для выделенных ячеек */
        }

        /* Убираем белые пробелы в области прокрутки */
        QTableWidget QAbstractScrollArea {
            background-color: #181818;  /* Тёмный фон для области прокрутки */
        }
        QTableWidget QScrollBar:vertical {
            background: #181818;
            width: 10px;
            margin: 0px;
        }
        QTableWidget QScrollBar::handle:vertical {
            background: #424242;
            border-radius: 5px;
        }
        QTableWidget QScrollBar::add-line:vertical, QTableWidget QScrollBar::sub-line:vertical {
            height: 0px;
        }

        /* Заголовки таблицы */
        QHeaderView::section {
            background-color: #3b3b3b;  /* Тёмно-серый фон заголовков */
            color: #E0E0E0;
            padding: 6px;
            border: 1px solid #8f8f8f;
            font-family: "Arial";
            font-size: 13px;
            font-weight: bold;
        }
        QHeaderView::section:horizontal {
            border-right: 1px solid #8f8f8f;  /* Разделяем заголовки */
        }
        """
        self.setStyleSheet(qss)

    def safe_log(self, message):
        if message.strip():
            # Потокобезопасное добавление лога через invokeMethod
            QMetaObject.invokeMethod(
                self.log_text,
                "append",
                Qt.QueuedConnection,
                Q_ARG(str, message)
            )

    def append_log(self, message):
        if message.strip():
            self.log_text.append(message)
            # Прокрутка в конец без QTextCursor
            self.log_text.verticalScrollBar().setValue(self.log_text.verticalScrollBar().maximum())

    def load_players(self):
        if self.is_updating:
            return
        self.is_updating = True
        try:
            self.table.blockSignals(True)
            try:
                with open(PLAYERS_FILE, 'r') as f:
                    players = json.load(f)
                self.safe_log(f"DEBUG: Загружено игроков: {len(players)}")
            except FileNotFoundError:
                self.safe_log(f"DEBUG: Файл {PLAYERS_FILE} не найден")
                players = {}
            except json.JSONDecodeError as e:
                self.safe_log(f"DEBUG: Ошибка формата JSON в {PLAYERS_FILE}: {e}")
                players = {}
            except Exception as e:
                self.safe_log(f"DEBUG: Ошибка загрузки {PLAYERS_FILE}: {e}")
                players = {}

            sorted_players = sorted(players.items(), key=lambda x: x[1]['coins'], reverse=True)
            self.table.setRowCount(0)
            self.table.setRowCount(len(players))
            for row, (user_id, player) in enumerate(sorted_players):
                rank = row + 1
                self.table.setItem(row, 0, QTableWidgetItem(user_id))
                self.table.setItem(row, 1, QTableWidgetItem(player['username']))
                self.table.setItem(row, 2, QTableWidgetItem(str(int(player['coins']))))
                self.table.setItem(row, 3, QTableWidgetItem(str(player['click_power'])))
                self.table.setItem(row, 4, QTableWidgetItem(str(player['autoclick'])))
                self.table.setItem(row, 5, QTableWidgetItem(str(player['total_clicks'])))
                self.table.setItem(row, 6, QTableWidgetItem(str(rank)))
                for col in [0, 6]:
                    item = self.table.item(row, col)
                    if item:
                        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.table.setColumnWidth(1, 175)  # Устанавливаем ширину столбца "Username" в 150 пикселей
            #self.table.resizeColumnsToContents()
            #self.table.resizeRowsToContents()
            self.safe_log("Таблица игроков обновлена")
        finally:
            self.table.blockSignals(False)
            self.is_updating = False

    def save_player_changes(self, row, column):
        if self.is_updating or column in [0, 6]:
            return
        self.is_updating = True
        try:
            user_id = self.table.item(row, 0).text()
            try:
                with open(PLAYERS_FILE, 'r') as f:
                    players = json.load(f)
            except Exception as e:
                self.safe_log(f"DEBUG: Ошибка загрузки players.json: {e}")
                return

            if user_id in players:
                value = self.table.item(row, column).text()
                try:
                    if column == 1:
                        players[user_id]['username'] = value
                    elif column == 2:
                        players[user_id]['coins'] = int(value)
                    elif column == 3:
                        players[user_id]['click_power'] = int(value)
                    elif column == 4:
                        players[user_id]['autoclick'] = int(value)
                    elif column == 5:
                        players[user_id]['total_clicks'] = int(value)
                    with open(PLAYERS_FILE, 'w') as f:
                        json.dump(players, f, indent=4)
                    self.safe_log(f"Игрок {user_id} обновлён")
                    self.load_players()
                except ValueError:
                    self.safe_log(f"DEBUG: Ошибка: Некорректное значение для {user_id}")
                except Exception as e:
                    self.safe_log(f"DEBUG: Ошибка сохранения игрока: {e}")
            else:
                self.safe_log(f"DEBUG: Игрок {user_id} не найден")
        finally:
            self.is_updating = False

    def delete_player(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Ошибка", "Выберите игрока для удаления")
            return
        user_id = self.table.item(selected_rows[0].row(), 0).text()
        try:
            with open(PLAYERS_FILE, 'r') as f:
                players = json.load(f)
            if user_id in players:
                del players[user_id]
                with open(PLAYERS_FILE, 'w') as f:
                    json.dump(players, f, indent=4)
                self.safe_log(f"Игрок {user_id} удалён")
                self.load_players()
            else:
                self.safe_log(f"DEBUG: Игрок {user_id} не найден")
        except Exception as e:
            self.safe_log(f"DEBUG: Ошибка удаления игрока: {e}")

    def run_bot(self):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            self.safe_log("DEBUG: Запуск цикла asyncio для бота...")
            loop.run_until_complete(tg_bot_practice.start_bot())
            self.safe_log("DEBUG: Цикл бота завершён")
        except Exception as e:
            self.safe_log(f"DEBUG: Ошибка в потоке бота: {e}")
        finally:
            loop.close()
            self.bot_thread = None
            self.safe_log("DEBUG: Поток бота завершён")

    def start_bot(self):
        if self.bot_thread is None or not self.bot_thread.is_alive():
            self.bot_thread = threading.Thread(target=self.run_bot, daemon=True)
            self.bot_thread.start()
            self.safe_log(f"Запуск бота... Поток: {self.bot_thread.name}")
        else:
            self.safe_log(f"Бот уже запущен! Поток: {self.bot_thread.name}")

    def closeEvent(self, event):
        # Предупреждение при закрытии
        reply = QMessageBox.question(
            self,
            "Подтверждение выхода",
            "Вы действительно хотите выйти? Закрытие приложения приведет к остановке бота.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            # Останавливаем бот перед закрытием
            if self.bot_thread and self.bot_thread.is_alive():
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    asyncio.run_coroutine_threadsafe(tg_bot_practice.stop_bot(), loop)
                    self.bot_thread.join(timeout=5.0)
                    if self.bot_thread.is_alive():
                        self.safe_log("DEBUG: Поток бота не завершился вовремя")
                    else:
                        self.safe_log("DEBUG: Поток бота успешно завершён")
                    loop.close()
                except Exception as e:
                    self.safe_log(f"DEBUG: Ошибка остановки бота: {e}")
                finally:
                    self.bot_thread = None
            event.accept()
        else:
            event.ignore()

# Перенаправление stdout/stderr
class StreamRedirector(io.StringIO):
    def __init__(self, log_callback):
        super().__init__()
        self.log_callback = log_callback

    def write(self, text):
        self.log_callback(text.strip())

    def flush(self):
        pass

if __name__ == "__main__":
    # Настройка Qt для масштабирования
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QApplication(sys.argv)
    window = BotManager()
    window.show()
    sys.exit(app.exec_())