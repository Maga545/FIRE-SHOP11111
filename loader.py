
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import BoundFilter
from data import config
from utils.db_api.sqlite import  get_is_user_banned


# Проверка на бан
class IsBanned(BoundFilter):
    required=True
    default=1
    key='is_banned'
    reply_messages_ids = []
    def __init__(self, **kwargs):
        pass

    async def check(self, message: types.Message):
        
        is_banned = get_is_user_banned(int(message.from_user.id))
        if len(IsBanned.reply_messages_ids) > 100:
            IsBanned.reply_messages_ids = []

        if is_banned and not message.message_id in IsBanned.reply_messages_ids:
            IsBanned.reply_messages_ids.append(message.message_id)
            await message.reply('🚫 Вы были заблокированы в боте!')
        return not is_banned

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.filters_factory.bind(IsBanned,event_handlers=[dp.message_handlers])


