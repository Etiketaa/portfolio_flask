from flask import Flask, render_template, request, jsonify
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv() # Carga las variables de entorno desde .env

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        if not name or not email or not message:
            return jsonify({'success': False, 'message': 'Datos inválidos.'}), 400

        # IMPORTANT: For Vercel deployment, use environment variables for security.
        # You should set these in your Vercel project settings.
        EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
        EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

        if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
            return jsonify({'success': False, 'message': 'Error de configuración del servidor.'}), 500

        msg = EmailMessage()
        msg['Subject'] = f'Nuevo mensaje de contacto de {name}'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = 'francoparedes1992@gmail.com'
        msg.set_content(f'Nombre: {name}\nEmail: {email}\n\nMensaje:\n{message}')

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                smtp.send_message(msg)
            return jsonify({'success': True, 'message': 'Mensaje enviado.'})
        except Exception as e:
            print(e)
            return jsonify({'success': False, 'message': 'Error al enviar el mensaje.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
