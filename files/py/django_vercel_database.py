with open('/var/task/django/db/backends/sqlite3/_functions.py', mode='r') as f:
    content = f.read().replace('deterministic=True,', 'deterministic=False,')

with open('/var/task/django/db/backends/sqlite3/_functions.py', mode='w') as f:
    f.write(content)
