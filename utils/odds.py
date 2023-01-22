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

def favoritismo(odd1, oddx, odd2):
  palpite = "sem palpite"

  if odd1 <= 1.50 or odd2 <= 1.50:
    palpite = "muito favorito"
  elif odd1 > 1.50 or odd2 > 1.50:
    palpite = "favorito"

  return palpite

def palpite(odd1, oddx, odd2):
  if bom_empate(odd1, oddx, odd2):
    return "empate"
  else:
    return favoritismo(odd1, oddx, odd2)

def dupla_hipotese(odd1, odd2):
  if odd1 <= odd2:
    return "1X"
  else:
    return "X2"

