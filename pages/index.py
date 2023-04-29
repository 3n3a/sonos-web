from fastapi import Request
from nicegui import ui

from auth import get_session, is_authenticated
from fastapi.responses import RedirectResponse

from sonos import sonos

def create():
    def get_sonos_table_config():
        columns = [
            {
                'name': 'id',
                'label': 'Id',
                'field': 'id',
            },
            {
                'name': 'ip',
                'label': 'IP Address',
                'field': 'ip',
                'sortable': 'true'
            },
            {
                'name': 'name',
                'label': 'Name',
                'field': 'name',
                'sortable': 'true'
            },
            {
                'name': 'play_mode',
                'label': 'Queue Play Mode',
                'field': 'play_mode',
                'sortable': 'true'
            },
            {
                'name': 'volume',
                'label': 'Volume',
                'field': 'volume',
            },
            {
                'name': 'bass',
                'label': 'Bass EQ',
                'field': 'bass',
            },
            {
                'name': 'treble',
                'label': 'Treble EQ',
                'field': 'treble',
            },
            {
                'name': 'loudness',
                'label': 'Loudness Enabled',
                'field': 'loudness',
            }
        ]
        rows = []
        sonos.update_discovered_zones()
        for zone in sonos.discovered_zones:
            rows.append({
                'id': zone.uid,
                'name': zone.player_name,
                'ip': zone.ip_address,
                'play_mode': zone.play_mode,
                'volume': zone.volume,
                'bass': zone.bass,
                'treble': zone.treble,
                'loudness': zone.loudness,
                'ctrl_url': f"/sonos/{zone.uid}"
            })
        return columns, rows


    @ui.page('/', title='Sonos Controller')
    def main_page(request: Request) -> None:
        if not is_authenticated(request):
            return RedirectResponse('/login')
        session = get_session(request.session['id'])

        title = 'Sonos Controller'

        with ui.header(elevated=True).classes('items-center justify-between'):
            ui.label(title)

            ui.label(f'Hello {session["username"]}!')

            # NOTE we navigate to a new page here to be able to modify the session cookie (it is only editable while a request is en-route)
            # see https://github.com/zauberzeug/nicegui/issues/527 for more details
            ui.button('', on_click=lambda: ui.open('/logout')).props('outline round icon=logout').classes('text-white')

        with ui.row().classes('w-full justify-center mt-5'):
            ui.label('Sonos Controller').classes('text-3xl')

        with ui.row().classes('w-full justify-center mt-10'):

            with ui.column().classes('w-2/3'):
                ui.label(f'Sonos Devices on Your Network').classes('text-2xl')

                columns, rows = get_sonos_table_config()
                table = ui.table(columns=columns, rows=rows, row_key='ip').classes('w-full')
                table.add_slot('header', r'''
                    <q-tr :props="props">
                        <q-th auto-width />
                        <q-th v-for="col in props.cols" :key="col.name" :props="props">
                            {{ col.label }}
                        </q-th>
                    </q-tr>
                ''')
                table.add_slot('body', r'''
                    <q-tr :props="props">
                        <q-td auto-width>
                            <a :href="props.row.ctrl_url">
                                <q-btn color="accent" label="Control" />
                            </a>
                        </q-td>
                        <q-td v-for="col in props.cols" :key="col.name" :props="props">
                            {{ col.value }}
                        </q-td>
                    </q-tr>
                ''')

