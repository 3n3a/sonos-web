

# in reality users and session_info would be persistent (e.g. database, file, ...) and passwords obviously hashed
from typing import Dict
from fastapi import Request


users = {
    'user': b'$2b$12$UCuCq9Lix9CKOaR3PTg8LuXvQPuXSPsiYLfC9hruwM20kHkBeggK.'
}
session_info: Dict[str, Dict] = {}

def pop_session(id):
    session_info.pop(id)

def add_session(id, value):
    session_info[id] = value

def get_session(id):
    return session_info[id]

def is_authenticated(request: Request) -> bool:
    return session_info.get(request.session.get('id'), {}).get('authenticated', False)
