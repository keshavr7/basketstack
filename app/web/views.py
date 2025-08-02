import requests
import os
from django.http import HttpResponse

from web.settings import DEBUG, STATIC_ROOT

def app(request):
    """Main app view that serves the React app"""
    if DEBUG:
        # Try to proxy to Vite dev server first
        try:
            vite_url = f"http://host.docker.internal:5173{request.path}"
            if request.GET:
                vite_url += f"?{request.GET.urlencode()}"
            
            response = requests.get(vite_url, timeout=2)
            return HttpResponse(
                response.content, 
                content_type=response.headers.get('content-type', 'text/html')
            )
        except (ImportError, Exception):
            # Fall through to serve built files
            pass
    
    # Serve built index.html from STATIC_ROOT
    index_path = os.path.join(STATIC_ROOT, 'fe', 'index.html')
    try:
        with open(index_path, 'r') as f:
            return HttpResponse(f.read(), content_type='text/html')
    except FileNotFoundError:
        return HttpResponse(
            '<div id="root">Run <code>npm run build</code> and <code>python manage.py collectstatic</code></div>', 
            content_type='text/html'
        )
