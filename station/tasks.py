from datetime import timedelta

from celery.utils.log import get_task_logger

from pymeters import celery_app
from station.communicate import Counter, Comm
from station.models import Cell, Profile, get_energy_type_names


@celery_app.task
def celery_get_profile(com_port, cell_id, dt):

    logger = get_task_logger(__name__)
    logger.info('start task celery_get_profile')

    comm = Comm(com_port)
    cell = Cell.objects.get(cell_id)
    errs = []
    res = "success"
    """
    try:
        comm.open()
        cnt = Counter(cell.serial_number, comm)
        if cnt.auth():

            for en_i, en_type in get_energy_type_names():

                profile = cnt.get_profile(dt, en_type)

                if profile is None:
                    errs.append("Неполный профиль {}".format(profile))
                    if res != "error":
                        res = "warning"
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

                        errs.append("Created  {}".format(o))
                        dtm += timedelta(minutes=30)
                    except Exception as e:
                        errs.append("Exception {} {} {} {} {}".format(e, cell, dt, dtm.time(), profile[i]))
                        res = "error"

    except Exception as e:
        errs.append("Exception {} {}".format(e, cell))
        return {"res": res, "error": "\n".join(errs)}

    finally:
        comm.close()
        return {"res": res, "error": "\n".join(errs)}
    """
