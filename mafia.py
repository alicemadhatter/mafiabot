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
                                                     "\"как в разрушителях\". Отправьте слово \"ИГРА\", "
                                                     "чтобы начать (обязательно КАПСОМ) " + ":]" * random.randint(1,10), mail.pet_id)
                if "ИГРА" in mailcheck['messages'][0]['text']:
                    mailsend = await mpets.post_send("Напишите названия ролей и их количество в игре. "
                                                     "В начале напишите \"СПИСОК РОЛЕЙ\", так я пойму, что Вы добавляете "
                                                     "роли в игру! " + ":-)" * random.randint(1, 10), mail.pet_id)
                if "СПИСОК РОЛЕЙ" in mailcheck['messages'][0]['text']:
                    temp = mailcheck['messages'][0]['text']
                    temp = temp.split("\n")[1:]
                    text = "Обнаружены следующие роли:\n"
                    counter = 1
                    tmp = []
                    for i in temp:
                        n_c = i.split(". ")[1].split(":")
                        for i in range(0, int(n_c[1])):
                            tmp.append([n_c[0]])
                    random.shuffle(tmp)
                    for i in tmp:
                        text += f"{counter}. {i[0]} \n"
                        counter += 1
                    text += "  " * random.randint(1,100)
                    mailsend = await mpets.post_send(text, pet_id=mail.pet_id)


if __name__ == '__main__':
    name = " "
    password = " "
    rucaptcha_api = " "
    asyncio.run(main(name=name,
                     password=password,
                     rucaptcha_api=rucaptcha_api))
