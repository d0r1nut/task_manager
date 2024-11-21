def check_token(request):
    token = request.session.get('token')
    if token is None:
        return False
    return True