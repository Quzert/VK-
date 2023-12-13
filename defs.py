import vk_api 
from vk_api import VkUpload
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import os
from image import *

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

# Подключение бота
vk_session = vk_api.VkApi(token="vk1.a.DuSUTm5V1Nwp9TAY6h5WRjxu4FIJCrAZaK3utrREhPRLFfNTg2Vqlgym3f-22yFdbjGxInNcUfHmLgebq_cSVhMR2Dd34ytVZCYIOOz-z8vFmUp0ZktDrfgAxW2nHTpdDd7gktWiKben-0_5tXfoJEFy1EleOqM_xQvOJL5C0K3hm-890volf05eK74mc85rwnaGM1Mv2cfUGsiuPua0Dg")
session_api = vk_session.get_api()
upload = VkUpload(vk_session)

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