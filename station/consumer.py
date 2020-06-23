from datetime import datetime

from channels.generic.websocket import AsyncWebsocketConsumer

from station.communicate import Comm, Counter


class GetInfoConsumer(AsyncWebsocketConsumer):

    async def receive(self, text_data):
        print(text_data)

        for i in range(10):
            try:
                comm = Comm("COM2")
                comm.open()
                cnt = Counter("007259077000018", comm)
                profile = cnt.get_profile(datetime(2018, 12, 16), "PE")
                print(profile)
                profile = cnt.get_profile(datetime(2018, 12, 16), "PI")
                print(profile)
                profile = cnt.get_profile(datetime(2018, 12, 16), "QE")
                print(profile)
                profile = cnt.get_profile(datetime(2018, 12, 16), "QI")
                print(profile)
                comm.close()
            except Exception as e:
                await self.send(str(e))
