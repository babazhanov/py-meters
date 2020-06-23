import os
import time
from datetime import datetime, timedelta, date, time


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kmacnt.settings")
    import django
    django.setup()

    from station.communicate import Comm, Counter
    from station.models import Profile, Cell

    #date = datetime.combine(date.today(), time()) - timedelta(days=1)
    #date = datetime(2018, 1, 14)
    for date in [datetime(2019, 1, i+18) for i in range(3)]:
        print('-' * 80)
        print(date)

        comm = Comm("COM2")

        en_type = {
            1: "PE",
            2: "PI",
            3: "QE",
            4: "QI"
        }

        for cell in Cell.objects.all():
            try:
                print(cell)
                
                comm.open()

                cnt = Counter(cell.serial_number, comm)

                if cnt.auth():
                    cell = Cell.objects.get(serial_number=cell.serial_number)

                    for en_i in en_type:

                        profile = cnt.get_profile(date, en_type[en_i])

                        if profile is None:
                            print("Неполный профиль", profile)
                            continue

                        dtm = date
                        for i in range(48):

                            try:
                                o = Profile.objects.create(
                                    cell=cell,
                                    date=date,
                                    time=dtm.time(),
                                    value_type=en_i,
                                    value=profile[i]
                                )

                                print("Created ", o)
                                dtm += timedelta(minutes=30)
                            except Exception as e:
                                print(e, cell, date, dtm.time(), profile[i])

            except Exception as e:
                print(e, cell)
            finally:
                comm.close()
