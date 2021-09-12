import urllib.parse
from datetime import datetime
from flask import request
from flask_restful import Resource
from share_image.utils.decorators import (
    application_jwt_required,
    perm_required
)
from share_image.utils.http_reponses import error, success
from share_image.models.user import User
from share_image.models.shared_image import SharedImage
from share_image.models.dashboard_user import DashboardUser

class Backoffice(Resource):
    PAGE_SIZE = 10
    @application_jwt_required
    # @perm_required(role="can_access_backoffice")
    def get(self, jwt_data):
        try:
            page_number = int(request.args.get("pg", 0))
            user = User.objects(id=jwt_data.user_id).first()
            if not user:
                return error('Usuário não encontrado', 404)
            
            limit = Backoffice.PAGE_SIZE
            skip_pages = Backoffice.PAGE_SIZE * page_number
            images = []
            total = SharedImage.objects.count()
            
            shared_images = SharedImage.objects.order_by("-created_at")
            # .skip(skip_pages).limit(limit)
            
            page_size = len(shared_images)

            if len(shared_images) > 0:
                for img in shared_images:
                    
                    # dash_user = DashboardUser.objects(id=).first()
                    # us = User.objects(id=dash_user.user).first()
                    # print(us.name)
                    images.append(
                        {
                            'user': img.user.user.name,
                            'created_at': str(datetime.strftime(img.created_at, "%Y-%m-%d")),
                            'path': img.path
                        }
                    )
            return success({
                'list': images,
                "pagination": {
                        "total": total,
                        "actual_page": page_number,
                        "page_size": page_size,
                }
            })
        except Exception as e:
            print(e)
            return error('Erro inesperado', 500)