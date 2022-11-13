import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import auth, healthcheck, post, user, vote


def make_app() -> FastAPI:
    """
    Creates FastAPI app
    """
    app_ = FastAPI()

    for route in [auth, healthcheck, post, user, vote]:
        app_.include_router(route.router)

    # origins = [
    #     "http://localhost",
    #     "http://localhost:8000",
    #     "https://www.google.com",
    # ]
    origins = ["*"]  # public API

    app_.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app_


app = make_app()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
