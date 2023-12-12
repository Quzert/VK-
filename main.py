import vk_api 
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api import VkUpload
from PIL import Image,ImageDraw, ImageFont
from math import *
from random import randint
import os


# Подключение бота
vk_session = vk_api.VkApi(token="vk1.a.DuSUTm5V1Nwp9TAY6h5WRjxu4FIJCrAZaK3utrREhPRLFfNTg2Vqlgym3f-22yFdbjGxInNcUfHmLgebq_cSVhMR2Dd34ytVZCYIOOz-z8vFmUp0ZktDrfgAxW2nHTpdDd7gktWiKben-0_5tXfoJEFy1EleOqM_xQvOJL5C0K3hm-890volf05eK74mc85rwnaGM1Mv2cfUGsiuPua0Dg")
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
upload = VkUpload(vk_session)

# Данные
users = {} #ключ:значение
orders = [] #id, имя, номер телефона, адрес, корзина
menu = {
        '001':['Солянка',229],
        '002':['Салат Сельдь под шубой',189],
        '003':['Салат Цезарь с цыпленком',249],
        '004':['Салат Оливье с курицей',219],
        '005':['Крафт Бургер курица',439],
        '006':['Шашлый из свинины',549],
        '007':['Рубленый стейк',549],
        '008':['Мохто',139],
        '009':['Морс клюквенный',159],
        '010':['Какао',359]
    }

# Создание директорий
try:
    os.mkdir('newimgs')
    print('newimgs was created')
except:
    print('Done')


# Функции
def send_msg(text,id,kb = None):
    '''
    Отправка сообщений с текстом text пользователю id
    '''
    post = {"user_id":id, 
            "message":text, 
            "random_id":0
            }
    if kb != None:
        post["keyboard"] =kb.get_keyboard() 
    else:
        post = post

    vk_session.method("messages.send", post)


def send_img(img,id,d = True):
    '''
    Отправка изображения расположенному по пути img, пользователю
    '''
    att = []
    upload_img = upload.photo_messages(photos=img)[0]
    att.append('photo{}_{}'.format(upload_img['owner_id'],upload_img['id']))
    vk_session.method("messages.send", {"user_id":id, "random_id":0, 'attachment': ','.join(att)})
    if d:
        os.remove(img)
    

def get_menu(id):
    '''
    Отправляет меню пользователю id
    '''
    send_msg('Сегодня в меню:',id)
    send_img('img/menu1.png',id,False)   #костыль
    send_img('img/menu2.png',id,False)   #сделать перебор меню
    send_img('img/menu3.png',id,False)   #НОРМАЛЬНЫЙ!!!!!!!!!


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
        if count_imgs == 1:
            new_img = Image.new('RGB', (800,400), (250,250,250)) 
        elif count_imgs < 4:
            new_img = Image.new('RGB', (800,200 * count_imgs), (250,250,250)) 
        else:
            new_img = Image.new('RGB', (800,800), (250,250,250))

        for i in range(len(imgs)):
            new_img.paste(imgs[i],pos[i])
            draw_text = ImageDraw.Draw(new_img)
            draw_text.text((pos[i][0] + 700, pos[i][1] +  140), ('x' + str(bask[i][1])),font = font,fill=('#1C0606'))
        
        name = "newimgs/bask" + str(id) + str(randint(0,1000000)) + ".png"
        new_img.save(name, "PNG")
        name_imgs.append(name)
        it += 1
        count_imgs -= 4

    return name_imgs


def check_bask(id):
    '''
    Отправляет картинку с содержимым корзины пользователю id
    '''
    try:
        img = gen_bask_img(users[id],id)
        for i in range(len(img)):
            send_img(img[i],id)
        sum = 0
        for i in range(len(users[id])):
            sum += menu[users[id][i][0]][1] * users[id][i][1]
        send_msg(('Итог: ' + str(sum) + 'Р'),id)
    except Exception as e:
        print(e)
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
                keyboard = VkKeyboard(inline=True)
                keyboard.add_button('Посмотреть меню')
                keyboard.add_line()
                keyboard.add_button('Посмотреть корзину')
                keyboard.add_line()
                keyboard.add_button('Сделать заказ')

                send_msg('Привет пользователь, я тестовый бот для заказа доставки еды. Пожалуйста выбеде один из следующих пунктов.',id,keyboard)

                
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
