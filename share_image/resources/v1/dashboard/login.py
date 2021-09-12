import datetime

from flask import request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    # jwt_refresh_token_required
)
from flask_restful import Resource

from share_image.utils.crypto import hash_string
from share_image.utils.data_validation import validate_email
from share_image.utils.http_reponses import error, success
from share_image.utils.decorators import (
    data_required
)
from share_image.models.user import User

class Login(Resource):
    @data_required({'email', 'password'})
    def post(self):
        try:
            data = request.json
            email = data.get("email")
            if not validate_email(email):
                return error("Email inválido.")

            user = User.objects(email__value=email, email__validated=True, password=hash_string(data.get('password'))).first()

            if not user:
                return error('Usuário não encontrado', 404)

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

class RefreshToken(Resource):
    """This resource is used to crate new access token based in refresh token."""
    #TODO: verificar porque nao está encontrando o decorator
    # @jwt_refresh_token_required
    def get(self):
        """Return new access token."""
        session_data = get_jwt_identity()
        return success({"access_token": create_access_token(session_data, fresh=False)})

