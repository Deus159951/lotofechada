def conferir_completo(arquivo):
    entrada = input("Digite os 15 números sorteados, separados por vírgula: ")
    try:
        sorteio_set = set(map(int, entrada.split(',')))
    except ValueError:
        print("Erro: Digite apenas números separados por vírgula.")
        return

    print("Aguarde, processando e localizando as linhas...")
    
    contador_14 = 0
    contador_15 = 0
    
    with open(arquivo, 'r') as f:
        # O enumerate começa do 1 para indicar a linha correta
        for numero_linha, linha in enumerate(f, 1):
            try:
                numeros_linha = set(map(int, linha.strip().split(',')))
                acertos = len(sorteio_set.intersection(numeros_linha))
                
                if acertos == 15:
                    contador_15 += 1
                    print(f"[PREMIO MÁXIMO] 15 ACERTOS encontrados na LINHA: {numero_linha}")
                elif acertos == 14:
                    contador_14 += 1
                    print(f"[PREMIO] 14 ACERTOS encontrados na LINHA: {numero_linha}")
            except ValueError:
                continue
    
    print("-" * 30)
    print(f"RESUMO FINAL")
    print(f"Total de acertos com 15 pontos: {contador_15}")
    print(f"Total de acertos com 14 pontos: {contador_14}")
    print("-" * 30)

conferir_completo('todas_combinacoes.txt')