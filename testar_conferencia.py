# Lista de 15 números de um resultado real da Lotofácil
# (Exemplo: concurso 3110)
resultado_oficial = [1, 2, 4, 5, 8, 9, 10, 11, 13, 14, 18, 19, 21, 22, 23]
resultado_oficial.sort() # Organiza em ordem crescente

print("Procurando o resultado no arquivo...")

with open("todas_combinacoes.txt", "r") as f:
    for i, linha in enumerate(f, 1):
        # Transforma a linha do arquivo em lista de números
        jogo = sorted(list(map(int, linha.strip().split(','))))
        
        # Compara com o resultado oficial
        if jogo == resultado_oficial:
            print(f"ENCONTRADO! O sorteio está na linha {i} do seu arquivo.")
            break
    else:
        print("Resultado não encontrado (isso não deveria acontecer se o arquivo estiver completo).")