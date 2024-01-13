import vk_api 
from image import *
from defs import *
from vk_api.longpoll import VkLongPoll, VkEventType
import threading



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
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        threading.Thread(target=proc, args=(event,), name= str(event.user_id)).start()