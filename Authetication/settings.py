
STATIC_URL = 'static/'
################################ 
######## Email OTP send ########
##################################
"""  
Go to setting.py file of project folder. Then copy the below code and paste it below the STATIC_URL = 'static/'. You just need to add the company email by which the OTP will send to the user eamil and app password. To create app password Follow the instruction of the Link: https://www.geeksforgeeks.org/python/setup-sending-email-in-django-project/

"""
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = "Sender Email name"
EMAIL_HOST_PASSWORD = "app password" 
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

################################ 
##### For Token Permission #####
################################

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

######################################## 
#### Access and Refresh token time #####
#######################################

import timedelta 
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=8),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=10), # Example refresh token lifetime
}