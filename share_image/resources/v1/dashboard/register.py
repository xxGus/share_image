import datetime
import re
from base64 import b64decode
from io import BytesIO

from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token
)
from share_image.utils.crypto import hash_string
from share_image.utils.data_validation import validate_email
from share_image.utils.http_reponses import error, success
from share_image.utils.decorators import (
    data_required
)
from share_image.models.user import ( User, Email )
from share_image.models.dashboard_user import DashboardUser
from share_image.models.permission_group import PermissionGroup

class Register(Resource):
    @data_required({'email', 'password', 'name', 'birthday', 'gender'})
    def post(self):
        try:
            data = request.json

            email = data.get("email")
            if not validate_email(email):
                return error("Email inválido.")
            
            user = User.objects(email__value=email).first()
            if user:
                return error("usuário já cadastrado.", 401)

            user_permissions = PermissionGroup.objects(name="dashboard-user").first()

            # TODO: validar email
            user = User(
                name=data.get("name"),
                password=hash_string(data.get("password")),
                email=Email(value=email, validated=True),
                permissions=user_permissions.id
            )
            user.save()
            
            dash_user = DashboardUser(
                birthday=data.get("birthday"),
                gender=data.get("gender"),
                user=user.id
            )

            dash_user.save()
            return success({
                "name": user.name,
                "access_token": create_access_token(
                    {
                        "user_id": str(user.id),
                        "permissions": user.permissions.permitted,
                    },
                    fresh=True,
                ),
                "refresh_token": create_refresh_token(
                    {
                        "user_id": str(user.id),
                        "permissions": user.permissions.permitted,
                    }
                ),
            })
        except Exception as e:
            print(e)
            return error('Erro inesperado', 500)