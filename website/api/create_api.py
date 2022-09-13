from .api import (
    Words,
    Register,
    Login,
    TodaysWord,
    AwardPoint,
    AwardLoss
)
from flask_restful import Api, Resource

class CreateApi:

    api = None

    def __new__(cls, app, *args, **kwargs):
        """
        Only One Api Can Exist At One Given Time
        """
        if cls.api is None:
            cls.api = Api(app)
        return super().__new__(cls)

    def add_all(self) -> None:
        """
        Creates All Routes For Api
        """
        self.api.add_resource(Words, "/api/words", "/words")
        self.api.add_resource(Register, "/auth/register")
        self.api.add_resource(Login, "/auth/login")
        self.api.add_resource(TodaysWord, "/api/todays-word")
        self.api.add_resource(AwardPoint, "/api/award-point/<string:username>", "/award-point/<string:username>")
        self.api.add_resource(AwardLoss, "/api/award-loss/<string:username>", "/award-loss/<string:username>")

    def add_one(self, rsrc, *urls, **kwargs) -> None:
        """
        Adds A Custom Route To The Api
        """
        if issubclass(rsrc, Resource):
            self.api.add_resource(rsrc, *urls, **kwargs)
