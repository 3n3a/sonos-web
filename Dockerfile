FROM zauberzeug/nicegui:latest

COPY requirements.txt .

RUN python3 -m pip install -r requirements.txt

COPY src .