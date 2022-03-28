

# # 中国农业大学_基于深度学习的植物营养缺乏检测研究与系统构建 

import os
from flask import Flask, request
from werkzeug.utils import secure_filename
from weplant_predict import main


current_dir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = current_dir + "/static/uploads"
BANNER_PATH = os.path.join("/static", "cau.png")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route('/')
def project_info():
    return '''
        <!doctype html>
        <link rel="icon" href="https://www.cau.edu.cn/images/1182/xiaohui.png" sizes="16x16">
        <div style="text-align: center; margin: 0 auto;" >
            <title>中国农业大学🐂🍺 </title>
            <img src='%s'></img>
            <h2> 基于深度学习的植物营养缺乏检测研究与系统构建  </h2>
            <a href='%s/upload' > 👉 GAME START </a>
        </div>
    ''' % (BANNER_PATH, request.url)

def allowed_file(filename):
    return '.' in filename and \
          filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST', 'GET'])
def upload_file():
    if(request.method == "POST"):
        if 'file' not in request.files:
            return "你发来的文件就像我的♥ 一样空 -_-!"
        file = request.files['file']
        if file.filename == '':
            return "你的文件名? :) "
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], "test.jpg"))
            return '''
                <!doctype html>
                <div style="text-align: center; margin: 0 auto;" >
                    <title>leimu</title>
                    <h2>Save %s success! Good job! </h2>
                    <a href='http://flask-u1x8-1752743-1306451594.ap-shanghai.run.tcloudbase.com/main' > 👉 VIEW RESULT </a>
                </div>
            ''' % (filename)
        else:
            return "Just support photo！防呆不防傻!😕 "
    else:
        return '''
            <!doctype html>
            <link rel="icon" href="https://www.cau.edu.cn/images/1182/xiaohui.png" sizes="16x16">
            <title>图片上传</title>
            <h1>请上传一张图片(●'◡'●) Please solo, don't group!</h1>
            <form method=post enctype=multipart/form-data>
              <input type=file name=file>
              <input type=submit value=Upload>
            </form>
        '''


@app.route('/main', methods=['GET'])
def main_predict():
    url = request.args['url']
    return main(url)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)