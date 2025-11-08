import menus
import operacoes

def main():
  # Carrega culturas cadastradas em arquivo CSV
  operacoes.executar(operacoes.CARREGAR_CULTURAS)

  # Inicializa o menu principal
  menu = menus.menu_principal()
  
  # Loop para menu iterativo com opção de interrupção para sair do programa
  # Ao sair um menu de confirmação é exibido para caso o usuário deseje
  # desfazer a ação
  while True:
    try:
      opcao_selecionada = menu.unsafe_ask()
      operacoes.executar(opcao_selecionada)
    except KeyboardInterrupt:
      opcao_selecionada = menus.menu_confirmacao_de_saida().ask()

      if opcao_selecionada:
        operacoes.executar(operacoes.SAIR)
      else:
        operacoes.executar(operacoes.LIMPAR_TERMINAL)
        continue
       
if __name__ == "__main__":
  main()
