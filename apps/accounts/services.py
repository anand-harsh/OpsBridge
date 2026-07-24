from django.contrib.auth import get_user_model

User = get_user_model()


def create_user(*, email, username, password, first_name="", last_name=""):
    user = User(
        email=email,
        username=username,
        first_name=first_name,
        last_name=last_name,
    )

    user.set_password(password)
    user.save()

    return user