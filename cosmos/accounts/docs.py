from coreapi import Link, Field

BASE_AUTH_URL = '/api/v1/auth/'

ACCOUNTS = {
    'register': Link(
        url=BASE_AUTH_URL + 'users/create/',
        action='post',
        description="""
            Register a new user

            Note: You have to activate your email address, before logging in.
        """,
        fields=[
            Field(
                name='email',
                required=True,
                location='formData',
            ),
            Field(
                name='password',
                required=True,
                location='formData',
            ),
            Field(
                name='first_name',
                required=False,
                location='formData',
            ),
            Field(
                name='last_name',
                required=False,
                location='formData',
            ),
        ]
    ),
    'activate': Link(
        url=BASE_AUTH_URL + 'users/activate/',
        action='post',
        description="""
            Activate account

            Note: Accounts are activated automatically for now.
        """,
        fields=[
            Field(
                name='uid',
                required=True,
                location='formData',
            ),
            Field(
                name='token',
                required=True,
                location='formData',
            ),
        ],
    ),
    'login': Link(
        url=BASE_AUTH_URL + 'token/create/',
        action='post',
        description="""
            User Login
        """,
        fields=[
            Field(
                name='email',
                required=True,
                location="formData",
                description='Email'
            ),
            Field(
                name='password',
                required=True,
                location="formData",
                description='Password'
            )
        ]
    ),
    'logout': Link(
        url=BASE_AUTH_URL + 'token/destroy/',
        action='post',
        description="""
        User Logout

        Just deletes the Token from the backend
        """,
        fields=[
            Field(
                name="Authorization",
                required=False,
                location="header",
                description="ex. Token XXX"
            ),
        ]
    ),
    'me': Link(
        url=BASE_AUTH_URL + 'me/',
        action='get',
        description="""
            Get logged-in user profile details
        """,
        fields=[
            Field(
                name="Authorization",
                required=False,
                location="header",
                description="ex. Token XXX"
            ),
        ]
    ),
    'update-me': Link(
        url=BASE_AUTH_URL + 'me/',
        action='patch',
        description="""
            Update Logged-in User Profile
        """,
        fields=[
            Field(
                name="Authorization",
                required=False,
                location="header",
                description="ex. Token XXX"
            ),
            Field(
                name='email',
                required=False,
                location='formData',
            ),
            Field(
                name='first_name',
                required=False,
                location='formData',
            ),
            Field(
                name='last_name',
                required=False,
                location='formData',
            ),
            Field(
                name='instagram_handle',
                required=False,
                location='formData',
            ),
            Field(
                name='birthdate',
                required=False,
                location='formData',
            ),
        ]
    ),
    'change-password': Link(
        url=BASE_AUTH_URL + 'password/',
        action='post',
        description="""
            Change Password
        """,
        fields=[
            Field(
                name="Authorization",
                required=False,
                location="header",
                description="ex. Token XXX"
            ),
            Field(
                name='current_password',
                required=True,
                location='formData',
            ),
            Field(
                name='new_password',
                required=True,
                location='formData',
            ),
        ],
    ),
    'reset-password': Link(
        url=BASE_AUTH_URL + 'password/reset/',
        action='post',
        description="""
            Reset Password

            Sends the user an email with a link(to the frontend). The link has two parts, a uid, and a token
            that should be extracted from the frontned in sent back to the backend for resetting password
            as explained in the reset-password-confirm endpoint documentation.
        """,
        fields=[
            Field(
                name='email',
                required=True,
                location='formData',
            ),
        ],
    ),
    'reset-password-confirm': Link(
        url=BASE_AUTH_URL + 'password/reset/confirm/',
        action='post',
        description="""
            Reset Password confirm

            Using the link sent in the email which contained a uid and a token,
            The frontend client should extract those values and send them to the backend through this endpoint
            along with the new password the user wants to update the password.
        """,
        fields=[
            Field(
                name='uid',
                required=True,
                location='formData',
            ),
            Field(
                name='token',
                required=True,
                location='formData',
            ),
            Field(
                name='new_password',
                required=True,
                location='formData',
            ),
        ],
    ),
    'social-login': Link(
        url=BASE_AUTH_URL + 'social/token_user/',
        action='post',
        description="""
            User Social Login "google, harvest, etc"

            current providers: "google-oauth2, harvest"
        """,
        fields=[
            Field(
                name='provider',
                required=True,
                location="formData",
                description='ex. google-oauth2'
            ),
            Field(
                name='code',
                required=True,
                location="formData",
                description='code received from social website'
            ),
            Field(
                name='redirect_uri',
                required=True,
                location="formData",
                description='redirect url'
            )
        ]
    ),
}
