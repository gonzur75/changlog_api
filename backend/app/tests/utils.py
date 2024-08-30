from app.modules.auth import create_jwt_token


def get_test_auth_header_and_user(user_factory):
    user = user_factory()
    jwt_token = create_jwt_token(username=user.username)
    return {"Authorization": f"Bearer {jwt_token}"}, user
