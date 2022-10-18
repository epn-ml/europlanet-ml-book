#!/usr/bin/env python3
from datetime import datetime as dt, timedelta as td
import pandas as pd

philpott = pd.read_excel('jgra55678-sup-0002-Table_SI-S01.xlsx')
philpott['timestamp']=philpott.apply(lambda x: dt(year=int(x['Year']), month=1, day=1) + td(days=x['Day of year']-1, minutes=x['Minute'], hours=x['Hour'], seconds=x['Second']), axis=1)
phx = philpott.pivot_table(index=['Orbit number'], columns=['Boundary number'], values=['timestamp'])['timestamp'].reset_index()
phy = phx.rename({1: "SK outer in", 2: "SK inner in", 3: "MP outer in", 4: 'MP inner in', 5: 'MP inner out', 6: 'MP outer out', 7: 'SK inner out', 8: 'SK outer out', 'Orbit number': 'ORBIT'}, axis=1).rename_axis(None, axis=1).drop([9, 10], axis=1)
phy.to_csv('philpott.csv')
