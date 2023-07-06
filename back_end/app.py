import os
import time

import speech_recognition as sr
import uuid
from flask import Flask, request, render_template
from pydub import AudioSegment
from werkzeug.utils import secure_filename

from utils.LongFormASR import ConverterApi
from db.db_api import DataBase

app = Flask(__name__)
recognizer = sr.Recognizer()


def video_text_converter(filename):
    """
    暂时使用google识别
    :param filename: 文件名
    :return: 识别结果
    """

    video = AudioSegment.from_file(os.path.join(os.path.abspath(__file__), f"../uploads/{filename}"))
    video.export(os.path.join(os.path.abspath(__file__), "../wav_out/out.wav"), format="wav")

    with sr.AudioFile(os.path.join(os.path.abspath(__file__), "../wav_out/out.wav")) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio, language="zh-CN")
    except sr.UnknownValueError:
        return "Google Speech Recognition could not understand audio"
    except sr.RequestError as e:
        return "Could not request results from Google Speech Recognition service; {0}".format(e)


@app.route("/upload", methods=["POST"])
def file_uploader():
    video = request.files["video"]
    print(request.files)
    format_time = time.strftime("%Y%m%d%H%M%S")
    # TODO 生成id保存文件及对应的识别结果
    video.save(os.path.join(os.path.abspath(__file__), f"../uploads/{secure_filename(video.filename)}"))
    return video_text_converter(video.filename)


'''
使用讯飞接口测试
'''
@app.route("/uploadTest", methods=["POST"])
def uploade_test():
    """
    TODO 获取上传信息完毕，编写回调接口获取结果
    :return:
    """
    video = request.files["video"]
    format = video.filename.split(".")[-1]
    vname = str(uuid.uuid4()) + "." + format
    video.save(os.path.join(os.path.abspath(__file__), f"../uploads/{vname}"))
    db = DataBase()
    db.newVideo(vname)
    converter = ConverterApi(appid="26bb2303",
                             secret_key="06b53acfaa6ce27530ec1351e74ace49",
                             upload_file_path=os.path.join(os.path.abspath(__file__), f"../uploads/{vname}"))
    upload_res = converter.upload()
    return upload_res


@app.route("/testpage")
def testpage():
    """
        文件上传测试页面
        识别效果页面
    """
    return render_template("test.html")


if __name__ == "__main__":
    db = DataBase()
    db.createTable()
    db.close()
    app.run(debug=True, port=2121)
