from fastapi import FastAPI
from to_do_list.routers import (
    router_users,
    router_auth,
    router_home
)

app = FastAPI(
    title="To Do List",
    description="",
    version="0.0.1"
)

app.include_router(router_home.router)
app.include_router(router_auth.router)
app.include_router(router_users.router)