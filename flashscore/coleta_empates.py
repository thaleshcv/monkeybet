from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from datetime import timedelta
import time

def init_driver():
  options = Options()
  options.headless = True
  return webdriver.Firefox(options=options)

def bom_empate(odd1, oddx, odd2):
  maior = 0
  menor = 0

  if odd1 > odd2:
    maior = odd1
    menor = odd2
  else:
    maior = odd2
    menor = odd1

  diff = maior - menor

  if odd1 > 3.0 or odd2 > 3.0:
    return False
  elif oddx >= 3.2 or oddx < 2.5:
    return False
  elif diff >= 0.3:
    return False
  
  return True

def dupla_hipotese(odd1, odd2):
  if odd1 <= odd2:
    return "1X"
  else:
    return "X2"

def nome_banca(banca):
  if banca == "5":
    return "UNIBET"
  elif banca == "16":
    return "BET365"
  elif banca == "417":
    return "1XBET"
  else:
    return banca

def executar_coleta():
  driver = init_driver()

  print("Lançando FlashScore....")
  driver.get("https://www.flashscore.com/")
  driver.maximize_window
  driver.set_window_position(0,-2000)

  wait = WebDriverWait(driver, 100)
  
  try:
    print("Esperando aba Odds...")
    aba_odds = wait.until(
      EC.element_to_be_clickable((By.XPATH, "//div[@class='tabs__text tabs__text--default'] | //div[text()='Odds']"))
    )

    aba_odds.click()

    print("Esperando Dia Seguinte...")
    next_day = wait.until(
      EC.element_to_be_clickable((By.XPATH, "//button[@class='calendar__navigation calendar__navigation--tomorrow']"))
    )

    next_day.click()

    print("Esperando Jogos...")
    time.sleep(10)
    
    wait.until(
      EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='sportName soccer']"))
    )

    tabela_jogos = driver.find_element(By.XPATH, "//div[@class='sportName soccer']")
    jogos = tabela_jogos.find_elements(By.XPATH, "//div[contains(@class,'event__match ')]")

    records = []

    data_jogo = datetime.now() + timedelta(1)
    data_jogo = data_jogo.strftime("%d/%m/%Y")

    for game in jogos:
      try:
        row = [data_jogo]

        horario = game.find_element(By.CLASS_NAME, "event__time")
        horario = horario.text

        casa = game.find_element(By.CLASS_NAME, "event__participant--home")
        casa = casa.text

        visitante = game.find_element(By.CLASS_NAME, "event__participant--away")
        visitante = visitante.text

        odd1 = game.find_element(By.CLASS_NAME, "event__odd--odd1")
        odd1 = odd1.text

        oddx = game.find_element(By.CLASS_NAME, "event__odd--odd2")
        oddx = oddx.text

        odd2 = game.find_element(By.CLASS_NAME, "event__odd--odd3")
        odd2 = odd2.text

        if odd1 != "-":
          odd1 = float(odd1)
          oddx = float(oddx)
          odd2 = float(odd2)

          if bom_empate(odd1, oddx, odd2):
            banca = game.find_element(By.CLASS_NAME, "event__odd--odd1")
            banca = banca.get_attribute("data-bookmaker-id")

            row.append(horario[0:5])
            row.append(casa + " x " + visitante)
            row.append(odd1)
            row.append(oddx)
            row.append(odd2)
            row.append(nome_banca(banca))
            row.append(dupla_hipotese(odd1, odd2))

            records.append(row)
      except:
        print("Erro coletando jogo " + game.get_attribute("id"))

    return records
  finally:
    driver.quit()
