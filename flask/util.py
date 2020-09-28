import requests
import json
import settings


class LineReplyMessage:
    """
    LINEへメッセージを送受信するためのクラス
    """
    CONTENT_ENDPOINT = 'https://api.line.me/v2/bot/message'
    REPLY_ENDPOINT = 'https://api.line.me/v2/bot/message/reply'
    LINE_ACCESS_TOKEN = settings.LINE_ACCESS_TOKEN

    def get_content(self, replyToken, messageId):
        """
        画像や音声ファイルなどをLINE APIから取得する

        Parameters
        ----------
        replayToken : str
            API側から取得したアクセストークン（セッション継続用）
        messageId : str
            メッセージの一意ID

        Returns
        -------
        res.content : str
            requests.models.Responseクラスのcontent属性
            リクエストした結果のレスポンス内容
        """
        get_url = self.CONTENT_ENDPOINT + '/' + messageId + '/content'

        headers = {
            'Authorization': 'Bearer {}'.format(self.LINE_ACCESS_TOKEN)
        }

        res = requests.get(get_url, headers=headers)
        return res.content

    def send_reply(self, replyToken, messages):
        """
        テキストをLINE APIへ送信する

        Parameters
        ----------
        replayToken : str
            API側から取得したアクセストークン（セッション継続用）
        messages : str
            メッセージテキスト
        """
        req_body = json.dumps({
            'replyToken': replyToken,
            'messages': messages
        })

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.LINE_ACCESS_TOKEN)
        }

        requests.post(self.REPLY_ENDPOINT, data=req_body, headers=headers)
