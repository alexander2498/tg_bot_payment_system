import config
import logging

from aiogram import Bot, types, Dispatcher, executor
from aiogram.types.message import ContentType

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)

PRICE = types.LabeledPrice(label='тестовый платеж', amount=10000)

@dp.message_handler(commands=['buy'])
async def buy(message: types.Message):
    if config.PAYMENTS_PROVIDER_TOKEN.split(':') == 'TEST':
        await bot.send_message(message.chat.id, "Тестовый платеж")

    await bot.send_invoice(message.chat.id,
                           title="Тестовый платеж",
                           description="Проверка платежеприемности",
                           provider_token=config.PAYMENTS_PROVIDER_TOKEN,
                           currency='rub',
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter='test_payment',
                           payload='test_invoice_payload'
                           )

@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)

@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    print("SUCCESSFUL PAYMENT:")
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info.items():
        print(f"{k} = {v}")
    
    await bot.send_message(message.chat.id,
                           f"Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно!",
                           )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)