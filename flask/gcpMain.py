from gcp.gcpVision import gcpVision
from gcp.gcpSpeech import gcpSpeech
from gcp.gcpNaturalLanguage import gcpNaturalLanguage
import settings


class gcpMain:
    """
    GCPのML用APIにアクセスするクラス
    """

    def __init__(self):
        self.gVision = gcpVision(settings.GCP_API_KEY)
        self.gSpeech = gcpSpeech(settings.GCP_API_KEY)
        self.gNL = gcpNaturalLanguage(settings.GCP_API_KEY)

    def Vision(self):
        """
        Returns
        -------
        gVision : gcpVision
            画像処理クラス
        """
        return self.gVision

    def Speech(self):
        """
        Returns
        -------
        gSpeech : gcpSpeech
            音声識別処理クラス
        """
        return self.gSpeech

    def NL(self):
        """
        Returns
        -------
        gNL : gcpNaturalLanguage
            自然言語処理クラス
        """
        return self.gNL
