import bcrypt


class Auth:

    def hash_password(self, password):

        return bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        )

    def verify_password(
        self,
        password,
        hashed
    ):

        return bcrypt.checkpw(
            password.encode("utf-8"),
            hashed
        )