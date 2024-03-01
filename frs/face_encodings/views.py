import hashlib

import face_recognition
import redis
from django.core.cache import cache
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from face_encodings.models import ImageFaceEncoding


@csrf_exempt
@require_http_methods(["POST"])
async def generate_face_encoding(request):
    if not request.FILES:
        return JsonResponse(status=422, data={"message": "No image sent!"})

    uploaded_file = request.FILES["upload_file"]
    file_hash = await get_file_hash(uploaded_file.read())

    # Set a semaphore with the hash of the image uploaded, in order to avoid
    # processing an image twice due to race conditions.
    r = redis.Redis(host="redis_semaphore")
    with r.lock(file_hash):
        face_encodings = await get_existing_face_encodings(file_hash)
        if not face_encodings:
            face_encodings = await generate_face_encodings(uploaded_file)
            cache.set(key=file_hash, value=face_encodings)

    if not face_encodings:
        return JsonResponse(status=422, data={"message": "No faces found!"})

    message = await generate_message(len(face_encodings))

    response = {"message": message, "face_encoding": list(face_encodings[0])}
    return JsonResponse(response)


async def get_file_hash(file_content):
    return hashlib.sha256(file_content).hexdigest()


async def get_existing_face_encodings(file_hash):
    face_encodings = cache.get(key=file_hash)
    if face_encodings:
        return face_encodings

    image_face_encoding_query = ImageFaceEncoding.objects.filter(file_hash=file_hash)
    if await image_face_encoding_query.aexists():
        image_face_encoding = await image_face_encoding_query.aget()
        return await image_face_encoding.get_face_encoding()

    return []


async def generate_face_encodings(uploaded_file):
    file_image = face_recognition.load_image_file(uploaded_file.file)
    return face_recognition.face_encodings(file_image)


async def generate_message(number_of_faces):
    message = "OK"
    if number_of_faces > 1:
        message += " - Multiple faces. Returning first"
    return message
