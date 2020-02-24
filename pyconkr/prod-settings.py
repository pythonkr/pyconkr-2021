from pyconkr.settings import *
import os
import requests

DEBUG = True
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'www.pycon.kr',
    'dev.pycon.kr',
    'pycon.kr',
]

# Append ELB healthcheck hostname(internal ip address)
# https://stackoverflow.com/questions/55718292/getting-400s-from-aws-elb-hostcheck-to-work-with-django-allowed-hosts-in-aws-ec
if 'ECS_CONTAINER_METADATA_URI' in os.environ:
    ELB_HEALTHCHECK_HOSTNAMES = [ip for network in
                                 requests.get(os.environ['ECS_CONTAINER_METADATA_URI']).json()[
                                     'Networks']
                                 for ip in network['IPv4Addresses']]
    print(f'Append ELB healthcheck hostname: {ELB_HEALTHCHECK_HOSTNAMES}')
    ALLOWED_HOSTS += ELB_HEALTHCHECK_HOSTNAMES

db_env_keys = ['POSTGRES_HOST', 'POSTGRES_NAME', 'POSTGRES_PORT',
               'POSTGRES_USER', 'POSTGRES_PASSWORD']

for key in db_env_keys:
    if not os.getenv(key):
        print(f'You should set {key}')
        exit(1)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_NAME'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
    }
}


aws_env_keys = ['AWS_ACCESS_KEY_ID',
                'AWS_SECRET_ACCESS_KEY', 'AWS_STORAGE_BUCKET_NAME']

for key in aws_env_keys:
    if not os.getenv(key):
        print(f'You should set {key}')
        exit(1)

AWS_DEFAULT_ACL = 'public-read'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = 'ap-northeast-2'
AWS_S3_SIGNATURE_VERSION = 's3v4'
