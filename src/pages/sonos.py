import time
from fastapi import Request
from nicegui import ui

from auth import get_session, is_authenticated
from fastapi.responses import RedirectResponse

from sonos import sonos

WAIT_AFTER_PLAY = 2 # seconds

def create():
    @ui.refreshable
    def current_volume(device) -> None:
        ui.label(f'current volume: {device.volume}')

    def set_relative_volume(device, volume) -> None:
        device.set_relative_volume(volume)
        current_volume.refresh()

    @ui.refreshable
    def play_pause(device) -> None:
        current_transport_state = device.get_current_transport_info()["current_transport_state"]
        print(current_transport_state)
        if current_transport_state == "PLAYING":
            ui.button('Pause', on_click=lambda: pause_refresh(device)).props('icon=pause')
        else:
            ui.button('Play', on_click=lambda: play_refresh(device)).props('icon=play_arrow')

    def play_refresh(device):
        device.play()
        time.sleep(WAIT_AFTER_PLAY)
        play_pause.refresh()

    def pause_refresh(device):
        device.pause()
        play_pause.refresh()

    @ui.refreshable
    def mute_unmute(device) -> None:
        is_muted = device.mute
        if is_muted:
            ui.button('Unmute', on_click=lambda: unmute_refresh(device)).props('icon=volume_up')
        else:
            ui.button('Mute', on_click=lambda: mute_refresh(device)).props('icon=volume_off')
        current_volume.refresh()

    def unmute_refresh(device) -> None:
        device.mute = False
        mute_unmute.refresh()

    def mute_refresh(device) -> None:
        device.mute = True
        mute_unmute.refresh()

    def play_song_url(url, device) -> None:
        device.play_uri(url)
        track_info_ui.refresh()

    @ui.refreshable
    def track_info_ui(device) -> None:
        track_info = device.get_current_track_info()
        ui.label('Current Track').classes('text-2xl font-bold')
        with ui.card().tight() as card:
            ui.image(track_info['album_art'])
            with ui.card_section():
                ui.label(track_info["title"]).classes('font-bold')
                ui.label(f'{track_info["artist"]} • {track_info["album"]}')

    @ui.page('/sonos/{id}', title='Sonos Device Control')
    def sonos_ctrl(id: str, request: Request) -> None:
        if not is_authenticated(request):
            return RedirectResponse('/login')
        session = get_session(request.session['id'])

        title = f'Sonos Device - {id}'
        device = sonos.get_zone_by_uid(id)

        with ui.header(elevated=True).classes('items-center justify-between'):
            with ui.row().classes('items-center'):
                ui.button('', on_click=lambda: ui.open('/')).props('outline round icon=arrow_back').classes('text-white')
                ui.label(title)

            ui.label(f'Hello {session["username"]}!')

            # NOTE we navigate to a new page here to be able to modify the session cookie (it is only editable while a request is en-route)
            # see https://github.com/zauberzeug/nicegui/issues/527 for more details
            ui.button('', on_click=lambda: ui.open('/logout')).props('outline round icon=logout').classes('text-white')

        with ui.row().classes('w-full justify-center mt-5'):
            ui.label(title).classes('text-3xl')

        with ui.row().classes('w-full justify-center mt-10'):
            with ui.column().classes('w-2/3 items-center'):
                if device is not None:
                    with ui.row():
                        with ui.column():
                            track_info_ui(device)
                        
                        with ui.column():
                            ui.label(f'Ip: {device.ip_address}')
                            current_volume(device)
                            ui.button('Volume Up', on_click=lambda: set_relative_volume(device, 1)).props('icon=volume_up')
                            ui.button('Volume Down', on_click=lambda: set_relative_volume(device, -1)).props('icon=volume_down')
                            play_pause(device)
                            mute_unmute(device)

                    with ui.row():
                        with ui.card().classes('absolute-center'):
                            url = ui.input('Song Url')
                            ui.button('Play Song', on_click=lambda: play_song_url(url.value, device))
                else:
                    ui.label('Device not found')