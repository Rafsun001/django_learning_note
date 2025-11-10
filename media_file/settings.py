
from pathlib import Path
from datetime import timedelta
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_URL = 'static/'
########################################################
###################### Media File Handling #############
########################################################
"""  
STATIC_URL variable er niche nicher code ta likhte hobe. Amn na j variable er porer line tai hobe. Just niche jknw jaygay. BASE_DIR tw amnei thake shobar upore
"""
import os
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
 ####################
 


