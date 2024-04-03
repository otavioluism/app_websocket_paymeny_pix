import uuid
import qrcode


class Pix(object): 

  def __init__(self):
    pass

  def create_payment(self) -> dict:
    #criando identificacao da Instituicao Financeira
    bank_payment_id = str(uuid.uuid4())

    # criando o conteudo do qrcode
    hash_payment = f'hash_payment_{bank_payment_id}'

    # gerando um qrcode com o conteudo passado
    img = qrcode.make(hash_payment)

    #salvando a imagem do qrcode na pasta...
    img.save(f'static/img/qr_code_payment_{bank_payment_id}.png')


    return {
      'bank_payment_id': bank_payment_id,
      'qr_code_path': f'qr_code_payment_{bank_payment_id}'
    } 

