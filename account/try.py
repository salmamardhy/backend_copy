from django.http import HttpResponse

def my_view(request):
    # Print isi dari request ke console
    print("Request Method:", request.method)
    print("Request Headers:", request.headers)
    print("Request GET Parameters:", request.GET)
    print("Request POST Parameters:", request.POST)
    print("User:", request.user)

    # Kembalikan response
    return HttpResponse("Check your console for request details.")
