import time
from dataclasses import dataclass, field
from typing import List


@dataclass
class User:
    name: str = ''
    level: int = 0
    address: str = ''


@dataclass
class Authorization:
    user: User = field(default_factory=User)
    jwt: str = ''


@dataclass
class Request:
    path: str
    method: str
    auth: Authorization


class AccessGatewayFilter:
    def __init__(self):
        pass

    def filter(self, request: Request) -> bool:
        request_uri = request.path
        method = request.method

        if self.is_start_with(request_uri):
            return True

        try:
            token = self.get_jwt_user(request)
            user = token.user
            if user.level > 2:
                self.set_current_user_info_and_log(user)
                return True
        except Exception:
            return False
        return False

    def is_start_with(self, request_uri: str) -> bool:
        start_with: List[str] = ["/api", "/login"]
        for s in start_with:
            if request_uri.startswith(s):
                return True
        return False

    def get_jwt_user(self, request: Request) -> Authorization:
        token = request.auth
        user = token.user

        if token.jwt.startswith(user.name):
            jwt_str_date = token.jwt[len(user.name):]

            try:
                jwt_timestamp = int(jwt_str_date)
            except ValueError:
                return Authorization()  # empty token

            now = int(time.time())
            if (now - jwt_timestamp) >= 3 * 24 * 60 * 60:
                return Authorization()  # empty token
        return token

    def set_current_user_info_and_log(self, user: User) -> None:
        print(f"{user.name} {user.address} {int(time.time())}")
