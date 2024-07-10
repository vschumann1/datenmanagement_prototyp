from django.shortcuts import redirect
from django.conf import settings

class SimplePasswordMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Überprüfen, ob der Benutzer das Passwort eingegeben hat
        if not request.session.get('password'):
            # Wenn der Pfad nicht zur Passwort-Seite führt und keine statische Datei ist
            if not request.path.startswith('/myapp/password/') and not request.path.startswith(settings.STATIC_URL):
                return redirect('myapp:password_protect')
        response = self.get_response(request)
        return response
