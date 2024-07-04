import logging

import sentry_sdk
import uvloop
from telegram.ext import Application, ApplicationBuilder

from settings import settings
from telegram_bot.handlers import create_handlers


def config_logging():
    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=settings.log_level)


def config_sentry():
    if settings.sentry_dsn:
        sentry_sdk.init(
            dsn=settings.sentry_dsn,
            traces_sample_rate=1.0,
            profiles_sample_rate=1.0,
        )


def create_app() -> Application:
    app = ApplicationBuilder().token(settings.bot_token).build()
    [app.add_handler(handler) for handler in create_handlers()]
    return app


if __name__ == "__main__":
    config_logging()
    uvloop.install()
    config_sentry()
    app = create_app()
    app.run_polling()
