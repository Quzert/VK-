import vk_api 
from image import *
from defs import *
from vk_api.longpoll import VkLongPoll, VkEventType


# Подключение бота
vk_session = vk_api.VkApi(token="vk1.a.DuSUTm5V1Nwp9TAY6h5WRjxu4FIJCrAZaK3utrREhPRLFfNTg2Vqlgym3f-22yFdbjGxInNcUfHmLgebq_cSVhMR2Dd34ytVZCYIOOz-z8vFmUp0ZktDrfgAxW2nHTpdDd7gktWiKben-0_5tXfoJEFy1EleOqM_xQvOJL5C0K3hm-890volf05eK74mc85rwnaGM1Mv2cfUGsiuPua0Dg")
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
upload = VkUpload(vk_session)


# Создание директорий
try:
    os.mkdir('newimgs')
    print('newimgs was created')
except:
    print('Done')
 

# Обработка ивентов
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:

            msg = event.text.lower()
            orig_msg = event.text
            id = event.user_id
            print(msg,'by',id)

            # Обработка сообщений
            if orig_msg in menu.keys():
                add_bask(id, orig_msg)
                print(users)
            
            elif msg == 'привет':
                keyboard = VkKeyboard()
                keyboard.add_button('Посмотреть меню' , color='positive')
                keyboard.add_line()
                keyboard.add_button('Посмотреть корзину', color='secondary')
                keyboard.add_line()
                keyboard.add_button('Сделать заказ', color='primary')
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
