import logging

from app.console import start_console_app

if __name__ == "__main__":
    logging.basicConfig(level=logging.CRITICAL)

    start_console_app()
