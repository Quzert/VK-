import vk_api 
from vk_api import VkUpload
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import os
from image import *

# Данные
users = {} #ключ:значение
orders = [] #id, имя, номер телефона, адрес, корзина
menu = {
        'Солянка':'001',
        'Салат Сельдь под шубой':'002',
        'Салат Цезарь с цыпленком':'003',
        'Салат Оливье с курицей':'004',
        'Крафт Бургер курица':'005',
        'Шашлый из свинины':'006',
        'Рубленый стейк':'007',
        'Мохито':'008',
        'Морс клюквенный':'009',
        'Какао':'010'
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
vk_session = vk_api.VkApi(token="vk1.a.DuSUTm5V1Nwp9TAY6h5WRjxu4FIJCrAZaK3utrREhPRLFfNTg2Vqlgym3f-22yFdbjGxInNcUfHmLgebq_cSVhMR2Dd34ytVZCYIOOz-z8vFmUp0ZktDrfgAxW2nHTpdDd7gktWiKben-0_5tXfoJEFy1EleOqM_xQvOJL5C0K3hm-890volf05eK74mc85rwnaGM1Mv2cfUGsiuPua0Dg")
session_api = vk_session.get_api()
upload = VkUpload(vk_session)

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
    if d:
        os.remove(img)

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
    keyboard.add_button('Посмотреть корзину', color='positive')



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
        print(pos)    
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
    data = (msg.replace('.', '').replace('заказ ', '')).split(',')
    orders.append([id,data[2],data[1],data[0],users[id]])
    send_msg('Заказ успешно сформирован.',id)
    send_msg('Дожидайтесь звонка оператора, он свяжется с вами для подтверждения заказа.',id)


def check_bask(id):
    '''
    Отправляет картинку с содержимым корзины пользователю id
    '''
    if id in users.keys():
        keyboard = VkKeyboard(inline=True)
        keyboard.add_button('Посмотреть меню', color='positive')
        keyboard.add_line()
        keyboard.add_button('Сделать заказ', color='positive')
        img = gen_bask_img(users[id],id)
        for i in range(len(img)):
            send_img(img[i],id)
        sum = 0
        for i in range(len(users[id])):
            sum += price[users[id][i][0]] * users[id][i][1]
        send_msg(('Итог: ' + str(sum) + 'Р'), id, keyboard)
    else:
        keyboard = VkKeyboard(inline=True)
        keyboard.add_button('Посмотреть меню', color='positive')
        send_msg('Ваша корзина пуста.', id, keyboard)
    