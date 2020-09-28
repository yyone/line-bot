from descriptions import get_desc_apiType, get_desc_help
from descriptions import get_desc_gcp_help, get_desc_ibm_help, get_desc_ms_help
from util import LineReplyMessage
from gcpMain import gcpMain
from ibmMain import ibmMain
from msMain import msMain


class LineBot:
    """
    LineBotのメイン処理クラス
    """
    api_type = 1     # default mode
    lang = 'ja'      # default language
    service = 'gcp'  # default service

    def get_api_type(self):
        """
        Returns
        -------
        self.api_type : str
            api_typeのゲッター
        """
        return self.api_type

    def get_lang(self):
        """
        Returns
        -------
        self.lang : str
            langのゲッター
        """
        return self.lang

    def get_service(self):
        """
        Returns
        -------
        self.service : str
            serviceのゲッター
        """
        return self.service

    def set_api_type(self, type):
        """
        Parameters
        ----------
        type : str
            typeのセッター
        """
        self.api_type = type

    def set_lang(self, lang):
        """
        Parameters
        ----------
        lang : str
            langのセッター
        """
        self.lang = lang

    def set_service(self, service):
        """
        Parameters
        ----------
        service : str
            serviceのセッター
        """
        self.service = service

    def reply_to_line(self, body):
        """
        Parameters
        ----------
        body : dict
            callbackリクエストで取得したJSON形式データ
        """
        lrm = LineReplyMessage()
        gcp = gcpMain()
        ibm = ibmMain()
        ms = msMain()

        for event in body['events']:
            responses = []
            reply_text = ''

            replyToken = event['replyToken']
            type = event['type']

            if type == 'message':
                message = event['message']

                # 環境設定処理
                if message['type'] == 'text':
                    # 数値処理
                    if message['text'].isdigit():
                        # 設定初期化
                        if int(message['text']) == 0:
                            self.set_api_type(1)
                            self.set_lang('ja')
                            self.set_service('gcp')
                            reply_text = '設定リセット'
                        # モード切り替え
                        elif int(message['text']) in {
                            1, 2, 3, 4, 5, 6, 7, 21, 22, 23, 24, 25
                        }:
                            reply_text += '「'
                            reply_text += get_desc_apiType(
                                int(message['text']), self.get_service()
                            )
                            reply_text += '」開始'
                            self.set_api_type(int(message['text']))
                        elif int(message['text']) in {11}:
                            self.set_api_type(int(message['text']))
                            reply_text = '開発中'
                        else:
                            pass

                    # 言語切り替え
                    elif message['text'].lower() in {
                        'ja', 'en'
                    }:
                        if message['text'].lower() == 'ja':
                            self.set_lang('ja')
                        elif message['text'].lower() == 'en':
                            self.set_lang('en')
                        reply_text += '言語切り替え完了 : '
                        reply_text += self.get_lang()

                    # サービス切り替え
                    elif message['text'].lower() in {
                        'gcp', 'ibm', 'ms'
                    }:
                        if message['text'].lower() == 'gcp':
                            self.set_service('gcp')
                        elif message['text'].lower() == 'ibm':
                            self.set_service('ibm')
                        elif message['text'].lower() == 'ms':
                            self.set_service('ms')
                        reply_text += 'サービス切り替え完了 : '
                        reply_text += self.get_service()
                    # ヘルプ
                    elif message['text'] in {'h', 'help'}:
                        reply_text = get_desc_help()
                    elif message['text'] == 'hg':
                        reply_text = get_desc_gcp_help()
                    elif message['text'] == 'hi':
                        reply_text = get_desc_ibm_help()
                    elif message['text'] == 'hm':
                        reply_text = get_desc_ms_help()
                    elif message['text'] == 'i':
                        reply_text = 'service : ' + self.get_service() + '\n'
                        reply_text += 'lang : ' + self.get_lang() + '\n'
                        reply_text += 'mode : ' + str(self.get_api_type())
                        reply_text += ' -> '
                        reply_text += get_desc_apiType(
                            self.get_api_type(),
                            self.get_service()
                        )
                    else:
                        pass

                # テキスト処理
                if message['type'] == 'text' and reply_text == '':
                    # GCP
                    if self.get_service() == 'gcp':
                        # 自然言語処理
                        if self.get_api_type() in {21, 22, 23, 24, 25}:
                            reply_text = gcp.NL().get_natural_language(
                                message['text'],
                                self.get_lang().upper(),
                                self.get_api_type()
                            )
                    # IBM
                    elif self.get_service() == 'ibm':
                        # テキスト to 音声処理
                        if self.get_api_type() == 21:
                            tmp_dict = ibm.TtoS().get_text_to_speech(
                                message['text'],
                                self.get_lang()
                            )
                            reply_text = tmp_dict['text']
                    # その他
                    else:
                        reply_text = message['text']

                # 画像処理
                if message['type'] == 'image':
                    image_binary = lrm.get_content(replyToken, message['id'])

                    if image_binary:
                        # GCP
                        if self.get_service() == 'gcp':
                            if self.get_api_type() in {1, 2, 3, 4, 5, 6, 7}:
                                tmp_dict = gcp.Vision().get_vision(
                                    image_binary,
                                    self.get_api_type()
                                )
                                reply_text = tmp_dict['text']
                            elif self.get_api_type() in {21, 22, 23, 24, 25}:
                                tmp_dict = gcp.Vision().get_vision(
                                    image_binary,
                                    2
                                )
                                reply_text = gcp.NL().get_natural_language(
                                    tmp_dict['text'],
                                    tmp_dict['lang'],
                                    self.get_api_type()
                                )
                        # IBM
                        elif self.get_service() == 'ibm':
                            if self.get_api_type() == 1:
                                tmp_dict = ibm.Vision().get_vision(
                                    image_binary
                                )
                                reply_text = tmp_dict['text']
                        # MS
                        elif self.get_service() == 'ms':
                            if self.get_api_type() in {1, 2, 3, 4, 11}:
                                tmp_dict = ms.Vision().get_vision(
                                    image_binary,
                                    self.get_api_type()
                                )
                                reply_text = tmp_dict['text']
                    else:
                        reply_text = 'error: line api for image'

                # 音声処理
                if message['type'] == 'audio':
                    audio_binary = lrm.get_content(replyToken, message['id'])

                    if audio_binary:
                        # GCP
                        if self.get_service() == 'gcp':
                            if self.get_lang() == 'ja':
                                lang = 'ja-JP'
                            elif self.get_lang() == 'en':
                                lang = 'en-US'

                            tmp_dict = gcp.Speech().get_speech(
                                audio_binary,
                                lang
                            )
                            reply_text = tmp_dict['text']

                            # 自然言語処理を追加実施
                            if self.get_api_type() in {21, 22, 23, 24, 25}:
                                reply_text = gcp.NL().get_natural_language(
                                    tmp_dict['text'],
                                    lang,
                                    self.get_api_type()
                                )
                        # IBM
                        if self.get_service() == 'ibm':
                            tmp_dict = ibm.StoT().get_speech_to_text(
                                audio_binary,
                                self.get_lang()
                            )
                            reply_text = tmp_dict['text']
                    else:
                        reply_text = 'error: line api for speech'

                # その他
                if reply_text == '':
                    reply_text = 'hello!'

            responses.append({
                'type': 'text',
                'text': reply_text
            })
            lrm.send_reply(replyToken, responses)
