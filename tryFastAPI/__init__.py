try:
    import dotenv

    dotenv.load_dotenv()
except ImportError:
    pass

from tryFastAPI.__main__ import make_app, app

__all__ = [make_app, app]
