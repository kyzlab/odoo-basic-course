# standalone_client.py — calls Odoo from external Python script (not inside the addon)
import requests

ODOO_URL = 'http://localhost:10019'
DB = 'petshop_db'

session = requests.Session()

# Step 1: Authenticate — lấy session cookie
resp = session.post(f'{ODOO_URL}/web/session/authenticate', json={
    'jsonrpc': '2.0', 'method': 'call',
    'params': {'db': DB, 'login': 'admin', 'password': 'admin'}
})
uid = resp.json().get('result', {}).get('uid')
print(f'Logged in UID: {uid}')

# Step 2: Read pets via /web/dataset/call_kw
resp = session.post(f'{ODOO_URL}/web/dataset/call_kw', json={
    'jsonrpc': '2.0', 'method': 'call',
    'params': {
        'model': 'petshop.pet',
        'method': 'search_read',
        'args': [[['is_alive', '=', True]]],
        'kwargs': {'fields': ['name', 'gender', 'weight'], 'limit': 5}
    }
})
pets = resp.json().get('result', [])
for p in pets:
    print(p)
