TIPOS_DE_CULTURA = ["Café", "Milho"]

CACHE_CULTURAS = []

def lista_culturas():
  return CACHE_CULTURAS

def encontra_cultura(identificador):
  try:
    return CACHE_CULTURAS[identificador]
  except IndexError:
    return None

def cria_cultura(cultura):
  CACHE_CULTURAS.append(cultura)

def atualiza_cultura(identificador, cultura):
  CACHE_CULTURAS[identificador] = cultura

def deleta_cultura(identificafor):
  try:
    return CACHE_CULTURAS.pop(identificafor)
  except IndexError:
    return None

def nova_cultuta(tipo_cultura, comprimento, largura):
  area_total = comprimento * largura

  ruas = 0
  # NPK é um tipo de insumo no qual a unidade que estamos utilizando
  # é kg/m2
  npk = 0
  
  if tipo_cultura == "Café":
    ruas = 0.9 # Número de ruas para plantio de café normalmente corresponde a 90% da área total
    npk = 0.015 # Para café a quantidade de NPK utilizado corresponse a 1.5% da área útil
  else:
    ruas = 0.95 # Número de ruas para plantio de milho normalmente corresponde a 95% da área total
    npk = 0.04 # Para ilho a quantidade de NPK utilizado corresponse a 4% da área útil
    
  area_util = area_total * ruas
  npk_necessario = area_util * npk

  return {
    "cultura": tipo_cultura,
    "comprimento": comprimento,
    "largura": largura,
    "area_total": area_total,
    "area_util": area_util,
    "npk": npk_necessario,
  }
