# 4 - Verificando Números Pares e Ímpares 
# Receba um número inteiro e diga se é par ou ímpar

numero = int(input("Digite um número inteiro: "))

if numero % 2 == 0:
    print(f"O número {numero} é PAR.")
else:
    print(f"O número {numero} é ÍMPAR.")
