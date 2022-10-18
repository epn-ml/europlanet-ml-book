#!/usr/bin/env python3
from time import sleep
from sys import argv
import calendar
import telnetlib
from datetime import datetime, timedelta

class HelioCoord:
    def __init__(self, body, dt_start, dt_end, interval):
        self.bodies = { "Mercury": "199", "Jupiter": "599", "Saturn": "699" }
        self.months = {v: k for k,v in enumerate(calendar.month_abbr)}
        if body not in self.bodies:
            raise Exception("Unsupported planet! Supported planet names: Mercury, Jupiter, Saturn")
        self.body = self.bodies[body]
        self.dt_start = dt_start
        self.dt_end = dt_end
        self.interval = interval


    def fetchall(self):
        step = timedelta(seconds=86400)
        xstart = datetime.strptime(self.dt_start, '%Y-%b-%d %H:%M')
        final_end = datetime.strptime(self.dt_end, '%Y-%b-%d %H:%M')
        while True:
            xend = xstart + step
            res = self.fetch(datetime.strftime(xstart, '%Y-%b-%d %H:%M'), datetime.strftime(xend, '%Y-%b-%d %H:%M'))
            for line in res:
                print("\t".join(line))
            xstart = xend
            if xstart >= final_end:
                break


    def fetch(self, dt_start, dt_end):
        commands = ['page',
                    self.body,
                    'E',
                    'V',
                    '@sun',
                    'eclip',
                    dt_start,
                    dt_end,
                    self.interval,
                    'n',
                    'J2000',
                    '1',
                    '1',
                    'N',
                    'n',
                    '2'
        ]
        tn = telnetlib.Telnet("horizons.jpl.nasa.gov", 6775)
        sleep(3)
        tn.read_very_eager()

        for c in commands:
            tn.write(c.encode('ascii') + b'\n')
            sleep(1)
            tn.read_very_eager()

        tn.write(b'n\n')
        sleep(4)
        result = b""
        i = 0
        while True:
            res = tn.read_some()
            result += res
            if res == b"" or result.find(b'$$EOE') != -1:
                break

        tn.write(b'q')
        sleep(1)
        tn.write(b'q\n')

        result = result.decode('ascii')

        res = result.split("$$")[1].replace("SOE", "").strip().split('\n')

        final = []
        for l in range(0, len(res), 3):
            line1 = res[l].split()
            line2 = res[l + 1].split()
            line3 = res[l + 2].split()
            final.append([f"{line1[3]}Z{line1[4]}",
                          line2[0], line2[1], line2[2],
                          line3[0], line3[1], line3[2]]
            )
        return final


def main():
    if len(argv) < 5:
        print("Usage: ./heliocoord.py Mercury|Jupiter|Saturn yyyy-Mon-ddZhh:mm yyyy-Mon-ddZhh:mm N[d|h|m]")
        print("Example: ./heliocoord.py Jupiter 1978-Apr-01Z00:00 1978-Apr-03Z15:00 10m")
        print("Output: YYYY-MM-DD hh:mm X Y Z VX VY VZ")
        exit()

    body = argv[1]
    dt_start, dt_end = argv[2].replace("Z", " "), argv[3].replace("Z", " ")
    interval = argv[4]
    hc = HelioCoord(body, dt_start, dt_end, interval)
    hc.fetchall()


if __name__ == "__main__":
    main()
