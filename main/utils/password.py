from main.security import bcrypt


def generate_password_hash(password):
    """
    Generate hashed password for user.

    :param password: Plaintext password
    :return: A string that is encrypted password
    """

    return bcrypt.generate_password_hash(password)


def update_password_hash_in_dict(data):
    """
    Remove old plaintext password from a dict and update
    it with a new hashed password.

    :param data: A dict contains password field
    :return: updated dict
    """

    if data:
        # Replace password with hashed password stored in password_hash
        data.update({
            'password_hash': bcrypt.generate_password_hash(data.get('password'))
        })
        data.pop('password')

    return data
