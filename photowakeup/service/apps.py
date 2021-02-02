from django.apps import AppConfig
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.join(os.path.dirname(__file__)))))#os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..')))
ROOT_PATH = os.path.dirname(os.path.abspath(os.path.join(os.path.dirname(__file__))))
print(ROOT_PATH)


class ServiceConfig(AppConfig):
    name = 'service'