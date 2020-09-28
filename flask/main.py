from lineBot import LineBot
from flask import Flask, request, Response
import wave


app = Flask(__name__)
lb = LineBot()


@app.route('/', methods=['GET'])
def hello():
    """
    flaskのルーティング
    LINEからアクセスするWebhook関数

    Parameters
    ----------
    URL : str
        /
    methods : list of str, default "GET"
        HTTPメソッドの文字列

    Returns
    -------
    None : str
        文字列
    """
    return 'Hello! This is Nginx Server'


@app.route('/bot/callback', methods=['POST'])
def callback():
    """
    flaskのcallback用ルーティング

    Parameters
    ----------
    URL : str
        /bot/callback
    methods : list of str, default "POST"
        HTTPメソッドの文字列

    Returns
    -------
    '' : str
        空白
    200 : int
        HTTPのレスポンスコード
    {} : dict
        空の辞書
    """
    lb.reply_to_line(request.json)
    return '', 200, {}


@app.route('/get/audio', methods=['GET'])
def getAudio():
    """
    flaskの音声ファイル用ルーティング

    Parameters
    ----------
    URL : str
        /get/audio
    methods : list of str, default "GET"
        HTTPメソッドの文字列

    Returns
    -------
    Response : Response
        wav形式の音声データ
    """
    wav_file = '.cache/ibmTransAudio.wav'
    wf = wave.open(wav_file, 'rb')

    # for Debug
    # print('channel = ' + str(wf.getnchannels()))
    # print('sample size = ' + str(wf.getsampwidth()))
    # print('sampling rate = ' + str(wf.getframerate()))
    # print('frame = ' + str(wf.getnframes()))
    audio_wav = wf.readframes(wf.getnframes())
    wf.close()

    return Response(audio_wav, mimetype='audio/wav')


if __name__ == '__main__':
    app.run()
