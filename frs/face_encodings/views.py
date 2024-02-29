import face_recognition
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


@csrf_exempt
@require_http_methods(["POST"])
async def generate_face_encoding(request):
    if not request.FILES:
        return JsonResponse(status=422, data={"message": "No image sent!"})

    uploaded_file = request.FILES["upload_file"]

    file_image = face_recognition.load_image_file(uploaded_file.file)
    face_encodings = face_recognition.face_encodings(file_image)

    if not face_encodings:
        return JsonResponse(status=422, data={"message": "No faces found!"})

    # Just get the first face
    face_encoding = face_encodings[0]

    response = {"message": "OK", "face_encoding": list(face_encoding)}
    return JsonResponse(response)
