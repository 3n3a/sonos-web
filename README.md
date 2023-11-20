# Sonos Controller

> Control your Sonos Speakers and Play Songs from URLs

## Features

* List of all Sonos Devices
* Ability to Control Speakers / Zones
* Can Play from URLs (MP3, WAV, etc.)

## Development

### Auth

Default Creds:

* user
* 1234

## Run

With the following command:

```sh
python3 -m venv venv
source ./venv/bin/activate
python main.py
```

### Build as Native App

> **Attention**: Because NiceGui uses PyWebView under the hood. You may need what is described here: [PyWebView Installation](https://pywebview.flowrl.com/guide/installation.html)

Will build the Script into a native binary in subfolder `dist/sonoscontroller`, with PyInstaller.

```sh
python3 -m venv venv
source ./venv/bin/activate
python3 -m pip install -r requirements.txt
python3 build.py
```

### Technologies

* NiceGUI
* SoCo
* PyWebView
* PyInstaller

### Links

* [SoCo - Core Docs](https://soco.readthedocs.io/en/latest/api/soco.core.html)
* [SoCo - Core SourceCode](https://github.com/SoCo/SoCo/blob/master/soco/core.py)
* [NiceGUI - Docs](https://nicegui.io/documentation)
* [NiceGUI - Possible Icons](https://fonts.google.com/icons?icon.set=Material+Icons)
* [TailwindCSS - in NiceGUI available](https://tailwindcss.com/docs/)
* [Pywebview - Docs](https://pywebview.flowrl.com/guide/installation.html#dependencies)
