import os
from datetime import datetime, timedelta
from random import randrange

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pymeters.settings")
    import django
    django.setup()

    from station.communicate import Comm, Counter
    from station.models import Profile, Cell

    for dt in [datetime(2020, 6, 22 + i) for i in range(3)]:
        print('-' * 80)
        print(dt)

        en_type = {
            1: "PE",
            2: "PI",
            3: "QE",
            4: "QI"
        }

        cell = Cell.objects.first()

        prfls = [randrange(300, 600) for i in range(48)]

        dtm = dt
        for i in range(48):

            try:
                o = Profile.objects.create(
                    cell=cell,
                    date=dt,
                    time=dtm.time(),
                    value_type=1,
                    value=prfls[i]
                )

                print("Created ", o)
                dtm += timedelta(minutes=30)
            except Exception as e:
                print(e, cell, dt, dtm.time(), profile[i])
