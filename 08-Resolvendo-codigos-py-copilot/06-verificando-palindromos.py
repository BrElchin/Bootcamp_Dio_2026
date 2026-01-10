# 6 - Verificando Palíndromos 
# Teste se uma palavra é palíndromo (lê igual de trás para frente)

palavra = input("Digite uma palavra: ").strip().lower()

if palavra == palavra[::-1]:
    print(f"A palavra '{palavra}' é um PALÍNDROMO!")
else:
    print(f"A palavra '{palavra}' NÃO é palíndromo.")
