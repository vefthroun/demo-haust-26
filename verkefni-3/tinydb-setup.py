from tinydb import TinyDB
import os # to generate secret key with operating system in flask app


# 1. Uppsetning: Býr til db.json ef hún er ekki til með indent og utf-8 stuðningi
db = TinyDB('db.json', indent=2, encoding='utf-8', ensure_ascii=False)
users_table = db.table('users')
posts_table = db.table('posts')


# 2. Setja inn Admin (stjórnanda)
# insert() skilar sjálfkrafa ID-inu sem skjalið fær
admin_id = users_table.insert({
    'username': 'vefstjori',
    'role': 'admin',
    'password': 'psw_123'
})

# 3. Setja inn almennan notanda
user_id = users_table.insert({
    'username': 'jon_jonsson',
    'role': 'user',
    'password': 'psw_456'
})

# 4. Setja inn spjallpóst sem tengist notanda-IDinu
posts_table.insert({
    'author_id': user_id,  # Tenging við notandann [Conversation]
    'content': 'Hæ öll! Þetta er minn fyrsti póstur.',
    'timestamp': '2026-06-14'
})