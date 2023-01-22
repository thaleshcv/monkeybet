import os
import csv
import numpy as np
from datetime import datetime
from flashscore.coleta_tudo import executar_coleta

def main():
  coleta = executar_coleta()
  np_array = np.asarray(coleta)

  home_dir = os.path.expanduser('~')
  csv_path = home_dir + '/coleta'

  data_exec = datetime.now().strftime("%Y%m%d")
  csv_name = 'coleta-' + data_exec + '.csv'

  csv_file = csv_path + '/' + csv_name

  if os.path.isfile(csv_file):
    sys.exit('Coleta ' + csv_name + ' ja existe. Saindo....')

  with open(csv_path + '/' + csv_name, 'w') as f:
    csv_writer = csv.writer(f, delimiter=';')
    csv_writer.writerows(np_array)


# LETS GO!!!

main()
