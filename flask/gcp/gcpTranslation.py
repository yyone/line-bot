import requests
import json


class gcpTranslation:
    """
    GCPの自然言語処理APIへアクセスするクラス
    """

    GCP_TRANSLATION_API_URL = \
        'https://translation.googleapis.com/language/translate/v2?key='
    API_KEY = ''

    def __init__(self, key):
        self.API_KEY = key

    def get_api_url(self):
        """
        Returns
        -------
        self.GCP_TRANSLATION_API_URL : str
            URL文字列
        """
        return self.GCP_TRANSLATION_API_URL

    def get_api_key(self):
        """
        Returns
        -------
        API_KEY : str
            API_KEYの文字列
        """
        return self.API_KEY

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
            翻訳されたテキスト

        See Also
        --------
        get_translation : テキストを翻訳する
        """
        trans_text = res_json['data']['translations']

        res_text = ''
        for obj in trans_text:
            res_text += obj['translatedText']

        return res_text

    def get_translation(self, text, source, target):
        """
        テキストを翻訳する

        Parameters
        ----------
        text : str
            入力されたメッセージテキスト
        source : str
            翻訳前の言語
        target : str
            翻訳後の言語

        Returns
        -------
        format_res(res_json) : str
            翻訳されたテキスト
        """
        api_url = self.get_api_url() + self.get_api_key()

        req_body = json.dumps({
            'q': [
                text
            ],
            'source': source,
            'target': target,
            'format': 'text'
        })
        res = requests.post(api_url, data=req_body)
        res_json = json.loads(res.text)

        if not res_json:
            return 'no response'

        return self.format_res(res_json)
