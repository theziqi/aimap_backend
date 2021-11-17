from PIL import Image
import time

def crop_img(x1,x2,y1,y2,category="label",city="nanjing"):
    print((x1,y1,x2,y2))
    if city == "nanjing":
        width = 8192
        height = 8192
    elif city == "luoyang":
        width = 8192
        height = 8192
    x1_ = float(x1)
    x2_ = float(x2)
    y2_ = height - float(y1)
    y1_ = height - float(y2)
    category_src = 'imgs/origin/%s/label.png' % city if (category == 'label') else 'imgs/origin/%s/color_%s_rgba.png' % (city, category)
    img=Image.open(category_src)
    print((x1_, y1_, x2_, y2_))
    crop_img = img.crop((x1_, y1_, x2_, y2_))
    result_src = 'imgs/cropped/%s/label_%s.png' % (city, str(int(time.time()))) if(category == 'label') else 'imgs/cropped/%s/color_%s_rgba_%s.png' % (city, category, str(int(time.time())))
    crop_img.save(result_src)
    return result_src
