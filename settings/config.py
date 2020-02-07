import os
import sys


class Config(object):
    DEBUG = False
    SECRET_KEY = "secret key"
    UPLOAD_FOLDER = "./temp_uploads"
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = ['json']


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    UPLOAD_FOLDER = "./uploads"
