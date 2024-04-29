import requests
import qrcode
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    shortened_url = None
    qr_generated = False

    if request.method == 'POST':
        if 'long_url' in request.form:
            long_url = request.form['long_url']
            shortened_url = shorten_url(long_url)
        elif 'qr_url' in request.form:
            qr_url = request.form['qr_url']
            generate_qr(qr_url)
            qr_generated = True

    return render_template('index.html', shortened_url=shortened_url, qr_generated=qr_generated)

def shorten_url(long_url):
    access_token = '3fd003e2d3fedf632537bef5c7a66636a8abcc29'
    endpoint = 'https://api-ssl.bitly.com/v4/shorten'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }
    data = {
        'long_url': long_url,
        'domain': 'bit.ly'
    }
    response = requests.post(endpoint, json=data, headers=headers)
    if response.ok:
        return response.json()['link']
    else:
        return 'Failed to shorten URL'

def generate_qr(url):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save('static/qrcode.png')

@app.route('/qr')
def qr():
    return render_template('qr.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
