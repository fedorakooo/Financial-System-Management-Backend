from fastapi import Depends
from dependency_injector.wiring import Provide, inject

from src.infrastructure.database.database_initializer import DatabaseInitializer
from src.infrastructure.dependencies.app import Application


@inject
async def app_startup(
        database_initializer: DatabaseInitializer = Depends(Provide[Application.gateways.database_initializer])
) -> None:
    await database_initializer.create_all_tables()
