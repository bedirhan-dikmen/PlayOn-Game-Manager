from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Veritabanı bağlantı bilgileri
db_config = {
    'host': 'localhost',
    'user': 'root', 
    'password': 'bilm317',
    'database': 'playon' 
}

@app.route('/')
def index():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM oyunlar")
    oyunlar = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', oyunlar=oyunlar)


@app.route('/add', methods=['GET', 'POST'])
def add_game():
    if request.method == 'POST':
        oyun_ad = request.form['oyun_ad']
        oyun_tur = request.form['oyun_tur']
        oyun_aciklamasi = request.form['oyun_aciklamasi']
        yayinci_ad = request.form['yayinci_ad']
        cikis_yili = request.form['cikis_yili']
        metacritic_puan = request.form['metacritic_puan']
        fiyat = request.form['fiyat']

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO oyunlar (oyun_ad, oyun_tur, oyun_aciklamasi, yayinci_ad, cikis_yili, metacritic_puan, fiyat)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (oyun_ad, oyun_tur, oyun_aciklamasi, yayinci_ad, cikis_yili, metacritic_puan, fiyat)
        )
        cursor.execute("INSERT INTO yayinci (yayinci_ad,oyun_ad) VALUES (%s,%s)",(yayinci_ad,oyun_ad))
        cursor.execute("INSERT INTO tur (oyun_tur,oyun_ad) VALUES (%s,%s)",(oyun_tur,oyun_ad))
        conn.commit()
        cursor.close()
        conn.close()
        
        return redirect('/')

    return render_template('add.html')


@app.route('/delete/<oyun_ad>', methods=['POST'])
def delete_game(oyun_ad):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM yayinci WHERE oyun_ad = %s", (oyun_ad,))
    cursor.execute("DELETE FROM tur WHERE oyun_ad = %s", (oyun_ad,))
    cursor.execute("DELETE FROM oyunlar WHERE oyun_ad = %s", (oyun_ad,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/')


@app.route('/update/<int:oyun_id>', methods=['GET', 'POST'])
def update_game(oyun_id):
    if request.method == 'POST':
        oyun_ad = request.form['oyun_ad']
        oyun_tur = request.form['oyun_tur']
        oyun_aciklamasi = request.form['oyun_aciklamasi']
        yayinci_ad = request.form['yayinci_ad']
        cikis_yili = request.form['cikis_yili']
        metacritic_puan = request.form['metacritic_puan']
        fiyat = request.form['fiyat']

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE oyunlar
            SET oyun_ad = %s, oyun_tur = %s, oyun_aciklamasi = %s, yayinci_ad = %s, cikis_yili = %s, metacritic_puan = %s, fiyat = %s
            WHERE oyun_id = %s
            """,
            (oyun_ad, oyun_tur, oyun_aciklamasi, yayinci_ad, cikis_yili, metacritic_puan, fiyat, oyun_id)
        )
        cursor.execute("UPDATE tur SET oyun_tur = %s,oyun_ad = %s WHERE oyun_ad = %s", (oyun_tur,oyun_ad,oyun_ad,))
        cursor.execute("UPDATE yayinci SET yayinci_ad = %s,oyun_ad = %s WHERE oyun_ad = %s", (yayinci_ad,oyun_ad,oyun_ad,))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/')

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM oyunlar WHERE oyun_id = %s", (oyun_id,))
    oyunlar = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('update.html', oyun=oyunlar)

if __name__ == '__main__':
    app.run(debug=True)

#220706048