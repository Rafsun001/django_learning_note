

import os
from django.core.asgi import get_asgi_application

### Need to add ########
from channels.routing import ProtocolTypeRouter, URLRouter
import app.routing # --> here app means app name and routing means routing.py file which need to be created inside app.
#################

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectContainer.settings') # --> here projectContainer is dynamic based on the new project.

### Need to add ########
application = ProtocolTypeRouter({
    'http' : get_asgi_application(),
    'websocket': URLRouter(
        app.routing.websocket_urlpatterns
    )
})
#################