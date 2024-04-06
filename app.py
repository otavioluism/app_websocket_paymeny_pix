from flask import Flask, jsonify, request, send_file, render_template
from flask_socketio import SocketIO
from repository.database import db
from db_models.payment import Payment
from datetime import datetime, timedelta
from payments.pix import Pix

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.py'
app.config['SECRET_KEY'] = 'SECRET_KEY_WEBSOCKET'

db.init_app(app)
socket_io = SocketIO(app)

# Rota para criar o pagamento
@app.route('/payments/pix', methods=['POST'])
def create_payment_pix(): 
  data = request.json

  if 'value' not in data: 
      return jsonify({'message': 'The request invalid!'}), 400

  expiration_date = datetime.now() + timedelta(minutes=30) # pega horario agora e soma 30 minutos
  payment = Payment(value=data.get('value'), expiration_date=expiration_date)

  pix_obj = Pix()
  data_payment_pix = pix_obj.create_payment()
  
  payment.bank_payment_id = data_payment_pix.get('bank_payment_id')
  payment.qr_code = data_payment_pix.get('qr_code_path')


  db.session.add(payment)
  db.session.commit()

  return jsonify({'message': 'The payment has been created', 'payment': payment.to_dict})

@app.route('/payments/pix/qr_code/<file_name>', methods=['GET'])
def get_image(file_name): 
  return send_file(f'static/img/{file_name}.png', mimetype='image/png')

# Rota para receber a confirmação do pagamento webHook a InstFina enviará para nós confirmação do pagamento 
@app.route('/payments/pix/confirmation', methods=['POST'])
def pix_confirmation(): 
  data = request.json

  if 'bank_payment_id' not in data and not 'value' not in data: 
     return jsonify({'message': 'The request is invalid!'}), 400
  
  payment = Payment.query.filter_by(bank_payment_id=data.get('bank_payment_id')).first()

  if not payment: 
     return jsonify({'message': 'The payment was not founded!'}), 404
    
  if data.get('value') != payment.value: 
     return jsonify({'message': 'The request is invalid!'}), 400
  
  payment.paid = True
  db.session.commit()
  socket_io.emit(f'payment-confirmed-{payment.id}')
  return jsonify({'message': 'The payment has been paid out'})

# Rota para criar a comunicação WebSocket
@app.route('/payments/pix/<int:payment_id>', methods=['GET'])
def payment_pix_page(payment_id): 
  payment = Payment().query.get(payment_id)

  if not payment: 
    return render_template('404.html')
  
  if payment.paid: 
     return render_template('confirmed_payment.html', 
                            payment_id=payment.id,
                            value=payment.value
                            )

  return render_template('payment.html', 
                         payment_id=payment.id, 
                         value=payment.value, 
                         host='http://127.0.0.1:5000', 
                         qr_code=payment.qr_code
                         )

# WEBSOCKET - lado do servidor criando um evento de recebimento do cliente (handshake)

@socket_io.on('connect')
def handle_message_connect():
    print('Cliente connected to the server!')


@socket_io.on('disconnect')
def handle_message_disconnect(): # esta funcao sera chamada quando na confirmacao do pagamento mudara a pagina, pois la não tem o script de socket
    print('Cliente disconnected to the server!')

if __name__ == '__main__': 
  socket_io.run(app, debug=True)