from flask import Flask, jsonify

app = Flask(__name__)

# Rota para criar o pagamento
@app.route('/payments/pix', methods=['POST'])
def create_payment_pix(): 
  return jsonify({'message': 'The payment has been created'})

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