import util
import sys
import questionary
import culturas
import data_source

# Constantes usadas para executar operações via código
# Onde não existe iteração do usuário
SAIR = 5
CARREGAR_CULTURAS = 6
LIMPAR_TERMINAL = -1

# Simula a camada de controle da aplicação (C do padrão de arquitetura MVC)
def executar(opcao_selecionada):
  match opcao_selecionada:
    case 1:
      __executar_acao("Criando nova cultura", __criar_cultura)
    case 2:
      __executar_acao("Listando culturas", __listar_culturas)
    case 3:
      __executar_acao("Atualizando cultura", __atualizar_cultura)
    case 4:
      __executar_acao("Deletando cultura", __deletar_cultura)
    case 5:
      __executar_acao("Saindo da aplicação...", __sair)
    case 6:
      data_source.carrega_dados_para_cache(culturas.CACHE_CULTURAS)
    case _:
      util.limpar_terminal()

def __executar_acao(titulo, acao):
  util.limpar_terminal()

  linha = "*" * (len(titulo) + 6) 
  print(linha)
  print(f"** {titulo} **")
  print(linha)

  print()
  acao()
  print()
  
  input("Pressione qualquer tecla para voltar ")
  util.limpar_terminal()

def __criar_cultura():
  nova_cultura = __formulario_cultura()
  culturas.cria_cultura(nova_cultura)
  
  print("Cultura criada com sucesso\n")

def __atualizar_cultura():
  __listar_culturas()

  indice_cultura = __safe_int_input("\nInforme a linha que você quer atualizar: ")
  indice_cultura = indice_cultura - 1

  if culturas.encontra_cultura(indice_cultura):
    nova_cultura = __formulario_cultura()
    culturas.atualiza_cultura(indice_cultura, nova_cultura)
    print("Cultura atualizada com sucesso")
  else:
    print("Linha inválida")

  print()

def __formulario_cultura():
  tipo_cultura = questionary.select(
    "Escolha o tipo de cultura:",
    choices=culturas.TIPOS_DE_CULTURA
  ).ask()

  comprimento = __safe_int_input("\nInforme a comprimento da área de plantio em metros: ")
  largura = __safe_int_input("\nInforme a largura da área de plantio em metros: ")

  print()
  
  return culturas.nova_cultuta(tipo_cultura, comprimento, largura)

def __listar_culturas():
  header = f"| {"ID".ljust(4)} | Cultura | Comprimento | Largura | Área total | Área util | {"NPK kg/m2".ljust(10)} |"

  line = '-' * len(header)
  print(line)
  print(header)
  print(line)

  for index, plantio in enumerate(culturas.lista_culturas()):
    id = f"{str(index + 1)}"
    cultura = plantio["cultura"]
    comprimento = str(plantio["comprimento"])
    largura = str(plantio["largura"])
    area_total = format(plantio["area_total"], ".2f")
    area_util = format(plantio["area_util"], ".2f")
    npk = format(plantio["npk"], ".2f")

    print(f"| {id.ljust(4)} | {cultura.ljust(7)} | {comprimento.ljust(11)} | {largura.ljust(7)} | {area_total.ljust(10)} | {area_util.ljust(9)} | {npk.ljust(10)} |")
    print(line)

def __deletar_cultura():
  __listar_culturas()

  indice_linha = __safe_int_input("\nInforme a linha que você quer excluir: ")

  if culturas.deleta_cultura(indice_linha-1):
    print("Cultura removida com sucesso")
  else:
    print("Linha inválida")

  print() 

def __safe_int_input(texto):
  valor = 0
  while valor < 1:
    try:
      valor = int(input(texto))
    except ValueError:
      print("Valor informado não é um número.\n")

  return valor

def __sair():
  # Atualiza o CSV ao sair do programa
  data_source.salva_dados_do_cache(culturas.CACHE_CULTURAS)
  sys.exit("Até logo ✌\n")
