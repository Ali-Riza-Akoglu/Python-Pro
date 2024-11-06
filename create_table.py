import sqlite3

# Veritabanı bağlantısı
conn = sqlite3.connect('quiz.db')  # mevcut quiz.db veritabanını kullanıyoruz
cursor = conn.cursor()

# Kullanıcı puanları tablosunu oluşturma (tablo yoksa)
cursor.execute('''CREATE TABLE IF NOT EXISTS scores
                (username TEXT, score INTEGER)''')

conn.commit()
conn.close()
