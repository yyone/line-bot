import requests
import json
import settings


class ibmTranslator:
    """
    IBM Watsonの自然言語処理APIへアクセスするクラス
    """

    IBM_TRANS_API_URL = \
        'https://gateway.watsonplatform.net' + \
        '/language-translator/api/v2/translate'

    def get_api_url(self):
        """
        Returns
        -------
        self.IBM_TRANS_API_URL : str
            URL文字列
        """
        return self.IBM_TRANS_API_URL

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
        get_translator : テキストを翻訳する
        """
        trans = res_json['translations']
        if not trans:
            return 'no objects'

        res_text = ''
        for obj in trans:
            res_text += obj['translation'] + ','
        res_text = res_text.rstrip(',')

        return res_text

    def get_translator(self, text, source, target):
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
        api_url = self.get_api_url()

        req_body = json.dumps({
            'text': text.split(','),
            'source': source,
            'target': target
        })
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        res = requests.post(
            api_url,
            data=req_body,
            auth=(
                settings.IBM_TARNS_USERNAME,
                settings.IBM_TARNS_PASSWORD
            ),
            headers=headers
        )
        res_json = json.loads(res.text)
        # print(res.text)

        if not res_json:
            return 'no response'

        return self.format_res(res_json)
