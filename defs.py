import vk_api 
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import os

from image import *

# Данные
users = {} #ключ:значение
orders = [] #id, имя, номер телефона, адрес, корзина
menu = {
        'солянка':'001',
        'салат сельдь под шубой':'002',
        'салат цезарь с цыпленком':'003',
        'салат оливье с курицей':'004',
        'крафт бургер курица':'005',
        'шашлый из свинины':'006',
        'рубленый стейк':'007',
        'мохито':'008',
        'морс клюквенный':'009',
        'какао':'010'
    }
price = {
        '001': 229,
        '002': 189,
        '003': 249,
        '004': 219,
        '005': 439,
        '006': 549,
        '007': 549,
        '008': 139,
        '009': 159,
        '010': 359
    }

# Подключение бота
vk_session = vk_api.VkApi(token="vk1.a.ASyNNLaODkng8BC1N4SK8tHnWmMlAOOtHcS94UyWrGFwE5XtoIIvd3kbz8ip0IBac-v6lwg01qiA8yrKhenyJbgA2GabF7fi5fTm5PdH-ixz1gm8_VGehHjWp5bTLv5zcpXWEj9Lx-tJGGuumhRO950-lGAC_DSK7phuIwMpV4RP0sVdB20hSSdrSA3_eIF7UatTHxwVn3LZMRKrozSyYw")
session_api = vk_session.get_api()
upload = VkUpload(vk_session)
longpoll = VkLongPoll(vk_session)

def find_key_by_value(dictionary, value):
    for key, val in dictionary.items():
        if val == value:
            return key
    return None

def proc(event):
    msg = event.text.lower()
    id = event.user_id
    print(msg,'by',id)

     # Обработка сообщений
    if msg in menu.keys():
        add_bask(id, msg)
        print(users)
    
    elif msg == 'привет' or msg == 'начать':
        keyboard = VkKeyboard()
        keyboard.add_button('Меню' , color='positive')
        keyboard.add_line()
        keyboard.add_button('Корзина', color='secondary')
        keyboard.add_line()
        keyboard.add_button('Сделать заказ', color='primary')
        send_msg('Привет пользователь, я тестовый бот для заказа доставки еды. Пожалуйста выбеде один из следующих пунктов.',id,keyboard)

    elif msg == 'меню':
        get_menu(id)

    elif msg == 'сделать заказ':
        send_msg('Нипишите ЗАКАЗ и через запятую адрес, номер телефона для подтверждения заказа и связи курьера, ваше имя.',id)
        send_msg('Пример: \nЗАКАЗ Ул.______, +79999999999, Иван.',id)
        send_msg('Коментарий к заказу можете сказать оператору при подтверждении заказа.',id)

    elif msg == 'корзина':
        check_bask(id)
        
    else:
        if msg.split()[0] == 'заказ':
            order(msg,id)
        elif msg.split()[0] == 'убрать':
            del_pos(msg,id)


def send_msg(text, id, kb = None):
    '''
    Отправка сообщений с текстом text пользователю id
    '''
    post = {
            "user_id":id, 
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
    """
    if d:
        os.remove(img)
    """
    
def get_menu(id):
    '''
    Отправляет меню пользователю id
    '''
    # Клавиатура
    keyboard = VkKeyboard()
    keyboard.add_button('Солянка', color='primary')
    keyboard.add_button('Салат Сельдь под шубой', color='primary')
    keyboard.add_line()
    keyboard.add_button('Салат Цезарь с цыпленком', color='primary')
    keyboard.add_button('Салат Оливье с курицей', color='primary')
    keyboard.add_line()
    keyboard.add_button('Крафт Бургер курица', color='primary')
    keyboard.add_button('Шашлый из свинины', color='primary')
    keyboard.add_line()
    keyboard.add_button('Рубленый стейк', color='primary')
    keyboard.add_button('Мохито', color='primary')
    keyboard.add_line()
    keyboard.add_button('Морс клюквенный', color='primary')
    keyboard.add_button('Какао', color='primary') 
    keyboard.add_line()
    keyboard.add_button('Корзина', color='positive')



    send_msg('Сегодня в меню:',id,keyboard)
    send_img('img/menu1.png',id,False) 
    send_img('img/menu2.png',id,False) 
    send_img('img/menu3.png',id,False)   


def add_bask(id,pos):
    '''
    Обработка добавление в корзину позиции val(значение словаря users) ,пользователя id(ключ словаря users). 
    Если пользователя не существует, то добавление пользователя и позиции заказа
    ''' 
    if pos in menu.keys():   
        if id in users:
            for i in range(len(users[id])):
                if users[id][i][0] == menu[pos]:
                    users[id][i][1] += 1
                    send_msg('Позиция успешно добавлена.',id)
                    return 0 
            users[id].append([menu[pos],1])
            send_msg('Позиция успешно добавлена.',id)
            return 0
        else:
            users[id] = [[menu[pos],1]]
            send_msg('Позиция успешно добавлена.',id)
    else:
        send_msg('Такого блюда у нас нет, пожалуйста выбирайте из меню.',id)
    


def order(msg,id):
    '''
    Формирует заказ в списоке orders из сообщения пользователя msg и корзины пользователя id
    '''
    if not(id in users) or (users[id] == []):
        keyboard = VkKeyboard(inline=True)
        keyboard.add_button('меню', color='positive')
        send_msg('Не удалось оформить заказ. Ваша корзина пуста.', id, keyboard)
        return 0
    data = (msg.replace('.', '').replace('заказ ', '')).split(',')
    orders.append([id,data[2],data[1],data[0],users[id]])
    send_msg('Заказ успешно сформирован.',id)
    send_msg('Дожидайтесь звонка оператора, он свяжется с вами для подтверждения заказа.',id)


def check_bask(id):
    '''
    Отправляет картинку с содержимым корзины пользователю id
    '''
    if id in users.keys():
        buttons = []
        for i in range(len(users[id])):
            buttons.append(find_key_by_value(menu,users[id][i][0]))

        img = gen_bask_img(users[id],id)
        for i in range(len(img)):
            send_img(img[i],id)
        sum = 0
        for i in range(len(users[id])):
            sum += price[users[id][i][0]] * users[id][i][1]

        keyboard = VkKeyboard()
        
        l = 0
        for i in buttons:
            if l == 2:
                keyboard.add_line()
                l = 0
            l += 1
            keyboard.add_button(str('убрать ' + i),color='negative')
        keyboard.add_line()
        keyboard.add_button('Меню' , color='positive')
        keyboard.add_button('Корзина' , color='positive')
        keyboard.add_button('Сделать заказ', color='primary')

        send_msg(('Итог: ' + str(sum) + 'Р'), id, keyboard)
    else:
        keyboard = VkKeyboard(inline=True)
        keyboard.add_button('меню', color='positive')
        send_msg('Ваша корзина пуста.', id, keyboard)
    
def  del_pos(msg,id):
    pos = msg.split(' ', 1)[1]
    if len(users[id]) == 0:
        keyboard = VkKeyboard(inline=True)
        keyboard.add_button('меню', color='positive')
        send_msg('Ваша корзина пуста.', id, keyboard)  
        return 0   
      
    for i in range(len(users[id])):
        if users[id][i][0] == menu[pos]:
            users[id][i][1] -= 1
            send_msg(f'Позиция "{pos.title()}" успешно удалена.',id)
            if users[id][i][1] == 0:
                users[id].pop(i)
            break
        elif i+1 == len(users[id]):
            send_msg('Такой позиции нет.',id)  
    print(users[id])

def gen_keyboard(buttons):
    keyboard = VkKeyboard()
    l = 0
    for i in range(len(buttons)):
        l += 1
        if l == 2:
            keyboard.add_line()
            l = 0
        keyboard.add_button(buttons[i],color='negative')
    return(keyboard)