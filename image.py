from PIL import Image,ImageDraw, ImageFont
from math import *
from random import randint

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
