from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from stats.models import AverageFaceEncoding


@csrf_exempt
@require_http_methods(["GET"])
def stats(request):  # noqa: ARG001
    average_face_encodings = AverageFaceEncoding.objects.first()
    data = {
        "number_of_images_processed": average_face_encodings.number_of_images_processed,
        "average_face_encodings": average_face_encodings.get_face_encoding(),
    }
    return JsonResponse(data)
