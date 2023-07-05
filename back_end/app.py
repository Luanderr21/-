import sqlite3
import pydub
from flask import Flask, request, redirect, render_template
from pydub import AudioSegment
from werkzeug.utils import secure_filename
import speech_recognition as sr
import time

app = Flask(__name__)
recognizer = sr.Recognizer()


def video_text_converter(filename):
    """
    暂时使用google识别
    TODO 使用讯飞接口代替
    :param filename: 文件名
    :return: 识别结果
    """
    video = AudioSegment.from_file("./static/" + filename)
    video.export("./wav_out/out.wav", format="wav")

    with sr.AudioFile("./wav_out/out.wav") as source:
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
    video.save("./static/" + secure_filename(video.filename))
    return video_text_converter(video.filename)


@app.route("/test")
def test():
    """
        文件上传测试页面
        识别效果页面
    """
    return render_template("test.html")


app.run(debug=True, port=2121)
