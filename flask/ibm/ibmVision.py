from ibm.ibmTranslator import ibmTranslator
import requests
import json
import datetime


class ibmVision:
    """
    IBM Watsonの画像識別APIへアクセスするクラス
    """

    IBM_VISUAL_API_URL = \
        'https://gateway-a.watsonplatform.net' + \
        '/visual-recognition/api/v3/classify?api_key='
    API_KEY = ''

    def __init__(self, key):
        self.API_KEY = key

    def get_api_url(self):
        """
        Returns
        -------
        self.IBM_VISUAL_API_URL : str
            URL文字列
        """
        return self.IBM_VISUAL_API_URL

    def get_api_key(self):
        """
        Returns
        -------
        API_KEY : str
            API_KEYの文字列
        """
        return self.API_KEY

    def get_date(self):
        """
        現在日付を取得する

        Returns
        -------
        "{0:%Y-%m-%d}".format(now) : str
            YYYY-MM-DD形式のテキスト
        """
        now = datetime.datetime.now()
        return "{0:%Y-%m-%d}".format(now)

    def format_res(self, res_json):
        """
        レスポンスデータを変換する

        Parameters
        ----------
        res_json : dict
            レスポンスデータを変換したJSON

        Returns
        -------
        tmp_dict : dict
            変換されたテキストなどを格納した辞書

        See Also
        --------
        get_vision : 画像データから分類処理を行う
        """
        text = tmp_score = tmp_desc = tmp_trans = ''
        tmp_dict = {}
        iTrans = ibmTranslator()

        type = res_json['images'][0]
        if not type:
            return 'no objects'

        # 画像検知 or 分類
        if 'classifiers' in type:
            for obj in type['classifiers'][0]['classes']:
                tmp_score += str('{:.3f}'.format(obj['score'])) + ','
                tmp_desc += obj['class'] + ','
            tmp_score = tmp_score.rstrip(',')
            tmp_desc = tmp_desc.rstrip(',')

            tmp_trans = iTrans.get_translator(tmp_desc, 'en', 'ja')
            for x in range(0, len(tmp_score.split(','))):
                text += tmp_score.split(',')[x] + ' : '
                text += tmp_desc.split(',')[x] + ' - '
                text += tmp_trans.split(',')[x] + '\n'

        # 文字
        elif 'textAnnotations' in type:
            obj = type['textAnnotations'][0]
            text += obj['description'] + '\n'
            tmp_dict['lang'] = self.trans_locale(obj['locale'])

        # 顔
        elif 'faces' in type:
            obj = type['faceAnnotations'][0]
            text += 'joyLikelihood : '
            text += self.trans_likelifood(obj['joyLikelihood'])
            text += '\n'

            text += 'sorrowLikelihood : '
            text += self.trans_likelifood(obj['sorrowLikelihood'])
            text += '\n'

            text += 'angerLikelihood : '
            text += self.trans_likelifood(obj['angerLikelihood'])
            text += '\n'

            text += 'surpriseLikelihood : '
            text += self.trans_likelifood(obj['surpriseLikelihood'])
            text += '\n'

            text += 'underExposedLikelihood : '
            text += self.trans_likelifood(obj['underExposedLikelihood'])
            text += '\n'

            text += 'blurredLikelihood : '
            text += self.trans_likelifood(obj['blurredLikelihood'])
            text += '\n'

            text += 'headwearLikelihood : '
            text += self.trans_likelifood(obj['headwearLikelihood'])
            text += '\n'

        # 構造物（名所）
        elif 'landmarkAnnotations' in type:
            for obj in type['landmarkAnnotations']:
                text += str('{:.3f}'.format(obj['score']))
                text += ' : '
                text += obj['description']
                text += '\n'

                text += 'latitude : '
                text += str(obj['locations'][0]['latLng']['latitude'])
                text += '\n'

                text += 'longitude : '
                text += str(obj['locations'][0]['latLng']['longitude'])
                text += '\n'
        else:
            text = "can not recognize this type of response"

        tmp_dict['text'] = text.rstrip('\n')
        return tmp_dict

    def get_vision(self, image_binary):
        """
        画像データから分類処理を行う

        Parameters
        ----------
        image_binary : binary
            画像バイナリデータ

        Returns
        -------
        res_dict : dict
            分類結果のテキストを格納した辞書
        """
        api_url = self.get_api_url() + self.get_api_key() + \
            '&version=' + self.get_date()
        headers = {
            'Content-Type': 'multipart/form-data'
        }

        res = requests.post(api_url, data=image_binary, headers=headers)
        # print(res.text)
        res_json = json.loads(res.text)
        res_dict = {}

        if not res_json:
            res_dict['text'] = 'no response'
        else:
            if 'error' in res_json:
                res_text = ''
                res_text += str(res_json['error']['error_id'])
                res_text += ' : '
                res_text += res_json['error']['description']

                res_dict['text'] = res_text
            else:
                res_dict = self.format_res(res_json)

        return res_dict
