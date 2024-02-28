from django.http import HttpResponse
from django.views.decorators.http import require_http_methods


@require_http_methods(["POST"])
async def generate_face_encoding(request):
    assert request is not None
    return HttpResponse("OK")
