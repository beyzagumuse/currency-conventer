from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def get_exchange_rate():
    try:
        # Anahtarsız çalışan API
        response = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
        data = response.json()
        return data['rates']['TRY']
    except Exception as e:
        print("Kur alınamadı:", e)
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    if request.method == 'POST':
        try:
            usd_amount = float(request.form['usd'])
            rate = get_exchange_rate()
            if rate:
                result = round(usd_amount * rate, 2)
            else:
                error = "Kur bilgisi alınamadı."
        except Exception as e:
            error = f"Hata: {e}"
    return render_template('index.html', result=result, error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
