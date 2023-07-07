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
converter = ConverterApi(appid="26bb2303",
                         secret_key="06b53acfaa6ce27530ec1351e74ace49")

def video_text_converter(filename):
    """
    暂时使用google识别
    :param filename: 文件名
    :return: 识别结果
    """
    videoPath = os.path.normpath(os.path.join(os.path.abspath(__file__), f"../uploads/{filename}"))
    outPath = os.path.normpath(os.path.join(os.path.abspath(__file__), "../wav_out/out.wav"))
    video = AudioSegment.from_file(videoPath)
    video.export(outPath, format="wav")

    with sr.AudioFile(outPath) as source:
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
    videoPath = os.path.normpath(os.path.join(os.path.abspath(__file__), f"../uploads/{secure_filename(video.filename)}"))
    video.save(videoPath)
    return video_text_converter(video.filename)


'''
使用讯飞接口测试
'''
@app.route("/uploadTest", methods=["POST"])
def uploade_test():
    """
    上传视频获取唯一orderId
    :return: orderId
    """
    video = request.files["video"]
    format = video.filename.split(".")[-1]
    vname = str(uuid.uuid4()) + "." + format
    videoPath = os.path.normpath(os.path.join(os.path.abspath(__file__), f"../uploads/{vname}"))
    video.save(videoPath)
    db = DataBase()
    db.newVideo(vname)
    upload_res = converter.upload(videoPath)
    if upload_res["descInfo"] == "success":
        orderId = upload_res["content"]["orderId"]
        db.addKey(vname, orderId)
        db.close()
        return orderId
    else:
        db.close()
        return "upload video failed!"

@app.route("/querypage")
def querypage():
    return render_template("query_test.html")

@app.route("/query", methods=["POST"])
def query():
    """
    根据唯一orderId查询识别结果
    :return: 识别结果（Json）
    """
    orderId = request.form["orderId"]
    db = DataBase()
    res = converter.query_result(orderId)
    db.addResult(orderId, res)
    return res


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
