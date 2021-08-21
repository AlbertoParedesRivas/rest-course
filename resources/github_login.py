from flask import g, request, url_for
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token
from oauth import github
from models.user import UserModel
from models.confirmation import ConfirmationModel

class GithubLogin(Resource):
    @classmethod
    def get(cls):
        return github.authorize(url_for("github.authorized", _external = True))

class GithubAuthorize(Resource):
    @classmethod
    def get(cls):
        response = github.authorized_response()

        if response is None or response.get("access_token") is None:
            error_response = {
                "error": request.args["error"],
                "error_description": request.args["error_description"]
            }
            return error_response

        g.access_token = response["access_token"]
        #Getting github username
        github_user = github.get("user")
        github_username = github_user.data["login"]
        #Gettting github email
        github_user_emails = github.get("user/emails")
        for email in github_user_emails.data:
            if email["primary"]:
                github_email = email["email"]

        user = UserModel.find_by_username(username=github_username)
        if not user:
            user = UserModel(username=github_username, email=github_email,password=None)
            user.save_to_db()
            confirmation = ConfirmationModel(user.id)
            confirmation.confirmed = True
            confirmation.save_to_db()

        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(user.id)

        return {"access_token": access_token, "refresh_token": refresh_token}, 200