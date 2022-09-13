from flask_restful import Resource, reqparse, abort
from flask import session, request
from flask_login import current_user
from ..scripts import EditTxt

class Auth:
    from ..models import Account, db

    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, help="Username Must Be Present", required=True)
    parser.add_argument('password', type=str, help="Password Must Be Present", required=True)

    @property
    def json(self):
        args = self.parser.parse_args()
        return args.get("username", None), args.get("password", None)

    def account_exists(self, username: str, password: str = ""):
        """
        checks whether an account exists. if a password param is present it checks if a username AND password exists else it will check just the name
        """
        
        if password:
            return self.Account.query.filter_by(username=username, password=password).first()

        return self.Account.query.filter_by(username=username).first()

    def add_account(self, username: str = "", password: str = ""):
        """
        Adds a new account to the database
        """
        if all([username, password]):
            account = self.Account(username=username, password=password)
            self.db.session.add(account)
            self.db.session.commit()
            return account
        else:
            _username, _password = self.json
            if _username and _password:
                account = self.Account(username=_username, password=_password)
                self.db.session.add(account)
                self.db.session.commit()
                return account

    def delete_account(self, username) -> None:
        """
        Deletes a account from the database
        """
        account = self.Account.query.filter_by(username=username).first()
        self.db.session.delete(account)
        self.db.session.commit()
        

class Words(Resource):

    add_word = reqparse.RequestParser()
    add_word.add_argument("word", type=str, help="Invalid Request Body. Must Not Contain Any Symbols And Be Exactly 5 Characters")

    @property
    def words(self):
        _words = EditTxt.get_words()
        return _words


    def get(self):
        return {
            "words": self.words
        }

    def post(self):
        args = self.add_word.parse_args()
        word = args["word"].strip()
        words = self.words
        words.append(word)
        if isinstance(words, tuple):
            return abort(400, message="Invalid Request Body. Must Not Contain Any Symbols And Be Exactly 5 Characters")
        
        EditTxt.write_words(words)
        return {
            "words": self.words,
            "added": word
        }, 201

class Register(Resource, Auth):
    def get(self):
        return abort(404, message="Invalid Request Method. To Register/Login Go To /register | /login")

    def post(self) -> None:
        if self.account_exists(self.json[0]):
            return abort(400, message="Account Exists")
        
        if self.add_account(): # already implements parsing
            return {"registered": True}, 201
        return {"Server Error": True}, 500

class Login(Resource, Auth):
    def get(self):
        return abort(404, message="Invalid Request Method. To Register/Login Go To /register | /login")

    def post(self) -> None:
        _username, _password = self.json
        if _username and _password:
            if self.account_exists(_username, _password):
                return {"valid": True}
        return abort(401, message="Invalid Credentials")

class TodaysWord(Resource):

    def get(self):
        return abort(404, message="Nope Don't Even Try It")

    def post(self):
        from json import loads

        _json = loads(request.data)
        _word_guessed = _json.get("word")

        if request.headers.get("Authorization", None) != "SUPER SECRET ADMIN KEY":
            return abort(401, message="Invalid Key")

        if "word" not in session:
            session["word"] = EditTxt.get_random_word()

        def get_spaces(word, guessed) -> str:
            def replace_index(string, index, char) -> str:
                if index in range(len(string)):
                    if index == 0:
                        return f"{char}{string[1:]}"

                    return f"{string[:index]}{char}{string[index + 1:]}"

            ret = "_____"
            try:
                for index, (char, guessed_char) in enumerate(zip(word, guessed)):
                    if char == guessed_char:
                        ret = replace_index(ret, index, "G")
                    elif guessed_char in word:
                        ret = replace_index(ret, index, "O")
            finally:
                return ret

        return {"word": get_spaces(session["word"], _word_guessed), "username": current_user.username}

class AwardPoint(Resource):
    def get(self, username):
        return abort(404, message="Nope Don't Even Try It")

    def post(self, username):
        if request.headers.get("Authorization", None) != "SUPER SECRET ADMIN KEY":
            return abort(401, message="Invalid Key")

        account = Auth().account_exists(username)
        account.score += 1
        Auth.db.session.commit()

class AwardLoss(Resource):
    def get(self, username):
        return abort(404, message="Are You Feeling Ok?")

    def post(self, username):
        if request.headers.get("Authorization", None) != "SUPER SECRET ADMIN KEY":
            return abort(401, message="Invalid Key")

        account = Auth().account_exists(username)
        account.losses += 1
        Auth.db.session.commit()