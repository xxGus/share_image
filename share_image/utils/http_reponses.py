def success(params: dict = {}, status_code: int = 200):
    response = params.copy()
    response.update({"success": True})
    return response, status_code


def error(msg: str, status_code: int = 400):
    response = {"success": False, "msg": msg}
    return response, status_code
