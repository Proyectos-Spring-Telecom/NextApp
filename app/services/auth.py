# app/services/auth.py

import requests
from app.config import AUTH_URL, API_TIMEOUT_SECONDS

def login(user_name: str, password: str):
    """
    POST TokenApp con { username, password }.
    Devuelve:
      { "ok": True, "token": "...", "data": <json> } en éxito
      { "ok": False, "error": "mensaje" } en error
    """
    payload = {"username": user_name, "password": password}

    try:
        resp = requests.post(AUTH_URL, json=payload, timeout=API_TIMEOUT_SECONDS)
    except requests.RequestException as ex:
        return {"ok": False, "error": f"Sin conexión ({ex})"}

    # Éxito típico .NET: 200/201
    if resp.status_code in (200, 201):
        try:
            jd = resp.json() if resp.content else {}
        except Exception:
            jd = {}

        # Token tolerante a distintos keys comunes
        token = (
            jd.get("token")
            or jd.get("Token")
            or jd.get("access_token")
            or jd.get("AccessToken")
            or jd.get("jwt")
        )

        return {"ok": True, "token": token, "data": jd}

    # Error con cuerpo JSON
    try:
        err = resp.json()
        msg = (
            err.get("message")
            or err.get("Message")
            or err.get("error")
            or err.get("Error")
            or str(err)
        )
    except Exception:
        msg = f"HTTP {resp.status_code}"

    return {"ok": False, "error": msg}
