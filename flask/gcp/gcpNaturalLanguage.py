import requests
import json


class gcpNaturalLanguage:
    """
    GCPの自然言語処理APIへアクセスするクラス
    """

    GCP_NL_BASE_API_URL = 'https://language.googleapis.com/v1beta2/documents:'
    API_KEY = ''

    def __init__(self, key):
        """
        Parameters
        ----------
        key : str
            API認証キー
        """
        self.API_KEY = key

    def get_api_key(self):
        """
        Returns
        -------
        API_KEY : str
            API_KEYの文字列
        """
        return self.API_KEY

    def get_req_json(self, text, lang, type=21):
        """
        APIリクエスト用にJSONを作成する

        Parameters
        ----------
        text : str
            LINEで入力されたテキスト
        lang : str
            言語を表す文字列（ex. JA, EN）
        type : int
            API種別（ex. 1 - 25）

        Returns
        -------
        dict_json : dict
            変換されたJSON
        """
        dict_json = {
            'document': {
                'type': 'PLAIN_TEXT',
                'language': lang,
                'content': text
            }
        }
        if type == 21:
            dict_json.update({
                'features': {
                    'extractSyntax': True,
                    'extractEntities': True
                }
            })

        return dict_json

    def get_api_url(self, type=21):
        """
        APIのURLを作成する

        Parameters
        ----------
        type : int
            API種別

        Returns
        -------
        url : str
            URL文字列
        """
        url = self.GCP_NL_BASE_API_URL

        if type == 21:
            url += 'annotateText'
        elif type == 22:
            url += 'analyzeSyntax'
        elif type == 23:
            url += 'analyzeEntities'
        elif type == 24:
            url += 'analyzeSentiment'
        elif type == 25:
            url += 'analyzeEntitySentiment'

        url += '?key=' + self.get_api_key()
        return url

    def trans_pos_word(self, text):
        """
        翻訳されたテキストの代名詞を英語から日本語に変換する

        Parameters
        ----------
        text : str
            英語の代名詞

        Returns
        -------
        result : str
            日本語の代名詞
        """
        result = ''

        if text == 'NOUN':
            result = '名詞'
        elif text == 'VERB':
            result = '動詞'
        elif text == 'ADJ':
            result = '形容詞'
        elif text == 'ADP':
            result = '前置詞／後置詞'
        elif text == 'ADV':
            result = '副詞'
        elif text == 'CONJ':
            result = '接続詞'
        elif text == 'PRON':
            result = '代名詞'
        elif text == 'AFFIX':
            result = '接頭辞／接尾辞'
        elif text == 'DET':
            result = '限定詞'
        elif text == 'PRT':
            result = '小詞'
        elif text == 'NUM':
            result = '基数'
        elif text == 'PUNCT':
            result = '句読点'
        elif text == 'X':
            result = 'その他'

        return result

    def format_res(self, res_json, type):
        """
        レスポンスデータを変換する

        Parameters
        ----------
        res_json : str
            レスポンスデータを変換したJSON
        type : int
            API種別

        Returns
        -------
        text.rstrip() : str
            JSONを変換したテキスト

        See Also
        --------
        get_natural_language : 自然言語処理をする
        """
        text = ''
        if type == 21:
            text += '[Token]\n'
            for obj in res_json['tokens']:
                text += obj['text']['content'].ljust(20) + ' : '
                text += obj['partOfSpeech']['tag'] + ' - '
                text += self.trans_pos_word(obj['partOfSpeech']['tag']) + '\n'

        elif type == 23:
            text += '[Entity]\n'
            for obj in res_json['entities']:
                text += obj['name'] + ' : ' + obj['type'] + ' - '
                text += str('{:.2f}'.format(obj['salience'])) + '\n'

        elif type == 24:
            text += '[Sentiment]\n'
            text += 'score : '
            text += str('{:.1f}'.format(
                res_json['documentSentiment']['score'])
            )
            text += '\n'
            text += 'magnitude : '
            text += str('{:.1f}'.format(
                res_json['documentSentiment']['magnitude'])
            )
            text += '\n'

        return text.rstrip('\n')

    def get_natural_language(self, text, lang, type):
        """
        自然言語処理をする

        Parameters
        ----------
        text : str
            LINEで入力されたテキスト
        lang : str
            言語を表す文字列（ex. JA, EN）
        type : int
            API種別（ex. 1 - 25）

        Returns
        -------
        res_text : str
            自然言語処理されたテキスト

        See Also
        --------
        descriptions.get_desc_apiType : API種別を返す。各種別を確認できる
        """
        req_body = json.dumps(self.get_req_json(text, lang, type))
        res = requests.post(self.get_api_url(type), data=req_body)
        res_json = json.loads(res.text)
        # print(res.text)

        if not res_json:
            return 'no response'
        else:
            if type == 21:
                res_text = self.format_res(res_json, type)

                # 追加でsentiment分析実施
                req_body = json.dumps(self.get_req_json(text, lang, 24))
                res = requests.post(self.get_api_url(24), data=req_body)
                res_json = json.loads(res.text)
                res_text += '\n\n' + self.format_res(res_json, 24)
            elif type in {23, 24}:
                res_text = self.format_res(res_json, type)
            else:
                print(res_json.text)
                res_text = res_json.text

        return res_text
