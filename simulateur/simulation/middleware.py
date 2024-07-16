# simulation/middleware.py
class CustomXFrameOptionsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['X-Frame-Options'] = 'SAMEORIGIN'  # or 'ALLOW-FROM https://example.com'
        return response
