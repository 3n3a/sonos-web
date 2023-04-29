from fastapi import Request
from nicegui import ui

from auth import is_authenticated, pop_session
from fastapi.responses import RedirectResponse

def create():
    @ui.page('/logout')
    def logout(request: Request) -> None:
        if is_authenticated(request):
            pop_session(request.session['id'])
            request.session['id'] = None
            return RedirectResponse('/login')
        return RedirectResponse('/')