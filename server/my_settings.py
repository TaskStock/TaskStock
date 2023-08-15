from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

import environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# reading .env file
environ.Env.read_env(BASE_DIR / '../.env')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')
DB_SECRET = env('DB_SECRET')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', #1
        'NAME': 'taskstock_db', #2
        'USER': 'admin', #3                      
        'PASSWORD': DB_SECRET,  #4              
        'HOST': 'database-1-instance-1.cc5vqvk6zxzm.ap-northeast-2.rds.amazonaws.com',   #5                
        'PORT': '3306', #6
        'OPTION': {
            'init_command': 'SET sql_mode="STRICT_TRANS_TABLES"'
        }
    }
}
SECRET_KEY =env('SECRET_KEY')