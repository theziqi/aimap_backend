import os
import numpy as np
import cv2
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签

color_2_cls = {
    (0, 0, 0): 0,
    (255, 20, 147): 1,
    (205, 92, 92): 2,
    (0, 191, 255): 3,
    (178, 34, 34): 4,
    (72, 61, 139): 5,
    (0, 255, 0): 6,
    (255, 215, 0): 7,
    (50, 0, 150): 8,
}

def calculate_class(img: Image, class_list: list):
    '''
    :param img: 要统计的图片
    :param class_list: 对应的类别列表
    :return: 返回一个列表，存放每个类别（像素）对应的占比
    '''
    if not isinstance(img, np.ndarray):
        img = np.array(img)
    # H, W = img.shape  # 这里需要img是二维的
    H, W = img.shape[0], img.shape[1]  # 这里不严格限制img是二维的但是需要其格式为[H, W, ...]
    total_pixel = H * W
    res = []
    for cls in class_list:
        count = sum(sum(img == cls))  # 这里没有给定维度，所以第一个sum是默认维度上sum
        # res.append(count / total_pixel)
        res.append(count)
    return res  # 这里的res的顺序要完全对应于class_list的顺序

def color_to_gray(color_img_file, save_file, bg_value=(0, 0, 0)):
    color_img = np.array(Image.open(color_img_file))
    gray_img = np.zeros((color_img.shape[0], color_img.shape[1]), dtype=np.uint8)
    for cls_color in color_2_cls:
        gray_img[np.logical_and(color_img[:, :, 0] == cls_color[0],
                                color_img[:, :, 1] == cls_color[1],
                                color_img[:, :, 2] == cls_color[2])] = color_2_cls[cls_color]

    cls_list = [color_2_cls[key] for key in color_2_cls]
    res = calculate_class(gray_img, class_list=cls_list)
    pil_gray_img = Image.fromarray(gray_img)
    pil_gray_img.save(save_file)

    return res



if __name__ == "__main__":

    lab_path = r"imgs/origin/nj_label.png"
    lab = np.array(Image.open(lab_path).convert("L"), dtype=np.uint8)
    lab_patch = lab[1024:2048+1024,3072:3072+2048]
    cls_list = [color_2_cls[key] for key in color_2_cls]
    print(cls_list)
    res = calculate_class(lab_patch, class_list=cls_list)
    print(res)

    slices = res  # 即 activities 分别占比 7/24, 2/24, 2/24, 13/24
    # activities = [
    #         "background",
    #         "barren_land",
    #         "covered_barren_land",
    #         "water",
    #         "builtup",
    #         "road",
    #         "vegetation",
    #         "farmland",
    #         "factory",
    #     ]
    activities = [
        "背景",
        "裸地",
        "苫盖",
        "水体",
        "建筑",
        "道路",
        "植被",
        "农田",
        "工厂",
    ]
    colors = np.array([[0, 0, 0], [255, 20, 147], [205, 92, 92], [0, 191, 255], [178, 34, 34],
              [72, 61, 139], [0, 255, 0], [255, 215, 0], [50, 0, 150]]) / 255.0
    color_list = colors.tolist()
    # colors = [(0.0, 0.0, 0.0), (0, 255, 0), 'm', 'r', 'b']
    fig1, ax1 = plt.subplots()
    patches, texts, autotexts = ax1.pie(slices,
                                        labels=activities,
                                        colors=color_list,
                                        startangle=90,
                                        pctdistance=0.7,
                                        radius=0.8,
                                        # shadow=True,
                                        explode=(0, 0.1, 0, 0, 0, 0, 0, 0, 0),
                                        autopct='%1.1f%%')

    # 重新设置字体大小
    proptease = fm.FontProperties()
    proptease.set_size('x-small')
    # font size include: ‘xx-small’,x-small’,'small’,'medium’,‘large’,‘x-large’,‘xx-large’ or number, e.g. '12'
    plt.setp(autotexts, fontproperties=proptease)
    plt.setp(texts, fontproperties=proptease)
    # plt.title('Interesting Graph\nCheck it out')
    fig1.set_facecolor('gray')
    plt.legend(loc="upper right",fontsize=10, bbox_to_anchor=(1.1, 1.1), borderaxespad=0.3)
    # plt.legend(loc="upper right", fontsize=10, bbox_to_anchor=(1.1, 1.05), borderaxespad=0.3)
    print_str = '各类别统计： \n背景: {}\n裸地: {}\n苫盖: {}\n水体: {}\n建筑: {}\n道路: {}\n植被: {}\n农田: {}\n工厂: {}'
    plt.title(print_str.format(res[0]*4,res[1]*4, res[2]*4, res[3]*4, res[4]*4, res[5]*4, res[6]*4, res[7]*4, res[8]*4), loc="left", x=0, y=0.8, fontsize=12)
    plt.show()


# from skimage.io import imread, imsave
# import numpy as np
# import os
# from tqdm import tqdm
# import cv2
#
# # color_2_cls = {
# #     (0, 0, 0): 0,
# #     (128, 0, 0): 1,
# #     (75, 0, 130): 2,
# #     (255, 215, 0): 3,
# #     (0, 0, 128): 4,
# #     (128, 128, 128): 5,
# #     (0, 128, 128): 6,
# #     (72, 209, 204): 7,
# #     (255, 0, 0): 8,
# #     (34, 139, 34): 9,
# #     (255, 0, 255): 10,
# # }
#
# color_2_cls = {
#     (0,200,0): 0,
#     (150,250,0): 1,
#     (150,200,150): 2,
#     (200,0,200): 3,
#     (150,0,250): 4,
#     (150,150,250): 5,
#     (250,200,0): 6,
#     (200,200,0): 7,
#     (200,0,0): 8,
#     (250,0,150): 9,
#     (200,150,150): 10,
#     (250,150,150): 11,
#     (0,0,200): 12,
#     (0,150,200): 13,
#     (0,200,250): 14,
#     (0,0,0): 15
# }
#
#
# def color_to_gray(color_img_file, save_file, bg_value=(0, 0, 0)):
#     color_img = imread(color_img_file)
#     gray_img = np.zeros((color_img.shape[0], color_img.shape[1]))
#     for i, row in enumerate(color_img):
#         for j, cell in enumerate(row):
#             if tuple(cell) in color_2_cls:
#                 gray_img[i, j] = color_2_cls[tuple(cell)]
#             else:
#                  gray_img[i, j] = color_2_cls[bg_value]
#     imsave(save_file, gray_img)
#

