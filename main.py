import sys
import logging
import os
from datetime import datetime
from datetime import timedelta

from flashscore.coleta_tudo import executar_coleta
from db.utils import setup as setup_db
from db.utils import insert_row
from db.utils import count_date

script_dir = os.path.abspath(os.path.dirname( __file__ ))
logging.basicConfig(filename=script_dir + '/monkeybet.log',
  level=logging.INFO,
  format="%(asctime)s %(message)s")

def main():
  prox_data = datetime.now() + timedelta(1)
  prox_data = prox_data.strftime("%d/%m/%Y")

  cont = count_date(prox_data)

  if cont > 0:
    logging.info('Coleta para %s ja realizada' % prox_data)
    sys.exit()

  # vai macaco!!!!
  coleta = executar_coleta()

  # se voltou de maos vazias, cai fora
  if not coleta:
    logging.info('Nenhum jogo encontrado. Saindo....')
    sys.exit()

  for row in coleta:
    insert_row(row)

# LETS GO!!!

setup_db()

main()
