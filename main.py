import vk_api 
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from PIL import Image,ImageDraw, ImageFont
from math import *
from random import randint
import os

# Подключение бота
vk_session = vk_api.VkApi(token="vk1.a.DuSUTm5V1Nwp9TAY6h5WRjxu4FIJCrAZaK3utrREhPRLFfNTg2Vqlgym3f-22yFdbjGxInNcUfHmLgebq_cSVhMR2Dd34ytVZCYIOOz-z8vFmUp0ZktDrfgAxW2nHTpdDd7gktWiKben-0_5tXfoJEFy1EleOqM_xQvOJL5C0K3hm-890volf05eK74mc85rwnaGM1Mv2cfUGsiuPua0Dg")
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
upload = VkUpload(vk_session)
users = {} #ключ:значение
orders = [] #id, имя, номер телефона, адрес, корзина
menu = {
        '001':'Рыба',
        '002':'Катлета',
        '003':'Пюре',
        '004':'Лапша по флотский',
        '005':'Лапша по флотский',
        '006':'Лапша по флотский',
        '007':'Лапша по флотский',
        '008':'Лапша по флотский',
        '009':'Лапша по флотский',
        '010':'Лапша по флотский'
    }

try:
    os.mkdir('newimgs')
except:
    print('1')

def send_msg(text,id):
    '''
    Отправка сообщений с текстом text пользователю id
    '''
    vk_session.method("messages.send", {"user_id":id, "message":text, "random_id":0})


def send_img(img,id):
    att = []
    upload_img = upload.photo_messages(photos=img)[0]
    att.append('photo{}_{}'.format(upload_img['owner_id'],upload_img['id']))
    vk_session.method("messages.send", {"user_id":id, "random_id":0, 'attachment': ','.join(att)})
    os.remove(img)
    

def get_menu(id):
    '''
    Отправляет меню пользователю id
    '''
    ret = 'Чтобы добавить в корзину напиште ПОЗИЦИЯ и номер блюда. \nПример ПОЗИЦИЯ 2 \nСегодня в меню\n'
    for i in range(len(menu)):
        ret = ret + str(i+1) + ") " + str(menu[i]) + '\n'
    send_msg(ret,id)


def add_bask(id,val):
    '''
    Обработка добавление в корзину позиции val(значение словаря users) ,пользователя id(ключ словаря users). 
    Если пользователя не существует, то добавление пользователя и позиции заказа
    ''' 
    try:
        pos = str(val.split(' ')[-1])    
        print(pos)    
        if pos not in menu.keys():
            send_msg('Такого блюда у нас нет, пожалуйста выбирайте из меню.',id)
            return 0
        if id in users:
            for i in range(len(users[id])):
                if users[id][i][0] == pos:
                    users[id][i][1] += 1
                    send_msg('Позиция успешно добавлена.',id)
                    return 0 
            users[id].append([pos,1])
            send_msg('Позиция успешно добавлена.',id)
            return 0
        else:
            users[id] = [[pos,1]]
            send_msg('Позиция успешно добавлена.',id)
    except:
        send_msg('Такого блюда у нас нет, пожалуйста выбирайте из меню.',id)


def order(msg,id):
    '''
    Формирует заказ в списоке orders из сообщения пользователя msg и корзины пользователя id
    '''
    data = (msg.replace('.', '').replace('заказ ', '')).split(',')
    orders.append([id,data[2],data[1],data[0],users[id]])
    send_msg('Заказ успешно сформирован.',id)


def gen_bask_img(bask,id):
    '''
    Функция принимает список товаров back и генерирует картинку с изображением товаров, которую сохраняет в папку newimgs.
    Возвращает список с путями изображений путь по которому можно получить это изображение
    '''

    count_imgs = len(bask)
    it = 0
    pos = [(0,0),(0,200),(0,400),(0,600)]
    name_imgs = []
    font = ImageFont.truetype('Roboto.ttf', size=50)

    while count_imgs > 0:
        imgs = []
        if count_imgs >= 4:
            count_it = 4
        else :
            count_it = count_imgs

        for i in range(count_it):
            imgs.append(Image.open(('img/dish' + str(bask[i + 4 * it][0]) + '.jpg')))
            
        new_img = Image.new('RGB', (800,800), (250,250,250))

        for i in range(len(imgs)):
            new_img.paste(imgs[i],pos[i])
            draw_text = ImageDraw.Draw(new_img)
            draw_text.text((pos[i][0] + 700, pos[i][1] +  140), ('x' + str(bask[i][1])),font = font,fill=('#1C0606'))
        
        name = "newimgs/bask" + str(id) + str(randint(0,1000)) + ".png"
        new_img.save(name, "PNG")
        name_imgs.append(name)
        it += 1
        count_imgs -= 4

    return name_imgs


def check_bask(id):
    try:
        img = gen_bask_img(users[id],id)
        for i in range(len(img)):
            send_img(img[i],id)
    except:
        send_msg('Ваша корзина пуста.',id)


# Обработка ивентов
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:

            msg = event.text.lower()
            id = event.user_id
            print(msg,id)

            # Обработка сообщений
            if msg == 'привет':
                send_msg('Привет пользователь, я тестовый бот для заказа доставки еды. Пожалуйста выбеде один из следующих пунктов.',id)
                send_msg('Посмотреть меню.',id)
                send_msg('Посмотреть корзину.',id)
                send_msg('Сделать заказ.',id)
            
            elif msg == 'посмотреть меню':
                get_menu(id)

            elif msg == 'сделать заказ':
                send_msg('Нипишите ЗАКАЗ и через запятую адрес, номер телефона для подтверждения заказа и связи курьера, ваше имя.',id)
                send_msg('Пример: \nЗАКАЗ Ул.______, +79999999999, Иван.',id)
                send_msg('Коментарий к заказу можете сказать оператору при подтверждении заказа.',id)
            elif msg == 'посмотреть корзину':
                check_bask(id)
                
            else:
                if msg.split()[0] == 'заказ':
                    order(msg,id)
                    print(orders)
                elif msg.split()[0] == 'позиция':
                    add_bask(id, msg)
                    print(users)
