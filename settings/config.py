import os
import sys

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "secret key"
    UPLOAD_FOLDER = "./temp_uploads"
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    UPLOAD_FOLDER = "./uploads"


class TestingConfig(Config):
    TESTING = True
