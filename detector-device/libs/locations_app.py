import asyncio
import winsdk.windows.devices.geolocation as wdg

def get_win_location():
    async def getCoords():
        locator = wdg.Geolocator()
        pos = await locator.get_geoposition_async()
        return [pos.coordinate.latitude, pos.coordinate.longitude]
    try:
        return asyncio.run(getCoords())
    except PermissionError:
        raise Exception("ERROR: You need to allow applications to access you location in Windows settings. Or just turn on location services on windows.")
    
class LocationsApp:
    def __init__(self):
        self.check_access_permission()
        
    def check_access_permission(self):
        return get_win_location()
        
    def get_current_location(self):
        coords = get_win_location()
        return {"lat": coords[0], "lng": coords[1]}