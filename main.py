from PIL import Image
from flask import Flask, request, jsonify
from crop import crop_img
from analysis import calculate_class
import shutil
import os
import json
import numpy
app = Flask(__name__, static_folder='imgs')
app.debug=True

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/analysis', methods=['GET'])
def analysis():
    if request.method == 'GET':
        x1 = request.args.get('x1')
        x2 = request.args.get('x2')
        y1 = request.args.get('y1')
        y2 = request.args.get('y2')
        city = request.args.get('city')
        cropped_label_src = crop_img(x1,x2,y1,y2,'label',city)
        res_list = calculate_class(Image.open(cropped_label_src),[0,1,2,3,4,5,6,7,8])
        res_list = res_list / sum(res_list) * 100
        for res in res_list:
            res = str(res)
        # res_dict = {
        #     'coordinate' : [x1,x2,y1,y2],
        #     'result' : res_list
        # }
        return json.dumps(res_list, cls=MyEncoder)

@app.route('/crop', methods=['GET'])
def crop():
    if request.method == 'GET':
        category = request.args.get('category')
        x1 = request.args.get('x1')
        x2 = request.args.get('x2')
        y1 = request.args.get('y1')
        y2 = request.args.get('y2')
        city = request.args.get('city')
        result_src = crop_img(x1,x2,y1,y2,category,city)
        return result_src

def setDir(filepath):
    '''
    如果文件夹不存在就创建，如果文件存在就清空！
    :param filepath:需要创建的文件夹路径
    :return:
    '''
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    else:
        shutil.rmtree(filepath)
        os.mkdir(filepath)

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)

if __name__ == '__main__':
    for root, dirs, files in os.walk('imgs/cropped/'):
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list
        for d in dirs:
            setDir(os.path.join(root, d))
    app.run()