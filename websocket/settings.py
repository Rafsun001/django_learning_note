

INSTALLED_APPS = [
    'channels', # --> Only add channels app here
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app1',
    'rest_framework',
    'rest_framework_simplejwt'
]




ASGI_APPLICATION = 'projectContainer.asgi.application' # --> projectContainer is dynamic based on project.
"""  
In the position of WSGI_APPLICATION = 'projectContainer.wsgi.application' write ASGI_APPLICATION = 'projectContainer.asgi.application'
"""
############# Redis Channel layer ################
"""  
Copy and paste exactly same thing
"""
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.01", 6379)],
        },
    },
}
