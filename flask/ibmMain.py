from ibm.ibmVision import ibmVision
from ibm.ibmSpeechToText import ibmSpeechToText
from ibm.ibmTextToSpeech import ibmTextToSpeech
import settings


class ibmMain:
    """
    IBM WatsonのML用APIにアクセスするクラス
    """

    def __init__(self):
        self.iVision = ibmVision(settings.IBM_API_KEY)
        self.iStoT = ibmSpeechToText()
        self.iTtoS = ibmTextToSpeech()

    def Vision(self):
        """
        Returns
        -------
        iVision : ibmVision
            画像処理クラス
        """
        return self.iVision

    def StoT(self):
        """
        Returns
        -------
        iStoT : ibmSpeechToText
            音声をテキストへ変換するクラス
        """
        return self.iStoT

    def TtoS(self):
        """
        Returns
        -------
        iTtoS : ibmTextToSpeech
            テキストを音声へ変換するクラス
        """
        return self.iTtoS
