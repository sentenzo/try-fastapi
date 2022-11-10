import uvicorn

from . import app
from .routers import auth, healthcheck, post, user, vote


app.include_router(healthcheck.router)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(vote.router)

if __name__ == "__main__":
    uvicorn.run("service.__main__:app", host="0.0.0.0", port=8000, reload=True)
