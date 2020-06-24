import os
from datetime import datetime, timedelta

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pymeters.settings")
    import django
    django.setup()

    from station.communicate import Comm, Counter
    from station.models import Profile, Cell

    #date = datetime.combine(date.today(), time()) - timedelta(days=1)
    #date = datetime(2018, 1, 14)
    for dt in [datetime(2019, 1, i + 18) for i in range(3)]:
        print('-' * 80)
        print(dt)

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

                        profile = cnt.get_profile(dt, en_type[en_i])

                        if profile is None:
                            print("Неполный профиль", profile)
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

                                print("Created ", o)
                                dtm += timedelta(minutes=30)
                            except Exception as e:
                                print(e, cell, dt, dtm.time(), profile[i])

            except Exception as e:
                print(e, cell)
            finally:
                comm.close()
