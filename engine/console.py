import logging
import os
import asyncio
import coloredlogs

def setup_logging():
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Настраиваем обработчики для логов
    file_log = logging.FileHandler('logs/logs.txt')
    console_out = logging.StreamHandler()

    # Настраиваем логирование
    logging.basicConfig(handlers=(file_log, console_out),
                        format='[%(asctime)s | %(levelname)s] %(message)s',
                        datefmt='%d.%m.%Y %H:%M:%S',
                        level=logging.INFO)

    # Настраиваем coloredlogs
    coloredlogs.DEFAULT_FIELD_STYLES = {
        'asctime': {'color': 'blue'},
        'levelname': {'color': 'magenta', 'bold': True},
        'message': {'color': 'white'}
    }

    coloredlogs.DEFAULT_LEVEL_STYLES = {
        'info': {'color': 'green'},
        'warning': {'color': 'yellow'},
        'error': {'color': 'red', 'bold': True}
    }

    coloredlogs.install(level='INFO', fmt='[%(asctime)s | %(levelname)s] %(message)s', datefmt='%d.%m.%Y %H:%M:%S', handlers=[console_out])

    async def log(message: str) -> str:
        logging.info(message)
        return message

    async def error(message: str) -> str:
        logging.error(message)
        return message

    async def warning(message: str) -> str:
        logging.warning(message)
        return message

    globals()['log'] = log
    globals()['error'] = error
    globals()['warning'] = warning

setup_logging()