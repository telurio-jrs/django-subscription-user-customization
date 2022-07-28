import os

import jwt


def auth(payload):
    return jwt.encode(
        payload=payload,
        key=os.getenv('JWT_SECRET', 'INSECURE'),
        algorithm=os.getenv('JWT_ALGORITHM', 'INSECURE')
    )
