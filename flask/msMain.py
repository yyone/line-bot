from ms.msVision import msVision
import settings


class msMain:
    """
    Microsoft AzureのML用APIにアクセスするクラス
    """

    def __init__(self):
        self.mVision = msVision(settings.MS_API_KEY)

    def Vision(self):
        """
        Returns
        -------
        mVision : msVision
            画像処理クラス
        """
        return self.mVision
