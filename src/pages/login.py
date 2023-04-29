import uuid
from fastapi import Request
from nicegui import ui
import bcrypt

from auth import is_authenticated, add_session, users
from fastapi.responses import RedirectResponse

def create():
    @ui.page('/login', title='Login')
    def login(request: Request) -> None:
        def try_login() -> None:  # local function to avoid passing username and password as arguments
            # salt = bcrypt.gensalt()
            # hashed_pass = bcrypt.hashpw(password.value, salt)
            stored_hash = users.get(username.value)
            if stored_hash and bcrypt.checkpw(bytes(password.value, 'utf-8'), stored_hash):
                add_session(request.session['id'], {'username': username.value, 'authenticated': True})
                ui.open('/')
            else:
                ui.notify('Wrong username or password', color='negative')

        if is_authenticated(request):
            return RedirectResponse('/')
        request.session['id'] = str(uuid.uuid4())  # NOTE this stores a new session ID in the cookie of the client
        with ui.card().classes('absolute-center'):
            username = ui.input('Username').on('keydown.enter', try_login)
            password = ui.input('Password').props('type=password').on('keydown.enter', try_login)
            ui.button('Log in', on_click=try_login)