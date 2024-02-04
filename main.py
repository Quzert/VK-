import threading
from image import *
from defs import *


# Создание папок
try:
    os.mkdir('newimgs')
    print('newimgs was created')
except:
    print('Done')
 

# Обработка ивентов
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        threading.Thread(target=proc, args=(event,), name= str(event.user_id)).start()