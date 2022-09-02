# !pip install pytelegrambotapi
# !pip install khayyam
import telebot
import requests
from requests import Request, Session
import json
import pprint
from telebot import types

S = '----------------------------------------'

bot = telebot.TeleBot('your-bot-token')

url = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest"
headers = {'accepts':'application/json','X-CMC_PRO_API_KEY':'e9ac1dae-19ad-4471-85f3-a781e418ab96'}
session = Session()
session.headers.update(headers)

keyboard1 = types.InlineKeyboardMarkup()
binance = types.InlineKeyboardButton('Binance', url='https://www.binance.com/en')
coinmarketcap = types.InlineKeyboardButton('Coinmarketcap', url='https://coinmarketcap.com')
keyboard1.add(binance).add(coinmarketcap)

keyboard3 = types.InlineKeyboardMarkup()
btc = types.InlineKeyboardButton('BTC', callback_data='btc')
eth = types.InlineKeyboardButton('ETH', callback_data='eth')
usdt = types.InlineKeyboardButton('USDT', callback_data='usdt')
usdc = types.InlineKeyboardButton('USDC', callback_data='usdc')
bnb = types.InlineKeyboardButton('BNB', callback_data='bnb')
ada = types.InlineKeyboardButton('ADA', callback_data='ada')
xrp = types.InlineKeyboardButton('XRP', callback_data='xrp')
busd = types.InlineKeyboardButton('BUSD', callback_data='busd')
sol = types.InlineKeyboardButton('SOL', callback_data='sol')
doge = types.InlineKeyboardButton('DOGE', callback_data='doge')
dot = types.InlineKeyboardButton('DOT', callback_data='dot')
shib = types.InlineKeyboardButton('SHIB', callback_data='shib')
dai = types.InlineKeyboardButton('DAI', callback_data='dai')
avax = types.InlineKeyboardButton('AVAX', callback_data='avax')
matic = types.InlineKeyboardButton('MATIC', callback_data='matic')
trx = types.InlineKeyboardButton('TRX', callback_data='trx')
wbtc = types.InlineKeyboardButton('WBTC', callback_data='wbtc')
uni = types.InlineKeyboardButton('UNI', callback_data='uni')
leo = types.InlineKeyboardButton('LEO', callback_data='leo')
etc = types.InlineKeyboardButton('ETC', callback_data='etc')
ltc = types.InlineKeyboardButton('LTC', callback_data='ltc')
ftt = types.InlineKeyboardButton('FTT', callback_data='ftt')
near = types.InlineKeyboardButton('NEAR', callback_data='near')
link = types.InlineKeyboardButton('LINK', callback_data='link')
back = types.InlineKeyboardButton('Back', callback_data='back')
keyboard3.add(btc, eth, usdt).add(usdc, bnb, ada).add(xrp, busd, sol).add(doge, dot, shib).add(dai, avax, matic).add(trx, wbtc, uni).add(leo, etc, ltc).add(ftt, near, link).add(back)

keyboard4 = types.InlineKeyboardMarkup()
crypto = types.InlineKeyboardButton('Cryptocurrency', callback_data='cryptocurrency')
stocks = types.InlineKeyboardButton('Stocks', callback_data='stocks')
keyboard4.add(crypto).add(stocks)


@bot.message_handler(commands=['start', 'help', 'price', 'website', 'donate'])
def commands(message):
    if message.text == '/start':
        bot.send_message(message.chat.id, 'Hi!, Im a Telegram bot./help\nPowered by telebot(PyTelegramBotApi)')
    
    elif message.text == '/help':
        bot.send_message(message.chat.id, 'Use the following options\n\n/price - cryptocurrency price\n/website - popular finance website\n/donate - donate')

    elif message.text == '/price':
        bot.send_message(message.chat.id, 'Select your option', reply_markup=keyboard4)

    elif message.text == '/website':
        bot.send_message(message.chat.id, f'{S}\nTap to open\n{S}', reply_markup=keyboard1)

    elif message.text == '/donate':
        bot.send_message(message.chat.id, 'My Wallet\n\n*BTC*:\n`bc1qrv8hfn2dkeav8jd95xned46menrx9mfwg4272f`\n\n*BNB*:\n`bnb1ds9l7jds3qy529we3mfve79wswrkvaetw9tuu3`\n\n*BCH*:\n`qrjlp3y6kgcmfdhh8zar4sp4xwp54twt5cvt5sgrne`\n\n*USDT*:\n`TMy1YrCULSqqex1P9wsCAAHtuHsKUjKxfo`',
            parse_mode='MarkDown',)

@bot.message_handler()
def manual_price_answer(message):
    try:
        s = message.text
        parameters = {'symbol':f'{s}','convert':'USD'}
        response = session.get(url, params=parameters)
        price = json.loads(response.text)['data'][f'{s.upper()}'][0]['quote']['USD']['price']
        name = json.loads(response.text)['data'][f'{s.upper()}'][0]['name']
        bot.reply_to(message, f'{name} : `{price}`', parse_mode='MarkDown')

    except(IndexError):
        if len(message.text) <= 5:
            bot.reply_to(message, 'This cryptocurrency does not exist. /help')
        else:
            bot.reply_to(message, '👇 Use the command menu. /help')

    except(KeyError):
        bot.reply_to(message, '👇 Use the command menu. /help')

@bot.callback_query_handler(func=lambda call:True)
def call_answer(call):
    S = '----------------------------------------'

    if call.data == 'cryptocurrency':
        bot.edit_message_text(f'{S}\nChoose or type Symbol\n{S}',
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=keyboard3)

    elif call.data == 'stocks':
        bot.answer_callback_query(call.id, 'Not set YET!')

    elif call.data == 'back':
        bot.edit_message_text('Select your option',
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=keyboard4)
        
    else:
        s = call.data
        parameters = {'symbol':f'{s}','convert':'USD'}
        response = session.get(url, params=parameters)
        name = json.loads(response.text)['data'][f'{s.upper()}'][0]['name']
        price = json.loads(response.text)['data'][f'{s.upper()}'][0]['quote']['USD']['price']
        bot.edit_message_text(f'{S}\n{name} : `{price}`\n{S}',
                            chat_id=call.message.chat.id,
                            message_id=call.message.message_id,
                            parse_mode='MarkDown',
                            reply_markup=keyboard3)

print('Runing...')
bot.infinity_polling()
