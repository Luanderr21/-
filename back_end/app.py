import json
import os.path
import time
import uuid

import flask
import pydub
import speech_recognition as sr
from flask import Flask, request
from moviepy.editor import *
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
def xf_uploader():
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
    upload_res = converter.upload(videoPath)
    if "descInfo" not in upload_res:
        return upload_res
    if upload_res["descInfo"] == "success":
        orderId = upload_res["content"]["orderId"]
        db.newVideo(orderId, vname)
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
    ###
    # 轮询获取结果方式
    ###
    db = DataBase()
    orderId = request.form["orderId"]
    res = db.getResult(orderId)
    if res is None:
        res = converter.query_result(orderId)
    res_json = json.loads(res)
    if res_json["descInfo"] == "success":
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
    else:
        return res_json["descInfo"]
    """
    ###
    # 配合回调接口，直接在数据库中查询
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
    """


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


@app.route("/replace", methods=["POST"])
def replace():
    """
    部分音频替换功能
    body表单参数
        audio：替换音频
        orderId：视频主键
        bg：替换起始时间
        ed：替换结束时间
    :return: 替换结果文件名，通过video_show接口获取视频
    """
    audio = request.files["audio"]
    orderId = request.form["orderId"]
    bg = int(request.form["bg"])
    ed = int(request.form["ed"])
    db = DataBase()
    vname = db.getVideo(orderId)
    format = audio.filename.split(".")[-1]
    # 生成uuid保存上传的替换音频
    replacer_id = str(uuid.uuid4()) + "." + format
    audio_path = os.path.normpath(os.path.join(os.path.abspath(__file__), f"../uploads/{replacer_id}"))
    video_path = os.path.normpath(os.path.join(os.path.abspath(__file__), f"../uploads/{vname}"))
    export_path = os.path.normpath(os.path.join(os.path.abspath(__file__), "../tmp/tmp_audio.wav"))
    audio.save(audio_path)
    db.addReplacer(orderId, replacer_id)
    origin = pydub.AudioSegment.from_file(video_path)
    replacer = pydub.AudioSegment.from_file(audio_path)
    # pydub切片生成替换后音频
    first_slice = origin[0:bg]
    last_slice = origin[ed:len(origin)]
    silence_slice = pydub.AudioSegment.silent(duration=(ed - bg - len(replacer)))
    replacer = replacer + silence_slice
    final_audio = first_slice + replacer + last_slice
    # pydub导出后moviepy读入
    final_audio.export(export_path, format="wav")
    final_audio_mv = AudioFileClip(export_path)
    final_name = str(uuid.uuid4()) + "." + "mp4"
    # moviepy合成到原视频并导出
    video_tmp = VideoFileClip(video_path)
    video_tmp = video_tmp.set_audio(final_audio_mv)
    video_tmp.write_videofile(os.path.normpath(os.path.join(os.path.abspath(__file__), f"../uploads/{final_name}")))
    db.addRepname(orderId, final_name)
    db.close()
    return final_name


@app.route("/video_show", methods=["GET"])
def replace_result():
    """
    获取视频接口
    vname：文件名
    :return: 二进制流视频
    """
    vname = None
    if "vname" in request.args:
        vname = request.args["vname"]
    if "vkey" in request.args:
        vkey = request.args["vkey"]
        db = DataBase()
        vname = db.getVideo(vkey)
        db.close()
    assert vname != None
    # return flask.send_file(os.path.normpath(os.path.join(os.path.abspath(__file__), f"../uploads/{vname}")))
    path = os.path.normpath(os.path.join(os.path.abspath(__file__), f"../uploads/{vname}"))
    headers = {
        "Accept-Range": "bytes",
        "Content-Length": os.path.getsize(path),
        "Content-Range": request.range.to_content_range_header(os.path.getsize(path))
    }
    f = open(path, "rb")
    f.seek(request.range.ranges[0][0])
    return flask.Response(f, 206, headers, content_type="video/mp4")


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
