from aiogram import F
from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Format

from .on_actions import auth_number_password_handler
from .states import StartStates

AUTH_TEXT = """
🔑 Вход в систему 🔑

Введите ваш <b>индивидуальный номер</b> и <b>пароль</b> через пробел.
Пример: `123 mypassword`
""".strip()

BAD_AUTH_FORMAT = "❌ Ошибка: номер или пароль указаны неверно."

auth_window = Window(
    Format(AUTH_TEXT, when=~F["dialog_data"]["retry"]),
    Format(BAD_AUTH_FORMAT, when=F["dialog_data"]["retry"] == "format"),
    MessageInput(auth_number_password_handler, content_types=ContentType.TEXT),
    state=StartStates.number_password,
)

start_dialog = Dialog(auth_window)
