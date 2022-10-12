import uvicorn
from fastapi import FastAPI

from tryFastAPI.endpoints import all_routers


def make_app() -> FastAPI:
    app_ = FastAPI()
    # SessionLocal = make_session_local_type()
    # # Dependency
    # def get_db():
    #     db = SessionLocal()
    #     try:
    #         yield db
    #     finally:
    #         db.close()

    for router in all_routers:
        app_.include_router(router, prefix="")

    return app_


app = make_app()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
