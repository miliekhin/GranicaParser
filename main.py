# https://vc.ru/dev/158757-sozdanie-i-razvertyvanie-retranslyatora-telegram-kanalov-ispolzuya-python-i-heroku
# https://proglib.io/p/pishem-prostoy-grabber-dlya-telegram-chatov-na-python-2019-11-06
import sys
import os
import requests
from dotenv import load_dotenv

from telethon import TelegramClient, events
from telethon.sessions import StringSession

from processor import get_valid_data
from test_parser import run_tests

load_dotenv()  # take environment variables from .env.
api_id = os.environ.get("API_ID")
api_hash = os.environ.get("API_HASH")
sess_id = os.environ.get("SESS_ID")
SOURCE_CHANNEL = os.environ.get("SOURCE_CHANNEL")

client = TelegramClient(StringSession(sess_id), int(api_id), api_hash)


# Обработчик новых сообщений
@client.on(events.NewMessage(chats='granicaRF2DPR'))
async def handler_new_message(event):
    try:
        # event.message содержит информацию о новом сообщении
        # print(event)
        print(f'\n--------------------------------\n{event.message.date}: {event.message.message}')
        data = get_valid_data(event.message.message)
        # if data:
        #     data = json.dumps(data)

        if data:
            print('Sending request...')
            r = requests.post('http://kppshka:8000/api/v1/telega_parser/', data=data)
            print('Response:', r)

            if data['cars_num'] > 128:
                print('Sending warning to MSGS group')
                ent = await client.get_entity('MSGS')
                print('Entity:', ent)
                await client.send_message(entity=ent, message=event.message.message)

    except Exception as e:
        print(e)


# async def main():
#     channel = await client.get_entity('https://t.me/granicaRF2DPR')
#     print(channel.stringify())


if __name__ == '__main__':

    if len(sys.argv) > 1 and sys.argv[1] == 'tests':
        run_tests()
    else:
        print(f'\n--------------------------------\nGranica parser launched!')
        client.start()
        client.run_until_disconnected()

    # datad = get_valid_data('Три экипажа дпс После кольца кургана')
    # print(datad)

    # palka_detector('Успенка Рф-днр 14-18 машин перед шлакбаумом.')

    # dat = dict()
    # dat['car_type'] = 0
    # dat['comment'] = 'Каментос'
    # dat['cars_num'] = 2
    # dat['kpp_name'] = 'Успенка'
    # dat['way'] = 'to_rf'
    # r = requests.post('http://kppshka:8000/api/v1/telega_parser/', data=dat)
    # print('Response:', r)
