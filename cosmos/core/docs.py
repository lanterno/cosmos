from coreapi import Document

from cosmos.accounts.docs import ACCOUNTS

BASE_URL = '/api/v1/'
BASE_AUTH_URL = BASE_URL + 'auth/'

SCHEMA = Document(
    title='Sheetu API',
    description="""
        Documents the sheetu project API.
    """,
    content={
        'Users and Authentication': ACCOUNTS,
    }
)
