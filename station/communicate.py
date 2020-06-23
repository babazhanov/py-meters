import serial
import time
from datetime import datetime
import re

"""
МЭК 61107-2001
ГОСТ IEC 61107-2011
Обмен данными при считывании показаний счетчиков,
тарификации и управлении нагрузкой. Прямой локальный обмен данными
"""


class Comm:
    """Класс взаимодействия с COM-портом """

    STX = '\x02'
    SOH = '\x01'
    ETX = '\x03'
    bETX = b'\x03'

    def __init__(self, port):
        self.__port = port
        self.__conn = None

    def open(self):
        self.__conn = serial.Serial(self.__port, 9600, timeout=5, stopbits=1, parity='E', bytesize=7)

    def close(self):
        if isinstance(self.__conn, serial.Serial):
            self.__conn.close()

    def write_str(self, string):
        # print("----->")
        # print(string)
        for c in string:
            self.__conn.write((ord(c),))

    def read_str(self):
        # print("<-----")
        b = self.__conn.read()
        if b == b'':
            return b''
        else:
            ret = b
            n = self.__conn.inWaiting()
            while n > 0:
                ret += self.__conn.read(n)
                time.sleep(0.5)
                n = self.__conn.inWaiting()

            # print(ret)
            return ret

    def read_str_for_etx(self):
        b = self.__conn.read(1)
        ret = b''
        while b != Comm.bETX:
            ret += b
            b = self.__conn.read(1)
            if b == b'':
                return ret

        # + BCC_CODE
        return ret + b + self.__conn.read(1)

    # ответ
    def ack(self):
        self.write_str('\x06\x30\x35\x31\r\n')


def BCC(string):
    ret = 0
    for c in string:
        ret += ord(c)
    return chr(ret & 0x7f)


class Counter:
    """Класс взаимодействия со счётчиком"""

    def __init__(self, serial_number, comm):
        self.__serial = serial_number
        self.__comm = comm

    def auth(self):
        """Аутентификация на счётчике"""
        _start_sym = '/?'
        _stop_sym = '!\r\n'
        "Передаём специальные символы и серийный номер"
        self.__comm.write_str(_start_sym + self.__serial + _stop_sym)
        ret = self.__comm.read_str()  # здесь может быть проверка
        self.__comm.ack()
        ret = self.__comm.read_str()  # здесь может быть проверка

        if ret != b'':
            return True

    def get_profile(self, date, energy_type):
        """Загрузка из счётчика профиля энергии [PE, PI, QE, QI] за сутки date"""
        self.auth()

        date = date.strftime("%d.%m.%y")

        mes = 'R1' + Comm.STX + 'GRA' + energy_type + '(' + date + '.1.48)' + Comm.ETX
        mes = Comm.SOH + mes + BCC(mes)
        self.__comm.write_str(mes)
        mes = self.__comm.read_str()
        vec = re.findall(b'\([0-9\.\-]+\)', mes)

        # конец чтения
        self.__comm.write_str(Comm.SOH + 'B0' + Comm.ETX + '\x75')

        if len(vec) == 48:
            return [v[1:-1] for v in vec]
        else:
            return None


if __name__ == "__main__":
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
