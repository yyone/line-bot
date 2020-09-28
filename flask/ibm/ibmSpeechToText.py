import requests
import json
import subprocess
import settings


class ibmSpeechToText:
    """
    IBM Watsonの音声 to テキスト処理APIへアクセスするクラス
    """

    IBM_SPEECH_API_URL = \
        'https://stream.watsonplatform.net' + \
        '/speech-to-text/api/v1/recognize'

    def get_api_url(self):
        """
        Returns
        -------
        self.IBM_SPEECH_API_URL : str
            URL文字列
        """
        return self.IBM_SPEECH_API_URL

    def trans_wav(self, audio):
        """
        レスポンスデータを変換する

        Parameters
        ----------
        audio : binary
            音声バイナリデータ

        Returns
        -------
        audio_wav : wav
            変換されたwav形式の音声データ
        """
        raw_file = '.cache/audio.raw'
        wav_file = '.cache/audio.wav'

        fp = open(raw_file, 'w+b')
        fp.write(audio)
        fp.close()

        # cmd = '/usr/local/bin/sox -r 8k -e signed -b 16 -c 1 '
        # cmd += raw_file + ' ' + wav_file
        cmd = '/usr/local/bin/ffmpeg -y -i ' + raw_file + ' ' + wav_file
        subprocess.call(cmd, shell=True)

        fp = open(wav_file, 'rb')
        audio_wav = fp.read()
        fp.close()

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
        get_speech_to_text : 音声をテキストに変換する
        """
        audio_text = res_json['results'][0]['alternatives'][0]

        res_text = ''
        res_text += str('{:.3f}'.format(audio_text['confidence']))
        res_text += " : "
        res_text += audio_text['transcript']

        return res_text

    def get_speech_to_text(self, audio_binary, lang):
        """
        音声をテキストに変換する

        Parameters
        ----------
        audio_binary : binary
            入力された音声データ
        lang : str
            変換後のテキスト言語

        Returns
        -------
        res_dict : dict
            変換されたテキストなどを格納した辞書
        """
        langParam = '?model='
        if lang == 'ja':
            langParam += 'ja-JP_NarrowbandModel'
        elif lang == 'en':
            langParam += 'en-US_NarrowbandModel'

        api_url = self.get_api_url() + langParam
        req_body = self.trans_wav(audio_binary)
        headers = {
            'Content-Type': 'audio/wav'
        }

        res = requests.post(
            api_url,
            data=req_body,
            auth=(
                settings.IBM_StoT_USERNAME,
                settings.IBM_StoT_PASSWORD
            ),
            headers=headers
        )
        # print(res.text)
        res_json = json.loads(res.text)
        res_dict = {}

        if not res_json['results']:
            res_dict['text'] = 'no reponse'
        else:
            if 'error' in res_json:
                res_dict['text'] = res_json['code'] + " : " + res_json['error']
            else:
                res_dict['text'] = self.format_res(res_json)

        return res_dict
