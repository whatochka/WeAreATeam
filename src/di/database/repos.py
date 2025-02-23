from dishka import Provider, Scope, provide

from database.repos.logs import LogsRepo
from database.repos.products import ProductsRepo
from database.repos.team_products import TeamProductsRepo
from database.repos.team_purchases import TeamPurchasesRepo
from database.repos.purchases import PurchasesRepo
from database.repos.secrets import SecretsRepo
from database.repos.tasks import TasksRepo
from database.repos.users import UsersRepo


class ReposProvider(Provider):
    scope = Scope.REQUEST

    logs_repo = provide(LogsRepo)
    products_repo = provide(ProductsRepo)
    team_products_repo = provide(TeamProductsRepo)
    purchases_repo = provide(PurchasesRepo)
    team_purchases_repo = provide(TeamPurchasesRepo)
    users_repo = provide(UsersRepo)
    secrets_repo = provide(SecretsRepo)
    tasks_repo = provide(TasksRepo)
