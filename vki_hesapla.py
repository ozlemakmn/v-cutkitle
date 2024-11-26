from flask import Flask, request, render_template_string
from waitress import serve

app = Flask(__name__)

html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vücut Kitle İndeksi Hesaplayıcı</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; text-align: center; }
        input { padding: 10px; margin: 10px; font-size: 1em; }
        button { padding: 10px 20px; font-size: 1em; }
        .result { margin-top: 20px; font-size: 1.2em; color: #007BFF; }
    </style>
</head>
<body>
    <h1>Vücut Kitle İndeksi Hesaplayıcı</h1>
    <form method="POST">
        <input type="number" name="kilo" placeholder="Kilonuzu (kg) giriniz" step="0.1" required>
        <br>
        <input type="number" name="boy" placeholder="Boyunuzu (metre) giriniz" step="0.01" required>
        <br>
        <button type="submit">Hesapla</button>
    </form>
    {% if vki is not none %}
    <div class="result">
        <p>Vücut Kitle İndeksiniz: {{ vki }}</p>
        <p>Durum: {{ durum }}</p>
    </div>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def vki_hesapla():
    vki = None
    durum = None
    if request.method == "POST":
        try:
            kilo = float(request.form["kilo"])
            boy = float(request.form["boy"])
            if boy > 0 and kilo > 0:
                vki = round(kilo / (boy ** 2), 2)
                if vki < 13:
                    durum = "Zayıf"
                elif 14 <= vki < 18:
                    durum = "Normal"
                elif 18 <= vki < 30:
                    durum = "Fazla Kilolu"
                else:
                    durum = "Obez"
            else:
                durum = "Boy ve kilo pozitif olmalıdır."
        except ValueError:
            durum = "Lütfen geçerli değerler giriniz."
    return render_template_string(html, vki=vki, durum=durum)

if __name__ == "__main__":
    # Flask uygulamanızı Waitress ile çalıştırın
    serve(app, host='0.0.0.0', port=5000)
