from django.http import HttpResponse


def index(request):
    html_content = """
       <!DOCTYPE html>
       <html>
       <head>
           <title>Welcome to the Luminal API</title>
       </head>
       <body>
           <p>Hello world</p>
       </body>
       </html>
       """
    return HttpResponse(html_content)