from flask import Flask, jsonify, request
from repository.database import db
from db_models.payment import Payment
from datetime import datetime, timedelta

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.py'
app.config['SECRET_KEY'] = 'SECRET_KEY_WEBSOCKET'

db.init_app(app)

# Rota para criar o pagamento
@app.route('/payments/pix', methods=['POST'])
def create_payment_pix(): 
  data = request.json

  if 'value' not in data: 
      return jsonify({'message': 'The request invalid!'}), 400

  expiration_date = datetime.now() + timedelta(minutes=30) # pega horario agora e soma 30 minutos
  payment = Payment(value=data.get('value'), expiration_date=expiration_date)


  db.session.add(payment)
  db.session.commit()

  return jsonify({'message': 'The payment has been created', 'payment': payment.to_dict})

# Rota para receber a confirmação do pagamento webHook a InstFina enviará para nós confirmação do pagamento 
@app.route('/payments/pix/confirmation', methods=['POST'])
def pix_confirmation(): 
  return jsonify({'message': 'The payment has been created'})

# Rota para criar a comunicação WebSocket
@app.route('/payments/pix/<int:payment_id>', methods=['GET'])
def payment_pix_page(): 
  return 'pagamento pix'

if __name__ == '__main__': 
  app.run(debug=True)