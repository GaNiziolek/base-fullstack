"""Main entry point
"""
from pyramid.config    import Configurator
from cornice           import CorniceRenderer
import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

API_DB_STRING = os.getenv("API_DB_STRING")
engine = create_engine(API_DB_STRING, echo=True, future=True)
Session = sessionmaker(engine)


def datetime_adapter(obj, request):
    return obj.isoformat()

def main(global_config, **settings):

    config = Configurator(settings=settings)

    # O renderer padrão (CorniceRenderer) não cosnegue lidar 
    # com dados do tipo "datetime", então foi necessário 
    # implementar esse "adapter" que fosse possível tratar
    # esse tipo de  informações 
    json_renderer = CorniceRenderer()
    json_renderer.add_adapter(datetime.datetime, datetime_adapter)
    config.add_renderer('cornicejson', json_renderer)

    config.include("cornice")
    config.scan("api.views")
    return config.make_wsgi_app()

