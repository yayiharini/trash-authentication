from django.utils.deprecation import MiddlewareMixin


class SameSiteMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        #print("entered", response.data)
        if 'jwt' in response.cookies:
            if not response.cookies['jwt']['samesite']:
                print("no same site")
                response.cookies['jwt']['samesite'] = 'None'
        return response
