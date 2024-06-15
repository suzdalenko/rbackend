from myapp.myresponse import DiscoJsonResponse

class Api:

    def example(request):
        return DiscoJsonResponse({"api":"example"}) 