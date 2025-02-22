from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const

from bot.dialogs.buttons import GoToMenuButton

from .states import HelpStates

HELP_TEXT = """
<b>Хочешь узнать, что я умею?</b> 💪

Узнаешь позже ;)

ℹ️ <b>Помимо меню, у бота есть несколько команд:</b>

/start — Перезапуск бота и главное меню.
/menu — Твой баланс, ID и главное меню.
/help — Всё, что нужно знать о боте.
/shop — Товары в наличии, тут можно потратить свои Червонцы.
/cart — Твои покупки, храню их для тебя.
/task — Твоё активное задание, работает, только если оно у тебя есть.

🆘 Если что-то идёт не так, всё зависло и нервы на пределе — пиши @whatochka, он тебе поможет 😉
""".strip()  # noqa: E501


help_dialog = Dialog(
    Window(
        Const(HELP_TEXT),
        GoToMenuButton(),
        state=HelpStates.help,
    ),
)
