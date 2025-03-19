from flask import Flask, render_template, request
import segno
import io
import base64

app = Flask(__name__, template_folder="templates")

@app.route('/')
def home():
    return render_template('index.html', image=None)

@app.route('/form-handler', methods=['POST'])
def generate_QR():
    qr_code_data = None
    input_text = None
    
    if request.method == 'POST':
        buffer = io.BytesIO()
        input_text = request.form['data']

        qr = segno.make_qr(input_text)
        qr.save(buffer, kind='png', scale=10, dark='purple', border=5)
        buffer.seek(0)
        qr_code_data = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return render_template('index.html', image=qr_code_data, input_text=input_text)

if __name__ == '__main__':
    app.run(debug=True)
