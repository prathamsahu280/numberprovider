from flask import Flask, request, render_template
import requests
import os

app = Flask(__name__)

def get_operator_circle(number):
    url = f"https://digitalapiproxy.paytm.com/v1/mobile/getopcirclebyrange?number={number}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.text}")
        if response.headers.get('Content-Type') == 'application/json':
            data = response.json()
            if 'Operator' in data and 'Circle' in data:
                return data['Operator'], data['Circle']
        return None, None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None, None
    except ValueError as e:
        print(f"JSON decoding failed: {e}")
        return None, None


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        numbers = request.form['numbers']
        numbers = [num.strip() for num in numbers.replace('\r', '').split('\n') if num.strip()]
        results = []
        for number in numbers:
            operator, circle = get_operator_circle(number)
            results.append({'number': number, 'operator': operator, 'circle': circle})
        return render_template('index.html', results=results)
    return render_template('index.html', results=[])

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
