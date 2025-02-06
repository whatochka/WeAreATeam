from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Back, Button, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.buttons import GoToAdminPanelButton, GoToMenuButton
from bot.dialogs.on_actions import on_start_update_dialog_data

from ..buttons import GoToSecretsButton
from ..getters import get_all_secrets, get_one_secret
from .on_actions import (
    on_confirm_delete_secret,
    on_create_secret,
    on_delete_secret,
    on_secret_selected,
)
from .states import ViewSecretsStates

secrets_list_window = Window(
    Const("🤫 Все секреты"),
    ScrollingGroup(
        Select(
            Format("{item.id} | {item.phrase}"),
            id="secrets_select",
            items="secrets",
            on_click=on_secret_selected,
            item_id_getter=lambda item: item.id,
            type_factory=int,
        ),
        width=1,
        height=10,
        hide_on_single_page=True,
        id="secrets_group",
    ),
    Button(
        Const("✏️ Создать секрет"),
        id="create",
        on_click=on_create_secret,
    ),
    GoToAdminPanelButton(),
    GoToMenuButton(),
    getter=get_all_secrets,
    state=ViewSecretsStates.list,
)

view_one_secret_window = Window(
    Format("ID: {secret.id}"),
    Format("Фраза:\n{secret.phrase}\n"),
    Format("Награда: {secret.reward}"),
    Format("Лимит активаций: {secret.activation_limit}"),
    Format("Всего активаций: {total_activations}"),
    # Row(
    #     Button(
    #         Const("💬 Изменить фразу"),
    #         id="pharse",
    #         on_click=on_edit_phrase,
    #     ),
    #     Button(
    #         Const("💰 Изменить награду"),
    #         id="reward",
    #         on_click=on_edit_reward,
    #     ),
    #     Button(
    #         Const("🚀 Изменить лимит"),
    #         id="activation_limit",
    #         on_click=on_edit_activation_limit,
    #     ),
    # ),
    Button(
        Const("🗑️ Удалить"),
        id="delete",
        on_click=on_delete_secret,
    ),
    Back(Const("⏪ Cекреты")),
    GoToAdminPanelButton(),
    getter=get_one_secret,
    state=ViewSecretsStates.one,
)

confirm_delete_secret_window = Window(
    Format("Ты уверен, что хочешь удалить секрет ID={secret.id}❓"),
    Button(
        Const("✅ Подтвердить"),
        id="confirm_delete",
        on_click=on_confirm_delete_secret,
    ),
    Back(Const("⏪ Отмена")),
    GoToSecretsButton(),
    GoToAdminPanelButton(),
    getter=get_one_secret,
    state=ViewSecretsStates.confirm,
)

view_secrets_dialog = Dialog(
    secrets_list_window,
    view_one_secret_window,
    confirm_delete_secret_window,
    on_start=on_start_update_dialog_data,
)
