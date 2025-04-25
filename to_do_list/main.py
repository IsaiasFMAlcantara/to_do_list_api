from fastapi import FastAPI
from to_do_list.routers import (
    router_home,
    router_auth
)

def create_app() -> FastAPI:
    app = FastAPI(
        title="Dashboard de gerentes",
        version="0.0.1"
    )
    app.include_router(router_auth.router)
    app.include_router(router_home.router)
    return app

app = create_app()
