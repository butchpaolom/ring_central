import datetime

def LoggerMiddleware(get_response):
    def middleware(request):
        if request.path == '/requests':
            response = get_response(request)
            return response
        time = datetime.datetime.now()
        if not request.session:
            request.session.save()
        response = get_response(request)
        if 'requests' not in request.session:
            request.session['requests'] = []
        reqs = request.session['requests']
        reqs.append(f'[{time}] {request.method} {request.path} {request.scheme}')
        request.session['requests'] = reqs

        return response

    return middleware