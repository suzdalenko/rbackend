from ..myresponse import SetLocateAddress, DiscoJsonResponse

def index_page(request):
    response_data = {'author': 'Alexey Suzdalenko'}
    return  DiscoJsonResponse(response_data)