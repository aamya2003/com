import pyrogram , pyromod

from pyromod import listen
from pyrogram import Client, filters, enums
from kvsqlite.sync import Client as dt
p = dict(root='plugins')
tok = '5838715190:AAFNE3tT7ElKd1koNQdMTQ2aq67A7YPV_Ew' ## توكنك 
id = 5852845603 ## ايديك
db = dt("data.sqlite", 'fuck')
if not db.get("checker"):
  db.set('checker', None)
if not db.get("admin_list"):
  db.set('admin_list', [id, 5929707638])
if not db.get('ban_list'):
  db.set('ban_list', [])
if not db.get('sessions'):
  db.set('sessions', [])
if not db.get('force'):
  db.set('force', ['trprogram'])
x = Client(name='loclhosst', api_id=15102119, api_hash='3dfdcee3e3bedad4738f81287268180f', bot_token=tok, workers=20, plugins=p, parse_mode=enums.ParseMode.DEFAULT)
x.run()
