import os
import csv
import numpy as np
from datetime import datetime
from flashscore.coleta_tudo import executar_coleta

def main():
  # montando o caminho do CSV gerado
  home_dir = os.path.expanduser('~')
  csv_path = home_dir + '/coleta'

  # arquivo CSV tem a data no nome
  data_exec = datetime.now().strftime("%Y%m%d")
  csv_name = 'coleta-' + data_exec + '.csv'

  csv_file = csv_path + '/' + csv_name

  # se existe CSV com a data atual, nao executa a coleta
  if os.path.isfile(csv_file):
    sys.exit('Coleta ' + csv_name + ' ja existe. Saindo....')

  # vai macaco!!!!
  coleta = executar_coleta()

  # se voltou de maos vazias, cai fora
  if not coleta:
    sys.exit('Nenhum jogo encontrado. Saindo....')

  # gera o CSV com os jogos encontrados
  np_array = np.asarray(coleta)

  with open(csv_path + '/' + csv_name, 'w') as f:
    csv_writer = csv.writer(f, delimiter=';')
    csv_writer.writerows(np_array)


# LETS GO!!!

main()
