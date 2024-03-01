import face_recognition
import redis
from asgiref.sync import sync_to_async
from django.core.cache import cache
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from stats.models import AverageFaceEncoding

from face_encodings.models import ImageFaceEncoding
from face_encodings.utils import generate_message, get_file_hash


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
            face_encodings = await generate_face_encodings(file_hash, uploaded_file)

    if not face_encodings:
        return JsonResponse(status=422, data={"message": "No faces found!"})

    message = await generate_message(len(face_encodings))

    response = {
        "message": message,
        "file_hash": file_hash,
        "face_encoding": list(face_encodings[0]),
    }
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["GET"])
async def face_encoding(request, file_hash):  # noqa: ARG001
    face_encodings = await get_existing_face_encodings(file_hash)
    message = await generate_message(len(face_encodings))
    if not face_encodings:
        return JsonResponse(status=422, data={"message": "No face encoding found!"})
    response = {
        "message": message,
        "file_hash": file_hash,
        "face_encoding": list(face_encodings[0]),
    }
    return JsonResponse(response)


async def get_existing_face_encodings(file_hash):
    face_encodings = cache.get(key=file_hash)
    if face_encodings:
        return face_encodings

    image_face_encoding_query = ImageFaceEncoding.objects.filter(file_hash=file_hash)
    if await image_face_encoding_query.aexists():
        image_face_encoding = await image_face_encoding_query.aget()
        return await image_face_encoding.get_face_encoding()

    return []


async def generate_face_encodings(file_hash, uploaded_file):
    file_image = face_recognition.load_image_file(uploaded_file.file)
    face_encodings = face_recognition.face_encodings(file_image)
    if face_encodings:
        await store_instances(file_hash, face_encodings[0])
    cache.set(key=file_hash, value=face_encodings)
    return face_encodings


async def store_instances(file_hash, face_encoding):
    image = ImageFaceEncoding(file_hash=file_hash)
    await sync_to_async(image.save)()
    await image.insert_face_encoding(face_encoding)

    # Move to a Celery task as a background task
    # Using global lock for avoding race conditions
    r = redis.Redis(host="redis_semaphore")
    with r.lock("global_lock"):
        average_face_encoding = await AverageFaceEncoding.objects.afirst()
        await sync_to_async(average_face_encoding.update_average_face_encodings)(image)
