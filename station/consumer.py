from datetime import datetime

from channels.generic.websocket import JsonWebsocketConsumer

from ensfera.models import Preference
from station.communicate import Comm
from station.models import Cell


class GetInfoConsumer(JsonWebsocketConsumer):
    en_type = {
        1: "PE",
        2: "PI",
        3: "QE",
        4: "QI"
    }

    def receive_json(self, content):
        print(content)

        if content.get('cmd') == "start":
            dt = datetime.now().date()
            self.send_json({"date": str(dt)})

            com_port = Preference.objects.get_or_create(
                name="com-port",
                defaults={'value': 'COM2'}
            )[0].value
            comm = Comm(com_port)

            self.send_json({"com": str(comm)})

            for cell in Cell.objects.all():
                self.send_json({"cell": str(cell)})
                
                try:
                    comm.open()

                    cnt = Counter(cell.serial_number, comm)

                    if cnt.auth():
                        cell = Cell.objects.get(serial_number=cell.serial_number)

                        for en_i in self.en_type:

                            profile = cnt.get_profile(dt, self.en_type[en_i])

                            if profile is None:
                                #yield "Неполный профиль {}".format(profile)
                                self.send_json({"cell": "Неполный профиль {}".format(profile)})
                                continue

                            dtm = dt
                            for i in range(48):

                                try:
                                    o = Profile.objects.create(
                                        cell=cell,
                                        date=dt,
                                        time=dtm.time(),
                                        value_type=en_i,
                                        value=profile[i]
                                    )

                                    #yield "Created  {}".format(o)
                                    self.send_json({"cell": "Created  {}".format(o)})
                                    dtm += timedelta(minutes=30)
                                except Exception as e:
                                    self.send_json({"Exception": "{} {} {} {} {}".format(e, cell, dt, dtm.time(), profile[i])})
                                    #yield "Exception {} {} {} {} {}".format(e, cell, dt, dtm.time(), profile[i])

                except Exception as e:
                    self.send_json({"Exception": "{} {}".format(e, cell)})
                    #yield "Exception {} {}".format(e, cell)
                finally:
                    comm.close()

