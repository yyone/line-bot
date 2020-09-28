import requests
import json
import urllib.parse


class msVision:
    """
    IBM Watsonの画像識別APIへアクセスするクラス
    """

    MS_VISION_API_URL = \
        'https://southeastasia.api.cognitive.microsoft.com' + \
        '/vision/v1.0/analyze?%s'
    API_KEY = ''

    def __init__(self, key):
        self.API_KEY = key

    def get_api_url(self):
        """
        Returns
        -------
        self.MS_VISION_API_URL : str
            URL文字列
        """
        return self.MS_VISION_API_URL

    def get_api_key(self):
        """
        Returns
        -------
        API_KEY : str
            API_KEYの文字列
        """
        return self.API_KEY

    def trans_locale(self, locale):
        """
        localeをlangに変換する

        Parameters
        ----------
        locale : str
            言語

        Returns
        -------
        lang : str
            言語 - 国
        """
        lang = 'ja-JP'

        if locale == 'ja':
            lang = 'ja-JP'
        elif locale == 'en':
            lang = 'en-US'

        return lang

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
        get_vision : 画像データから分類処理を行う
        """
        text = tmp_score = tmp_desc = ''
        res_text = ''

        type = res_json
        if not type:
            return 'no objects'

        # 画像検知
        if 'tags' in type:
            for obj in type['tags']:
                tmp_score += str('{:.3f}'.format(obj['confidence'])) + ','
                tmp_desc += obj['name'] + ','
            tmp_score = tmp_score.rstrip(',')
            tmp_desc = tmp_desc.rstrip(',')

            for x in range(0, len(tmp_score.split(','))):
                text += tmp_score.split(',')[x] + ' : '
                text += tmp_desc.split(',')[x] + '\n'

        # 解説
        elif 'description' in type:
            for obj in type['description']['captions']:
                tmp_score += str('{:.3f}'.format(obj['confidence'])) + ','
                tmp_desc += obj['text'] + ','
            tmp_score = tmp_score.rstrip(',')
            tmp_desc = tmp_desc.rstrip(',')

            for x in range(0, len(tmp_score.split(','))):
                text += tmp_score.split(',')[x] + ' : '
                text += tmp_desc.split(',')[x] + '\n'

        # 顔
        elif 'faces' in type:
            obj = type['faces'][0]
            text += 'gender : ' + obj['gender'] + '\n'
            text += 'age : ' + str(obj['age']) + '\n'

        # 不適コンテンツ
        elif 'adult' in type:
            obj = type['adult']

            if obj['isAdultContent']:
                isAdult = 'Yes'
            else:
                isAdult = 'No'
            text += 'isAdult : ' + isAdult
            text += '\n'

            text += 'Adult Score : '
            text += str('{:.3f}'.format(obj['adultScore']))
            text += '\n'

            if obj['isRacyContent']:
                isRacy = 'Yes'
            else:
                isRacy = 'No'
            text += 'isRacy : ' + isRacy
            text += '\n'

            text += 'Racy Score : '
            text += str('{:.3f}'.format(obj['racyScore']))
            text += '\n'

        else:
            text = json.dumps(res_json)

        res_text = text.rstrip('\n')
        return res_text

    def get_vision(self, image_binary, type):
        """
        画像データから分類処理を行う

        Parameters
        ----------
        image_binary : binary
            画像バイナリデータ
        type : int
            API種別

        Returns
        -------
        res_dict : dict
            分類結果のテキストを格納した辞書
        """
        api_url = self.get_api_url()
        headers = {
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': self.get_api_key()
        }
        req_body = image_binary

        if type == 1:
            feature = 'Tags'
        elif type == 2:
            feature = 'Description'
        elif type == 3:
            feature = 'Faces'
        elif type == 4:
            feature = 'Adult'
        elif type == 11:
            feature = 'Categories'

        param = urllib.parse.urlencode({
            'visualFeatures': feature,
            'language': 'en'
        })

        res = requests.post(api_url % param, data=req_body, headers=headers)
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
