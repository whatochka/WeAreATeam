import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

sys.path.insert(0, BASE_DIR)

import sys
import os
import asyncio
import csv
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import create_sessionmaker
from database.models.pre_registred_users import PreRegisteredUserModel
from database.config import get_db_config

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def import_users_from_csv(csv_file: str, session: AsyncSession):
    if not os.path.exists(csv_file):
        print(f"❌ Файл {csv_file} не найден!")
        return

    with open(csv_file, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        users = []

        for row in reader:
            number = row["number"]
            role = (
                "admin" if number == "000"
                else "organizer" if number.startswith("0")
                else "participant"
            )

            team_number = int(number[0]) if role == "participant" else None
            is_captain = row.get("is_captain", "false").lower() == "true"

            users.append(
                PreRegisteredUserModel(
                    number=number,
                    password_hash=PreRegisteredUserModel.hash_password(row["password"]),
                    name=row["name"],
                    tg_username=row["tg_username"] if row["tg_username"] else None,
                    phone=row["phone"] if row["phone"] else None,
                    team_number=team_number,
                    is_captain=is_captain,
                    role=role,
                )
            )

        session.add_all(users)
        await session.commit()
    print(f"✅ Загружено {len(users)} пользователей!")


async def main():
    db_config = get_db_config()
    sessionmaker = await create_sessionmaker(db_config)
    async with sessionmaker() as session:
        await import_users_from_csv("src/tools/users.csv", session)


if __name__ == "__main__":
    asyncio.run(main())
