def get_desc_apiType(type, service):
    """
    API種別を返す関数

    Parameters
    ----------
    type : int
        各MLサービスを判別する数字の種別
    service : str
        gcp/ibm/msの文字列で判別するAPIサービスの種別

    Returns
    -------
    text : str
        API種別の文字列
    """
    text = ''

    # GCP
    if service == 'gcp':
        if type == 1:
            text += '物体の検知 or 分類'
        elif type == 2:
            text += '文章の抽出'
        elif type == 3:
            text += '顔情報、表情などの検知'
        elif type == 4:
            text += '構造物から名所の検知'
        elif type == 5:
            text += 'ロゴ検知'
        elif type == 6:
            text += '有害コンテンツ検知'
        elif type == 21:
            text += '自然言語処理'
        elif type in {22, 23, 24, 25}:
            text += '自然言語処理：'
            if type == 22:
                text += '構文解析'
            elif type == 23:
                text += 'エンティティ分析'
            elif type == 24:
                text += '感情分析'
            elif type == 25:
                text += 'エンティティ感情分析'

    # IBM (Watson)
    elif service == 'ibm':
        if type == 1:
            text += '物体の検知 or 分類'
        elif type == 21:
            text += 'テキスト to 音声変換'

    # Microsoft
    elif service == 'ms':
        if type == 1:
            text += '物体の検知'
        elif type == 2:
            text += '解説'
        elif type == 3:
            text += '性別＆年齢識別'
        elif type == 4:
            text += '有害コンテンツ検知'

    return text


def get_desc_help():
    """
    基礎的なヘルプの文字列用関数

    Returns
    -------
    text : str
        ヘルプ文字列
    """
    text = '【使い方】\n'
    text += '\n'
    text += '各機械学習サービスや言語、モードを切り替えて使ってください。\n'
    text += '\n'

    text += '------------\n'
    text += '[サービス切り替え]\n'
    text += '\n'
    text += '以下のテキストを投稿することで、サービスを切り替えることができます。\n'
    text += '\n'
    text += 'gcp: Google Cloud Platform（デフォルト）\n'
    text += 'ibm: IBM Watoson\n'
    text += 'ms : Microsoft Azure\n'
    text += '\n'

    text += '------------\n'
    text += '[言語切り替え]\n'
    text += '\n'
    text += '以下のテキストを投稿することで、言語を切り替えることができます。\n'
    text += '\n'
    text += 'ja: 日本語（デフォルト）\n'
    text += 'en: 英語\n'
    text += '\n'

    text += '------------\n'
    text += 'モード切り替えに関しては、各サービスヘルプで確認してください。以下のテキストを投稿すれば、ヘルプを確認できます。\n'
    text += '\n'
    text += '[各サービスヘルプ]\n'
    text += '\n'
    text += 'hg: gcp ヘルプ\n'
    text += 'hi: ibm ヘルプ\n'
    text += 'hm: ms ヘルプ\n'
    text += '\n'

    text += '------------\n'
    text += '\n'
    text += 'なお、「0」を投稿すると、デフォルト設定に戻すことができます。\n'
    text += 'また、「i」を投稿すると、現在選択しているのサービスや言語、モードを確認することができます。\n'
    text += '\n'

    return text


def get_desc_gcp_help():
    """
    GCP用のヘルプの文字列用関数

    Returns
    -------
    text : str
        ヘルプ文字列
    """
    text = '【gcpモードの説明】\n'
    text += '\n'

    text += '------------\n'
    text += '[画像識別]\n'
    text += '\n'
    text += '以下の番号を投稿することで、画像識別のモードを切り替えることができます。\n'
    text += '\n'
    text += '1: 物体の検知 or 分類（デフォルト）\n'
    text += '2: 文章の抽出\n'
    text += '3: 顔情報、表情などの検知\n'
    text += '4: 構造物から名所の検知\n'
    text += '5: ロゴ検知\n'
    text += '6: 有害コンテンツの検知\n'
    text += '\n'

    text += '------------\n'
    text += '[音声識別]\n'
    text += '\n'
    text += '音声識別はモード切り替えは必要ありません。音声データを投稿すれば識別されます。\n'
    text += '言語は、選択している言語モードが適用されます。\n'
    text += '\n'

    text += '------------\n'
    text += '[テキスト（自然言語）識別]\n'
    text += '\n'
    text += '以下の番号を投稿することで、自然言語識別のモードを切り替えることができます。\n'
    text += 'モード切替後は、テキスト／画像／音声どれを投稿しても識別されます。なお、画像は文章が含まれる画像を投稿してください。\n'
    text += '\n'
    text += '21: 文法、感情の識別\n'
    text += '23: エンティティ分析\n'
    text += '\n'

    text += '------------\n'
    text += '\n'
    text += 'モード切り替えを行なってから、改めて投稿してください。なお、「0」を入力すると、デフォルト設定に戻すことができます。'
    text += '\n'

    return text


def get_desc_ibm_help():
    """
    IBM用のヘルプの文字列用関数

    Returns
    -------
    text : str
        ヘルプ文字列
    """
    text = '【ibmモードの説明】\n'
    text += '\n'

    text += '------------\n'
    text += '[画像識別]\n'
    text += '\n'
    text += '以下の番号を投稿することで、画像識別のモードを切り替えることができます。\n'
    text += '\n'
    text += '1: 物体の検知 or 分類（デフォルト）\n'
    text += '\n'

    text += '------------\n'
    text += '[音声識別]\n'
    text += '\n'
    text += '音声識別はモード切り替えは必要ありません。音声データを投稿すれば識別されます。\n'
    text += '言語は、選択している言語モードが適用されます。\n'
    text += '\n'

    text += '------------\n'
    text += '[テキスト（自然言語）識別]\n'
    text += '\n'
    text += '以下の番号を投稿することで、テキスト識別のモードを切り替えることができます。\n'
    text += 'モード切替後は、テキスト／画像／音声どれを投稿しても識別されます。なお、画像は文章が含まれる画像を投稿してください。\n'
    text += 'なお、音声変換の言語は、選択している言語モードが適用されます。\n'
    text += '\n'
    text += '21: テキスト to 音声変換\n'
    text += '22: \n'
    text += '\n'

    text += '------------\n'
    text += '\n'
    text += 'モード切り替えを行なってから、改めて投稿してください。なお、「0」を入力すると、デフォルト設定に戻すことができます。'
    text += '\n'

    return text


def get_desc_ms_help():
    """
    Microsoft用のヘルプの文字列用関数

    Returns
    -------
    text : str
        ヘルプ文字列
    """
    text = '【msモードの説明】\n'
    text += '\n'

    text += '------------\n'
    text += '[画像識別]\n'
    text += '\n'
    text += '以下の番号を投稿することで、画像識別のモードを切り替えることができます。\n'
    text += '\n'
    text += '1: 物体の検知（デフォルト）\n'
    text += '2: 文章解説\n'
    text += '3: 性別＆年齢の識別\n'
    text += '4: 有害コンテンツの検知\n'
    text += '\n'

    text += '------------\n'
    text += '\n'
    text += 'モード切り替えを行なってから、改めて投稿してください。なお、「0」を入力すると、デフォルト設定に戻すことができます。'
    text += '\n'

    return text
