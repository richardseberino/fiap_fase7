import util
import questionary

def menu_principal():
  util.limpar_terminal()

  return questionary.select(
    "Escolha uma opção:",
    choices=[
      {"name": "1) Criar uma cultura", "value": 1},
      {"name": "2) Listar culturas", "value": 2},
      {"name": "3) Atualizar uma cultura", "value": 3},
      {"name": "4) Deletar uma cultura", "value": 4},
      {"name": "5) Sair", "value": 5},
    ]
  )

def menu_confirmacao_de_saida():
  util.limpar_terminal()

  return questionary.select(
    "Deseja realmente sair?",
    choices=[
      {"name": "1) Não", "value": False},
      {"name": "2) Sim", "value": True},
    ]
  )
