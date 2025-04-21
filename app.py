from flask import Flask, render_template, request, session
import random

app = Flask(__name__)
app.secret_key = 'kunci_rahasia'

CLUE_THRESHOLD = 3  # Berikan clue setelah 3 tebakan salah

@app.route('/', methods=['GET', 'POST'])
def tebak_angka():
    if 'angka_rahasia' not in session:
        session['angka_rahasia'] = random.randint(1, 100)
        session['jumlah_tebakan'] = 0
        pesan = "Saya telah memilih sebuah angka antara 1 dan 100. Coba tebak!"
        indikator = ""
        clue = ""
    else:
        tebakan = request.form.get('tebakan', type=int)
        if tebakan is not None:
            session['jumlah_tebakan'] += 1
            if tebakan < session['angka_rahasia']:
                pesan = "Terlalu rendah! Coba lagi."
                indikator = "↓"
            elif tebakan > session['angka_rahasia']:
                pesan = "Terlalu tinggi! Coba lagi."
                indikator = "↑"
            else:
                pesan = f"Selamat! Anda benar dalam {session['jumlah_tebakan']} tebakan. Angka rahasianya adalah {session['angka_rahasia']}."
                indikator = "BENAR!"
                clue = ""
                del session['angka_rahasia']
            
            # Berikan clue setelah CLUE_THRESHOLD tebakan salah
            if 'angka_rahasia' in session and session['jumlah_tebakan'] >= CLUE_THRESHOLD and session['jumlah_tebakan'] % CLUE_THRESHOLD == 0:
                if session['angka_rahasia'] % 2 == 0:
                    clue = "Clue: Angka rahasia adalah bilangan genap."
                else:
                    clue = "Clue: Angka rahasia adalah bilangan ganjil."
            else:
                clue = ""
        else:
            pesan = "Masukkan tebakan Anda."
            indikator = ""
            clue = ""

    return render_template('tebak_angka.html', pesan=pesan, jumlah_tebakan=session.get('jumlah_tebakan', 0), indikator=indikator, clue=clue)

@app.route('/reset')
def reset_game():
    session.pop('angka_rahasia', None)
    session.pop('jumlah_tebakan', None)
    return redirect('/')

if __name__ == '__main__':
    from flask import redirect
    app.run(debug=True)