from flask_jwt_extended import create_access_token


def generate_token(user):
    return create_access_token(identity=dict(
        id=user.id,
        firstName=user.first_name,
        lastName=user.last_name,
        email=user.email,
        role=user.role.value))
