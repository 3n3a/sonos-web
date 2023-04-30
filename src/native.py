from starlette.middleware.sessions import SessionMiddleware

from nicegui import app, ui

import pages.login as login
import pages.logout as logout
import pages.index as index
import pages.sonos as sonos

app.add_middleware(SessionMiddleware, secret_key='asdf231k2l312dfjsldj1232312')  # use your own secret key here
app.title = 'Sonos Controller'

login.create()
logout.create()

index.create()
sonos.create()

app.native.window_args['resizable'] = True
app.native.start_args['debug'] = False

# ui.run()
ui.run(native=True, window_size=(1024, 786), fullscreen=False, reload=False)