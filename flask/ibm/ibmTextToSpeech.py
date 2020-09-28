import requests
import json
import wave
import random
import settings


class ibmTextToSpeech:
    """
    IBM Watsonのテキスト to 音声処理APIへアクセスするクラス
    """

    IBM_SPEECH_API_URL = \
        'https://stream.watsonplatform.net' + \
        '/text-to-speech/api/v1/synthesize'

    def get_api_url(self):
        """
        Returns
        -------
        self.IBM_SPEECH_API_URL : str
            URL文字列
        """
        return self.IBM_SPEECH_API_URL

    def get_text_to_speech(self, text, lang):
        """
        テキストを音声に変換する

        Parameters
        ----------
        text : str
            入力されたメッセージテキスト
        lang : str
            変換後の音声言語

        Returns
        -------
        res_dict : dict
            音声データ取得用のURL（EndPoint）などが格納された辞書
        """
        wav_file = '.cache/ibmTransAudio.wav'
        AudioEndPoint = 'https://api.yone3.net/get/audio'

        langParam = '?voice='
        if lang == 'ja':
            langParam += 'ja-JP_EmiVoice'
        elif lang == 'en':
            num = random.randint(1, 100)
            if num % 2 == 1:
                langParam += 'en-US_MichaelVoice'
            else:
                langParam += 'en-US_LisaVoice'

        api_url = self.get_api_url() + langParam
        req_body = json.dumps({
            'text': text
        })
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'audio/wav'
        }

        res = requests.post(
            api_url,
            data=req_body,
            auth=(
                settings.IBM_TtoS_USERNAME,
                settings.IBM_TtoS_PASSWORD
            ),
            headers=headers
        )
        # print(res.text)
        res_dict = {}

        if not res:
            res_dict['text'] = 'no reponse'
        else:
            wf = wave.open(wav_file, 'wb')
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(22050)
            wf.writeframesraw(res.content)
            wf.close()
            res_dict['text'] = AudioEndPoint

        return res_dict
