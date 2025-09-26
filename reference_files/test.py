import pymongoarrow as pma

from pymongoarrow.monkey import patch_all
patch_all()

from pymongo import MongoClient
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import pandas as pd


print("Script called.")
zoom = True

client = MongoClient()

database = client['flatsat']
coll = database['tlm']

r1 = coll.find_pandas_all({'mnemonic': 'OAR0_OSC_ACTMDL_RW'})
r2 = coll.find_pandas_all({'mnemonic': 'OAR1_OSC_ACTMDL_RW'})
r3 = coll.find_pandas_all({'mnemonic': 'OAR2_OSC_ACTMDL_RW'})
r4 = coll.find_pandas_all({'mnemonic': 'OAR3_OSC_ACTMDL_RW'})

tgt = coll.find_pandas_all({'mnemonic': 'EPH_TGTREL'})

r1.set_index('time', inplace=True)
r2.set_index('time', inplace=True)
r3.set_index('time', inplace=True)
r4.set_index('time', inplace=True)

tgt.set_index('time', inplace=True)

fig, (ax, tgtax, rgax) = plt.subplots(3)
fig.set_size_inches(18.5, 15.5)

ax.plot(r1.index, r1['OAR0_SPEED'], label='RW1 Speed')
ax.plot(r2.index, r2['OAR1_SPEED'], label='RW2 Speed')
ax.plot(r3.index, r3['OAR2_SPEED'], label='RW3 Speed')
ax.plot(r4.index, r4['OAR3_SPEED'], label='RW4 Speed')
ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=2))
ax.xaxis.set_minor_locator(mdates.MinuteLocator())
ax.set_xlabel("Time")
ax.set_ylabel("Speed (rad/s)")
ax.set_title("RW Speed (OARx_OSC_ACTMDL_RW.OARx_SPEED)")

ax.legend()

tgtax.plot(tgt.index, tgt['EPH_ELEVATIONSpotTarget'], label="Target Elevation")
tgtax.xaxis.set_major_locator(mdates.MinuteLocator(interval=2))
tgtax.xaxis.set_minor_locator(mdates.MinuteLocator())

tgtax.set_xlabel("Time")
tgtax.set_ylabel("Elevation (rad)")

tgtax.set_title("Target Elevation (EPH_TGTREL.EPH_ELEVATIONSpotTarget)")

rgax.plot(tgt.index, tgt['EPH_RANGESpotTarget'], label="Target Range")
rgax.xaxis.set_major_locator(mdates.MinuteLocator(interval=2))
rgax.xaxis.set_minor_locator(mdates.MinuteLocator())

rgax.set_xlabel("Time")
rgax.set_ylabel("Range (m)")

rgax.set_title("Target Range (EPH_TGTREL.EPH_RANGESpotTarget)")

ax.grid(True)
tgtax.grid(True)
rgax.grid(True)

if zoom:
  start = pd.Timestamp("2025-05-27 23:37:00")
  end = pd.Timestamp("2025-05-27 23:45:00")
  ax.set_xlim(left=start, right=end)
  ax.set_ylim(-100,150)
  tgtax.set_xlim(left=start, right=end)
  rgax.set_xlim(left=start, right=end)

fig.tight_layout(pad=3.0)
plt.show()



velerr = coll.find_pandas_all({'mnemonic': 'OER_POS_VEL_ERR'})
velerr.set_index('time', inplace=True)

atterr = coll.find_pandas_all({'mnemonic': 'OER_ATT_ERR'})
atterr.set_index('time', inplace=True)

fig, (ax1, ax2, ax3) = plt.subplots(3)

fig.set_size_inches(18.5, 15.5)
ax1.plot(velerr.index, velerr['OER_ESTVELERRMAG'], label="Velocity Error Mag")
ax1.xaxis.set_major_locator(mdates.MinuteLocator(interval=2))
ax1.xaxis.set_minor_locator(mdates.MinuteLocator())
ax1.set_title("Velocity Error Mag (OER_POS_VEL_ERR.OER_ESTVELERRMAG)")

ax1.set_xlabel("Time")
ax1.set_ylabel("Velocity Error Magnitude (m/s)")


ax2.plot(velerr.index, velerr['OER_ESTPOSERRMAG'], label="Position Error Mag")
ax2.xaxis.set_major_locator(mdates.MinuteLocator(interval=2))
ax2.xaxis.set_minor_locator(mdates.MinuteLocator())
ax2.set_title("Position Error Mag (OER_POS_VEL_ERR.OER_ESTPOSERRMAG)")

ax2.set_xlabel("Time")
ax2.set_ylabel("Position Error Magnitude (m)")

ax3.plot(atterr.index, atterr['OER_TOTATTERRMAG'], label="Attitude Error Mag")
ax3.xaxis.set_major_locator(mdates.MinuteLocator(interval=2))
ax3.xaxis.set_minor_locator(mdates.MinuteLocator())
ax3.set_title("Attitude Error Mag (OER_ATT_ERR.OER_TOTATTERRMAG)")

ax3.set_xlabel("Time")
ax3.set_ylabel("Attitude Error Magnitude (rad)")

if zoom:
  start = pd.Timestamp("2025-05-27 23:37:00")
  end = pd.Timestamp("2025-05-27 23:45:00")
  ax1.set_xlim(left=start, right=end)
  ax1.set_ylim(0,2)
  ax2.set_xlim(left=start, right=end)
  ax2.set_ylim(-500,1000)
  ax3.set_xlim(left=start, right=end)
  ax3.set_ylim(-0.01,0.01)

ax1.grid(True)
ax2.grid(True)
ax3.grid(True)


fig.tight_layout(pad=3.0)
plt.show()