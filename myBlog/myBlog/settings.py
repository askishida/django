"""
Django settings for myBlog project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
#from urllib.parse import urlparse
#import mysql.connector
#import pandas as pd
#import pandas.io.sql as psql
import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

with open('/etc/secret_key.txt') as f:
  SECRET_KEY =f.read().strip()
# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = True
DEBUG = False
def always_show_toolbar(request):
   return True

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': '%s.always_show_toolbar' % __name__,
}





ALLOWED_HOSTS = ["my_domain_name","160.16.227.228","127.0.0.1","localhost"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'helloworld',
    'members',
    'posts.apps.PostsConfig',
    'contact',
    'info',
    'debug_toolbar',
    'ckeditor',
    'ckeditor_uploader',
    'froala_editor',
    'crispy_forms',    

    'django_js_reverse',
    'rest_framework',
    'corsheaders',
    'webpack_loader',
    'todos.apps.TodosConfig',
    'locationmap',
    'search',
    'taggit',
    'taggit_templatetags2',
    'feedreader',
#    'sidebar',
#    'django_elasticsearch_dsl',

]



SITE_ID = 1

CRISPY_TEMPLATE_PACK = "bootstrap4"

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'bundles/' # end with slash
        }
}

#ELASTICSEARCH_DSL={
#    'default': {
#        'hosts': 'localhost:9200'
#    },
#}


CKEDITOR_UPLOAD_PATH = "uploads/"
#CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/",
CKEDITOR_IMAGE_BACKEND = "pillow"
#以下は入れると動かない。
#CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor"

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'height': 500,
        'toolbar_Custom': [
            ['Styles', 'Format', 'Bold', 'Italic', 'Underline','Pink_line','Strike', 'SpellChecker', 'Undo', 'Redo','CodeSnippet', 'Youtube','LocationMap'],
            ['Link', 'Unlink', 'Anchor'],
            ['Image', 'Flash', 'Table', 'HorizontalRule'],
            ['TextColor', 'BGColor'],
            ['Smiley','SpecialChar'],['Source'],
        ],
        'extraPlugins': ','.join(['codesnippet', 'youtube','locationmap']),        

        'locationMapPath': "/home/totinoki/testApp/templates/",
        'ckfinder': True,


    },
    'special': {
        'toolbar': 'Special',
        'toolbar_Special': [
            ['Bold', 'CodeSnippet', 'Youtube', 'LocationMap'],
        ],
        'extraPlugins': ','.join(['codesnippet', 'youtube','locationmap']),   
    },

    'special2': {
        'skin': 'moono',
        # 'skin': 'office2013',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_YourCustomToolbarConfig': [
            {'name': 'document', 'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates']},
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
            {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
            {'name': 'forms',
             'items': ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
                       'HiddenField']},
            '/',
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
                       'Language']},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            {'name': 'insert',
             'items': ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']},
            '/',
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
            {'name': 'about', 'items': ['About']},
            '/',  # put this to force next toolbar on new line
            {'name': 'yourcustomtools', 'items': [
                # put the name of your editor.ui.addButton here
                'Preview',
                'Maximize',

            ]},
        ],

        'toolbar': 'YourCustomToolbarConfig',  # put selected toolbar config here
        # 'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
        # 'height': 291,
        # 'width': '100%',
        # 'filebrowserWindowHeight': 725,
        # 'filebrowserWindowWidth': 940,
        # 'toolbarCanCollapse': True,
        # 'mathJaxLib': '//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML',
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            'uploadimage', # the upload image feature
            # your extra plugins here
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            # 'devtools',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath'
        ]),
    }
}




MIDDLEWARE = [

    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
   # 'csp.middleware.CSPMiddleware',
]

CORS_ORIGIN_WHITELIST = (
    'localhost:3001/',
    'localhost:3001',
    '127.0.0.1:3001/',
    '127.0.0.1:3001',
    'mydomain/frontend',
    'mydomain/frontend/',
)


ROOT_URLCONF = 'testApp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates',os.path.join(BASE_DIR, 'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
#以下は動かない。
#FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'
WSGI_APPLICATION = 'myBlog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

#with open('/etc/secret_key.txt') as f:
#  SECRET_KEY =f.read().strip()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':'sample',
	'USER':'adminuser',
	'PASSWORD':'***',
	'HOST':'localhost',
	'PORT':'8889',
	'OPTIONS':{
	   #'init_command':"SET sql_mode='STRICT_TRAS_TABLES'",
            'charset': 'utf8mb4',
	},
	'TEST':{
	   'NAME':'test_sample'
	}
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'ja'

#TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'mymailaccount@yyy.com'

with open('/etc/email_key.txt') as f:
  EMAIL_HOST_PASSWORD =f.read().strip()

EMAIL_PORT = 587
EMAIL_USE_TLS =True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
#以下で動作確認済み
STATIC_URL = '/static/'
#STATIC_ROOT = '/static/'
#STATIC_ROOT = os.path.join(BASE_DIR, "static/")
STATIC_ROOT = "static/"
#以下追加。webpack使う場合やrestframeworkに関係。
'''
STATICFILES_DIRS= (
    os.path.join(BASE_DIR, "assets"),
)
'''
#BASE_PATH = os.path.abspath(os.path.split(__file__)[0])
#MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
MEDIA_ROOT = 'media/'
#print("STATICFILES_DIRS = %s" % STATICFILES_DIRS)
print("BASE_DIR= %s" % BASE_DIR)
#print("STATIC_ROOT= %s" % STATIC_ROOT)
#print("STATIC_ROOT= %s" % STATIC_ROOT)
print("MEDIA_ROOT= %s" % MEDIA_ROOT)
print("MEDIA_URL= %s" % MEDIA_URL)
#print("CKEDITOR_BASEPATH = %s" % CKEDITOR_BASEPATH)
print("CKEDITOR_UPLOAD_PATH  =%s" % CKEDITOR_UPLOAD_PATH)
