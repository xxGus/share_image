import re
from datetime import datetime
from base64 import b64decode
from io import BytesIO

from flask import request
from flask_restful import Resource
from share_image.utils.crypto import hash_string
from share_image.utils.http_reponses import error, success
from share_image.utils.s3 import upload_image
from share_image.utils.decorators import (
    application_jwt_required,
    perm_required
)
from share_image.models.dashboard_user import DashboardUser
from share_image.models.shared_image import SharedImage

class ImageUpload(Resource):
    # TODO: verificar decorator de permissão
    @application_jwt_required
    def post(self, jwt_data):
        try:
            data = request.json
            today = datetime.now()
            
            user = DashboardUser.objects(user=jwt_data.user_id).first()
            if not user:
                return error('Usuário não encontrado', 404)

            img_body = re.search(r"(?<=base64,).+", data.get("img"))
            mime_type = re.search(r"(?<=data:).+(?=;base64)", data.get("img"))

            if not mime_type or not img_body:
                return error("Imagem mal formatada.")

            mime_type = mime_type.group(0)
            extension = mime_type.split("/")[-1]

            if extension.lower() not in ["jpg", "png", "gif", "svg", "bmp"]:
                return error("Extensão não permitida: use jpg, png, gif, svg e bmp.")

            timestamp = str(today).replace(" ", "+")

            image_name = f"share_image/{hash_string(timestamp)}.{extension}"
            in_memory = BytesIO()
            in_memory.write(b64decode(img_body.group(0)))
            in_memory.seek(0)
            path_img = upload_image(in_memory, image_name)
            shared_image = SharedImage(
                path=path_img,
                user=user.id
            )
            shared_image.save()

            return success({
                "link": shared_image.path 
            })
        except Exception as e:
            print(e)
            return error("Erro inesperado", 500)
