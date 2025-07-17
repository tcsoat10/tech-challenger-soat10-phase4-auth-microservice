from typing import Optional

from fastapi import Form


class OAuth2PasswordRequestFormCustom:
    def __init__(
        self,
        username: Optional[str] = Form(None, description="Username or CPF"),
        password: Optional[str] = Form(None, description="Password"),
    ):
        self.username = username
        self.password = password


__all__ = ["OAuth2PasswordRequestFormCustom"]
