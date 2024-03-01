import hashlib


async def get_file_hash(file_content):
    return hashlib.sha256(file_content).hexdigest()


async def generate_message(number_of_faces):
    message = "OK"
    if number_of_faces > 1:
        message += " - Multiple faces. Returning first"
    return message
