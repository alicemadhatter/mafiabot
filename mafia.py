import asyncio

from mpets import MpetsApi
import random
import time


async def main(name, password, rucaptcha_api):
    mpets = MpetsApi(name=name, password=password, rucaptcha_api=rucaptcha_api, timeout=5, fast_mode=True)
    resp = await mpets.login()
    while True:
        await mpets.actions(3)
        time.sleep(7200)
        mailresp = await mpets.view_posters()
        for mail in mailresp.players:
            print(mail)
            if mail.unread == True:
                mailcheck = await mpets.post_message(mail.pet_id)
                print("mail", mailcheck)
                if "Старт" in mailcheck['messages'][0]['text']:
                    mailsend = await mpets.post_send("Добро пожаловать! Я помогаю проводить Мафию в режиме "
                                                     "\"как в разрушителях\". Отправьте слово \"ИГРА\", "
                                                     "чтобы начать (обязательно КАПСОМ)" + ":]" * random.randint(1,10), mail.pet_id)
                if "ИГРА" in mailcheck['messages'][0]['text']:
                    mailsend = await mpets.post_send("Напишите названия ролей и их количество в игре."
                                                     "В начале напишите \"СПИСОК РОЛЕЙ\", так я пойму, что Вы добавляете"
                                                     "роли в игру!" + ":-)" * random.randint(1, 10), mail.pet_id)
                if "СПИСОК РОЛЕЙ" in mailcheck['messages'][0]['text']:
                    temp = mailcheck['messages'][0]['text'].split("\n")[1:]
                    temp = temp.split("\n")[1:]
                    text = "Обнаружены следующие роли:\n"
                    for i in temp:
                        text += '-'.join([*i.split(". ")[1].split(":")])
                        text += '\n'
                    mailsend = await mpets.post_send(text)


if __name__ == '__main__':
    name = "ВВЕДИТЕ СЮДА ЛОГИН ПИТОМЦА"
    password = "ВВЕДИТЕ СЮДА ПАРОЛЬ ПИТОМЦА"
    rucaptcha_api = "ВВЕДИТЕ СЮДА ТОКЕН ДОСТУПА RUCAPTCHA (если есть)"
    asyncio.run(main(name=name,
                     password=password,
                     rucaptcha_api=rucaptcha_api))