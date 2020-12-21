from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
import config

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()
bot = Bot(token=config.API_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot,storage=storage)