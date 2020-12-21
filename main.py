from aiogram.utils import executor
from dataBase import study
from loader import dp
import handlers
db = study('education')

if __name__=='__main__':

    executor.start_polling(dp,skip_updates=True)#,on_startup=send_to_admin)
