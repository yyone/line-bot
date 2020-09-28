import requests
import json
import base64
import subprocess


class gcpSpeech:
    """
    GCPの音声処理APIへアクセスするクラス
    """

    GCP_SPEECH_API_URL = \
        'https://speech.googleapis.com/v1beta1/speech:syncrecognize?key='
    API_KEY = ''

    def __init__(self, key):
        self.API_KEY = key

    def get_api_url(self):
        """
        Returns
        -------
        self.GCP_SPEECH_API_URL : str
            URL文字列
        """
        return self.GCP_SPEECH_API_URL

    def get_api_key(self):
        """
        Returns
        -------
        API_KEY : str
            API_KEYの文字列
        """
        return self.API_KEY

    def encode_base64(self, audio):
        """
        LINE APIリクエスト用に音声データをエンコードする

        Parameters
        ----------
        audio : wav形式の音声データ

        Returns
        -------
        base64.b64encode : str
            base64にエンコードされたwav音声データ
        """
        return base64.b64encode(audio)

    def trans_wav(self, audio):
        """
        LINE APIリクエスト用に音声データを変換する

        Parameters
        ----------
        audio : binary
            バイナリの音声データ

        Returns
        -------
        audio_wav : wav
            変換されたwav形式の音声データ
        """
        raw_file = '.cache/audio.raw'
        wav_file = '.cache/audio.wav'

        f = open(raw_file, 'w+b')
        f.write(audio)
        f.close()

        # cmd += '/usr/local/bin/sox -r 8k -e signed -b 16 -c 1 '
        # cmd += raw_file + ' ' + wav_file
        cmd = '/usr/local/bin/ffmpeg -y -i ' + raw_file + ' ' + wav_file
        subprocess.call(cmd, shell=True)

        f = open(wav_file, 'rb')
        audio_wav = f.read()
        f.close()

        return audio_wav

    def format_res(self, res_json):
        """
        レスポンスデータを変換する

        Parameters
        ----------
        res_json : dict
            レスポンスデータを変換したJSON

        Returns
        -------
        res_text : str
            変換されたテキスト

        See Also
        --------
        get_speech : 音声データをテキスト変換処理する
        """
        res_text = ''

        audio_text = res_json['results'][0]['alternatives'][0]
        res_text += str('{:.3f}'.format(audio_text['confidence']))
        res_text += ' : '
        res_text += audio_text['transcript']

        return res_text

    def get_speech(self, audio_binary, lang):
        """
        音声データをテキスト変換処理する

        Parameters
        ----------
        audio_binary : binary
            音声バイナリデータ
        lang : str
            変換するテキスト言語

        Returns
        -------
        res_dict : dict
            テキスト変換されたデータを格納した辞書
        """
        api_url = self.get_api_url() + self.get_api_key()

        req_body = json.dumps({
            'config': {
                'encoding': 'LINEAR16',
                'sampleRate': 16000,
                'languageCode': lang
            },
            'audio': {
                'content': self.encode_base64(
                    self.trans_wav(audio_binary)).decode('utf-8')
                # 'uri': speech_uri
            }
        })

        res = requests.post(api_url, data=req_body)
        # print(res.text)
        res_json = json.loads(res.text)
        res_dict = {}

        if not res_json:
            res_dict['text'] = 'no response'
        else:
            if 'error' in res_json:
                res_text = ''
                res_text += str(res_json['error']['code'])
                res_text += ' : '
                res_text += res_json['error']['message']

                res_dict['text'] = res_text
            else:
                res_dict['text'] = self.format_res(res_json)

        return res_dict
