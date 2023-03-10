import time
import sys
import logging
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from datetime import timedelta

from utils.odds import dupla_hipotese
from utils.odds import palpite

def init_driver():
  options = Options()
  options.headless = True
  options.add_argument("--start-maximized")
  options.add_argument("--disable-infobars")
  options.add_argument("--disable-extensions")
  options.add_argument("--no-sandbox")
  options.add_argument("--disable-application-cache")
  options.add_argument("--disable-gpu")
  options.add_argument("--disable-dev-shm-usage")

  return webdriver.Firefox(options=options)

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

  logging.info("Lançando FlashScore....")
  driver.get("https://www.flashscore.com/")
  driver.maximize_window
  driver.set_window_position(0,-2000)

  wait = WebDriverWait(driver, 100)

  try:
    logging.info("Esperando aba odds...")
    aba_odds = wait.until(
      EC.element_to_be_clickable((By.XPATH, "//div[@class='tabs__text tabs__text--default'] | //div[text()='Odds']"))
    )

    aba_odds.click()

    logging.info("Esperando jogos do dia seguinte...")
    next_day = wait.until(
      EC.element_to_be_clickable((By.XPATH, "//button[@class='calendar__navigation calendar__navigation--tomorrow']"))                                                              
    )

    next_day.click()

    logging.info("Esperando Jogos...")
    time.sleep(5)
    
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

        casa = game.find_element(By.CLASS_NAME, "event__participant--home")
        casa = casa.text

        visitante = game.find_element(By.CLASS_NAME, "event__participant--away")
        visitante = visitante.text

        horario = game.find_element(By.CLASS_NAME, "event__time")
        horario = horario.text

        odd1 = game.find_element(By.CLASS_NAME, "event__odd--odd1")
        odd1 = odd1.text

        oddx = game.find_element(By.CLASS_NAME, "event__odd--odd2")
        oddx = oddx.text

        odd2 = game.find_element(By.CLASS_NAME, "event__odd--odd3")
        odd2 = odd2.text

        if odd1 != "-":
          banca = game.find_element(By.CLASS_NAME, "event__odd--odd1")
          banca = banca.get_attribute("data-bookmaker-id")
          banca = nome_banca(banca)

          odd1 = float(odd1)
          oddx = float(oddx)
          odd2 = float(odd2)

          row.append(horario[0:5])
          row.append(casa + " x " + visitante)
          row.append(banca)
          row.append(odd1)
          row.append(oddx)
          row.append(odd2)
          row.append(palpite(odd1, oddx, odd2))
          row.append(dupla_hipotese(odd1, odd2))

          records.append(row)
        time.sleep(1)
      except Exception as err:
        if casa is not None and visitante is not None:
          logging.info("Erro coletando jogo " + casa + ' x ' + visitante)
        else:
          logging.info("Erro coletando jogo " + game.get_attribute('id'))
        
        logging.info(err)

    return records
  finally:
    driver.quit()

