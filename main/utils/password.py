from main.security import bcrypt


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
