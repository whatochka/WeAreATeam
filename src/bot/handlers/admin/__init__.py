from aiogram import Router

from bot.filters.roles import IsAdmin, IsWithRole, IsOrganizer, IsCaptain

from .broadcast.dialogs import broadcast_dialog
from .logs.router import router as logs_router
from .money.router import router as money_router
from .panel.dialogs import admin_panel_dialog
from .panel.router import router as admin_panel_router
from .secrets.dialogs import (
    create_secret_dialog,
    edit_secret_dialog,
    view_secrets_dialog,
)
from .shop.dialogs import (
    create_product_dialog,
    edit_product_dialog,
    view_products_dialog,
)
from .shop.router import router as products_routes
from .tasks.dialogs import create_task_dialog, view_tasks_dialog
from .tasks.router import router as tasks_router
from .users.cart.dialogs import user_cart_dialog
from .users.role.dialogs import user_role_dialog
from .users.router import router as users_router
from .users.task.dialogs import (
    cancel_task_dialog,
    confirm_task_dialog,
    view_user_task_dialog,
)
from .users.view.dialogs import view_user_dialog


def include_admin_routers(root_router: Router) -> None:
    admin_router = Router(name=__file__)
    for observer in admin_router.observers.values():
        observer.filter(IsAdmin())
    admin_router.include_routers(
        logs_router,
        money_router,
        products_routes,
    )

    # seller_router = Router(name=__file__)
    # for observer in seller_router.observers.values():
    #     observer.filter(IsSeller())
    # seller_router.include_routers()

    with_role_router = Router(name=__file__)
    for observer in with_role_router.observers.values():
        observer.filter(IsWithRole())
    with_role_router.include_routers(
        admin_panel_router,
        admin_router,
        users_router,
    )

    root_router.include_router(with_role_router)


def include_admin_dialogs(root_router: Router) -> None:
    admin_router = Router(name=__file__)
    for observer in admin_router.observers.values():
        observer.filter(IsAdmin())
    admin_router.include_routers(
        broadcast_dialog,
        view_secrets_dialog,
        create_secret_dialog,
        edit_secret_dialog,
        user_role_dialog,
        view_products_dialog,
        create_product_dialog,
        edit_product_dialog,
    )

    seller_router = Router(name=__file__)
    for observer in seller_router.observers.values():
        observer.filter(IsOrganizer())
    seller_router.include_router(
        user_cart_dialog,
    )

    stager_router = Router(name=__file__)
    for observer in stager_router.observers.values():
        observer.filter(IsOrganizer())
    stager_router.include_routers(
        view_tasks_dialog,
        create_task_dialog,
        view_user_task_dialog,
        cancel_task_dialog,
        confirm_task_dialog,
    )

    with_role_router = Router(name=__file__)
    for observer in with_role_router.observers.values():
        observer.filter(IsWithRole())
    with_role_router.include_routers(
        admin_panel_dialog,
        view_user_dialog,
        admin_router,
        seller_router,
        stager_router,
    )

    root_router.include_router(with_role_router)
