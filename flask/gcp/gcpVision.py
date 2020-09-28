from gcp.gcpTranslation import gcpTranslation
import requests
import json
import base64


class gcpVision:
    """
    GCPの画像識別APIへアクセスするクラス
    """

    GCP_VISION_API_URL = \
        'https://vision.googleapis.com/v1/images:annotate?key='
    API_KEY = ''

    def __init__(self, key):
        self.API_KEY = key

    def get_api_url(self):
        """
        Returns
        -------
        self.GCP_VISION_API_URL : str
            URL文字列
        """
        return self.GCP_VISION_API_URL

    def get_api_key(self):
        """
        Returns
        -------
        API_KEY : str
            API_KEYの文字列
        """
        return self.API_KEY

    def encode_base64(self, image):
        """
        LINE APIリクエスト用に画像データをエンコードする

        Parameters
        ----------
        image : 画像バイナリデータ

        Returns
        -------
        base64.b64encode : str
            base64にエンコードされた画像データ
        """
        return base64.b64encode(image)

    def trans_likelifood(self, text):
        """
        画像識別された「気分」を英語から日本語に変換する

        Parameters
        ----------
        text : str
            英語の気分

        Returns
        -------
        result : str
            日本語の気分
        """
        result = ''
        if text == 'VERY_UNLIKELY':
            result = '超低い'
        elif text == 'UNLIKELY':
            result = '低い'
        elif text == 'POSSIBLE':
            result = '普通'
        elif text == 'LIKELY':
            result = '高い'
        elif text == 'VERY_LIKELY':
            result = '超高い'
        else:
            result = '？'

        return result

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

    def get_vision_type(self, type):
        """
        API種別を適したfeature typeに変換する

        Parameters
        ----------
        type : int
            API種別

        Returns
        -------
        vision_type : str
            Vision Type
        """
        if type == 1:
            vision_type = 'LABEL_DETECTION'
        elif type == 2:
            vision_type = 'TEXT_DETECTION'
        elif type == 3:
            vision_type = 'FACE_DETECTION'
        elif type == 4:
            vision_type = 'LANDMARK_DETECTION'
        elif type == 5:
            vision_type = 'LOGO_DETECTION'
        elif type == 6:
            vision_type = 'SAFE_SEARCH_DETECTION'
        elif type == 7:
            vision_type = 'IMAGE_PROPERTIES'

        return vision_type

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
        gTrans = gcpTranslation(self.get_api_key())

        type = res_json['responses'][0]
        if not type:
            return 'no objects'

        # 画像検知 or 分類
        if 'labelAnnotations' in type:
            for obj in type['labelAnnotations']:
                tmp_score += str('{:.3f}'.format(obj['score'])) + ','
                tmp_desc += obj['description'] + ','
            tmp_score = tmp_score.rstrip(',')
            tmp_desc = tmp_desc.rstrip(',')

            tmp_trans = gTrans.get_translation(tmp_desc, 'en', 'ja')
            for x in range(0, len(tmp_score.split(','))):
                text += tmp_score.split(',')[x] + ' : '
                text += tmp_desc.split(',')[x] + ' - '
                text += tmp_trans.split('、')[x] + '\n'

        # 文字
        elif 'textAnnotations' in type:
            obj = type['textAnnotations'][0]
            text += obj['description'] + '\n'
            tmp_dict['lang'] = self.trans_locale(obj['locale'])

        # 顔
        elif 'faceAnnotations' in type:
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

        # ロゴ
        elif 'logoAnnotations' in type:
            obj = type['logoAnnotations'][0]
            text += str('{:.3f}'.format(obj['score']))
            text += ' : '
            text += obj['description']

        # 不適コンテンツ
        elif 'safeSearchAnnotation' in type:
            obj = type['safeSearchAnnotation']
            text += 'adult : '
            text += self.trans_likelifood(obj['adult'])
            text += '\n'

            text += 'spoof : '
            text += self.trans_likelifood(obj['spoof'])
            text += '\n'

            text += 'medical : '
            text += self.trans_likelifood(obj['medical'])
            text += '\n'

            text += 'violence : '
            text += self.trans_likelifood(obj['violence'])
            text += '\n'

        else:
            text = "can not recognize this type of response"

        tmp_dict['text'] = text.rstrip('\n')
        return tmp_dict

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
        api_url = self.get_api_url() + self.get_api_key()

        req_body = json.dumps({
            'requests': [{
                'image': {
                    'content': self.encode_base64(image_binary).decode('utf-8')
                },
                'features': [{
                    'type': self.get_vision_type(type),
                    'maxResults': 10,
                }]
            }]
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
                res_dict = self.format_res(res_json)

        return res_dict
