import itertools

# Define os 25 números da Lotofácil
numeros = list(range(1, 26))
tamanho_aposta = 15

# Gera todas as combinações
combinacoes = itertools.combinations(numeros, tamanho_aposta)

# Abre o arquivo para escrita
with open("todas_combinacoes.txt", "w") as f:
    for combo in combinacoes:
        # Formata os números como uma linha de texto e escreve no arquivo
        linha = ",".join(map(str, combo))
        f.write(linha + "\n")

print("Arquivo 'todas_combinacoes.txt' gerado com sucesso!")