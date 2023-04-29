from soco import discover

class Sonos:
    def __init__(self) -> None:
        self.discovered_zones = []

    def update_discovered_zones(self) -> None:
        self.discovered_zones = list(discover())

    def get_zone_by_uid(self, uid):
        self.update_discovered_zones()
        for zone in self.discovered_zones:
            if zone.uid == uid:
                return zone

sonos = Sonos()