
import os
import ffmpeg
import datetime
import tempfile
import speech_recognition as sr
from pydub import AudioSegment
from google.cloud import storage
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (   
    MessageEvent, TextMessage, TextSendMessage,AudioMessage,
)


os.environ["GCLOUD_PROJECT"] = "lalu"
app = Flask(__name__)

line_bot_api = LineBotApi('hKQqH81E7hVz7qTR2atb33XCwxGU7rp26ujip3v07w/zG6Mh/MFAytYQMRQ8REHXKFK83SxYet8CP8V9ToFTsT6ECb7okQaw/Ma3F8kMEe3qgdgA7CeDuNjQ+4UCkJqo7zwtkQEsYfxEYT2LNFB+PwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('25d6ce598476773ebf878082b36021b5')


@app.route("/", methods=['GET'])
def hello():
    return "Hello World!"

@app.route("/", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    print("Request body: " + body, "Signature: " + signature)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
       abort(400)
    return 'OK'

@handler.add(MessageEvent,message=AudioMessage)
def handle_aud(event):
    message_content = line_bot_api.get_message_content(event.message.id)
    ext = (datetime.date.today()+datetime.timedelta(hours=8)).strftime("%Y-%m-%d")
    try:
        with tempfile.NamedTemporaryFile(prefix=ext + '-',delete=False) as tf:
            for chunk in message_content.iter_content():
                tf.write(chunk)
            tempfile_path = tf.name
        path = tempfile_path 
        sound = AudioSegment.from_file_using_temporary_files(path)

        wavpath = os.path.splitext(path)[0]+'.wav'
        sound.export(wavpath, format="wav")
        head_tail = os.path.split(wavpath)
        f = head_tail[1]
        
        gcs = storage.Client()
        bucket = gcs.get_bucket('lalu-aud')
        folder = (datetime.date.today()+datetime.timedelta(hours=8)).strftime("%Y-%m-%d")
        filename = "%s/%s" % (folder, f)
        blob = bucket.blob(filename)
        blob.upload_from_filename(wavpath)
        
    except Exception as e:
        t = '音訊有問題'+str(e.args)+wavpath
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=t))

    os.remove(path)
    os.remove(wavpath)
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text='上傳成功\n'+'檔名為:'+f))


if __name__ == "__main__":
    app.run(debug=True)