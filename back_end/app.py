import json
import os
import time
import uuid

import speech_recognition as sr
from flask import Flask, request
from pydub import AudioSegment
from werkzeug.utils import secure_filename

from db.db_api import DataBase
from utils.LongFormASR import ConverterApi

app = Flask(__name__)
recognizer = sr.Recognizer()
converter = ConverterApi(appid="26bb2303",
                         secret_key="06b53acfaa6ce27530ec1351e74ace49")


def video_text_converter(filename):
    """
    使用google在线接口识别（需要翻墙）
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


@app.route("/uploadTest", methods=["POST"])
def file_uploader():
    """
    谷歌在线接口转换
    :return: 谷歌转换结果（纯文字）
    """
    video = request.files["video"]
    print(request.files)
    format_time = time.strftime("%Y%m%d%H%M%S")
    videoPath = os.path.normpath(
        os.path.join(os.path.abspath(__file__), f"../uploads/{secure_filename(video.filename)}"))
    video.save(videoPath)
    return video_text_converter(video.filename)


@app.route("/upload", methods=["POST"])
def uploade_test():
    """
    上传视频到讯飞接口获取唯一orderId
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


@app.route("/query", methods=["POST"])
def query():
    """
    根据唯一orderId查询识别结果
    :return: 识别结果（Json）
    """
    """
    ###
    #轮询获取结果方式
    ###
    db = DataBase()
    orderId = request.form["orderId"]
    res = db.getResult(orderId)
    if res is None:
        res = converter.query_result(orderId)
    res_json = json.loads(res)
    if res_json["content"]["orderInfo"]["status"] == 4:
        db.addResult(orderId, res)
        db.close()
        return get_words(res_json)
    elif res_json["content"]["orderInfo"]["status"] == 3:
        db.close()
        return "converting..."
    elif res_json["content"]["orderInfo"]["status"] == 0:
        db.close()
        return "uploading..."
    else:
        db.close()
        return "failed!"
    """
    ###
    #配合回调接口，直接在数据库中查询
    ###
    db = DataBase()
    orderId = request.form["orderId"]
    res = db.getResult(orderId)
    if res == "fail":
        return res
    elif res == None:
        return "converting"
    else:
        return get_words(json.loads(res))


def get_words(ori_json):
    """
    讯飞数据包解包函数
    :param ori_json: Json数据包
    :return: Json形式识别结果，格式如下
    [
        {
            "bg":xxx //语句开始时间(ms)
            "ed":xxx //语句结束时间(ms)
            “line”:xxx //识别结果
        },
        ...
    ]
    """
    lines = json.loads(ori_json["content"]["orderResult"])["lattice"]
    res = []
    for line in lines:
        tmp = json.loads(line["json_1best"])["st"]
        newLine = {}
        newLine["bg"] = tmp["bg"]
        newLine["ed"] = tmp["ed"]
        newLine["line"] = ""
        words = tmp["rt"]
        for word in words:
            sentence = ""
            for s in word["ws"]:
                sentence += s["cw"][0]["w"]
            newLine["line"] += sentence
        res.append(newLine)
    return res


@app.route("/callback", methods=["GET"])
def callbackFunc():
    """
    讯飞回调接口（需要公网部署）
    回调接口调用后自动填充转换结果
    :return: no return
    """
    args = request.args
    orderId = args["orderId"]
    db = DataBase()
    if args["status"] == "1":
        print("get an order done!")
        res = converter.query_result(orderId)
        db.addResult(orderId, res)
    else:
        db.addResult(orderId, "fail")
    db.close()
    return ""


if __name__ == "__main__":
    db = DataBase()
    db.createTable()
    db.close()
    app.run(debug=True, port=5000, host="0.0.0.0")
