import asyncio

from mpets import MpetsApi
import random
import time

async def main(name, password, rucaptcha_api):
    mpets = MpetsApi(name=name, password=password, rucaptcha_api=rucaptcha_api, timeout=5, fast_mode=True)
    resp = await mpets.login()
    if resp.status is False:
        print("Не удалось авторизоваться.")
    while True:
        time.sleep(3)
        mailresp = await mpets.view_posters()
        if mailresp.status is False:
            continue
        for mail in mailresp.players:
            if mail.unread == True:
                mailcheck = await mpets.post_message(mail.pet_id)
                if mailcheck['status'] is False:
                    continue
                print("mail", mailcheck)
                if "Старт" in mailcheck['messages'][0]['text']:
                    mailsend = await mpets.post_send("Добро пожаловать! Я помогаю проводить Мафию в режиме "
                                                     "«как в разрушителях». Отправьте слово «ИГРА», "
                                                     "чтобы начать (обязательно КАПСОМ, я иначе не пойму) " + ":]" * random.randint(1,10), mail.pet_id)
                if "ИГРА" in mailcheck['messages'][0]['text']:
                    mailsend = await mpets.post_send("Напишите названия ролей и их количество в игре. "
                                                     "Формат: название роли:количество человек на роли. "
                                                     "Укажите в начале «СПИСОК РОЛЕЙ», чтобы я понял, что Вы хотите добавить "
                                                     "роли!"
                                                     "\n"
                                                     "\n"
                                                     "Пример:\n"
                                                     "СПИСОК РОЛЕЙ\n"
                                                     "1. Мирный житель:4\n"
                                                     "2. Мафия:3\n"
                                                     "3. Комиссар:1\n"
                                                     "4. Доктор:1\n"
                                                     "5. Горожанка:1\n"
                                                     "\n"
                                                     "\n"
                                                     "Жду Вашего ответа с нетерпением" + ":-)" * random.randint(1, 10), mail.pet_id)
                if "СПИСОК РОЛЕЙ" in mailcheck['messages'][0]['text']:
                    temp = mailcheck['messages'][0]['text']
                    temp = temp.split("\n")[1:]
                    text = "Итак, вот список ролей по номерам:\n"
                    counter = 1
                    tmp = []
                    for i in temp:
                            try:
                                n_c = i.split(". ")[1].split(":")
                                for i in range(0, int(n_c[1])):
                                    tmp.append([n_c[0]])
                            except:
                                pass
                    random.shuffle(tmp)
                    for i in tmp:
                        text += f"{counter}. {i[0]} \n"
                        counter += 1
                    text += "  " * random.randint(1,100)
                    mailsend = await mpets.post_send(text, pet_id=mail.pet_id)


if __name__ == '__main__':
    name = "PET NAME"
    password = "PET PASSWORD"
    rucaptcha_api = "API RUCAPTCHA"
    asyncio.run(main(name=name,
                     password=password,
                     rucaptcha_api=rucaptcha_api))
