import sys 
sys.path.append('../') # fazendo com o que esta pasta tests tem acesso a todo src por isso voltar uma pasta

import pytest 
import os


from payments.pix import Pix

def test_create_payment_pix(): 
  pix = Pix()
  # passamos a base url para voltar a pasta e encontrar a static no source root
  create_payment_inst_fin = pix.create_payment(base_url='../')

  assert 'bank_payment_id' in create_payment_inst_fin
  assert 'qr_code_path' in create_payment_inst_fin

  qr_code_path = create_payment_inst_fin.get('qr_code_path')

  assert os.path.isfile(f'../static/img/{qr_code_path}.png')
 



