"""
認証情報などの環境変数を外部ファイルから取得するための関数
"""
import os
import pathlib
from dotenv import load_dotenv


dirname = pathlib.Path(__file__).parents[0]
dotenv_path = dirname/".env"
load_dotenv(dotenv_path)

LINE_ACCESS_TOKEN = os.environ.get("LINE_ACCESS_TOKEN")

GCP_API_KEY = os.environ.get("GCP_API_KEY")
IBM_API_KEY = os.environ.get("IBM_API_KEY")
MS_API_KEY = os.environ.get("MS_API_KEY")

IBM_TARNS_USERNAME = os.environ.get("IBM_TARNS_USERNAME")
IBM_TARNS_PASSWORD = os.environ.get("IBM_TARNS_PASSWORD")
IBM_TtoS_USERNAME = os.environ.get("IBM_TtoS_USERNAME")
IBM_TtoS_PASSWORD = os.environ.get("IBM_TtoS_PASSWORD")
IBM_StoT_USERNAME = os.environ.get("IBM_StoT_USERNAME")
IBM_StoT_PASSWORD = os.environ.get("IBM_StoT_PASSWORD")
