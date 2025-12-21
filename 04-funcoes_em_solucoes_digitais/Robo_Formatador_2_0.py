def formatar_mensagem(texto):
    """
    Padroniza uma mensagem removendo espaços extras, 
    convertendo para minúsculas e garantindo apenas um espaço entre palavras.
    
    Args:
        texto (str): Mensagem original enviada ao robô
        
    Returns:
        str: Mensagem formatada conforme as regras do desafio
    """
    # Remove espaços no início e no fim
    texto = texto.strip()
    
    # Se após o strip a string ficou vazia (ou só tinha espaços), retorna vazio
    if not texto:
        return ""
    
    # Converte tudo para minúsculas
    texto = texto.lower()
    
    # Separa a string em palavras (split remove espaços extras automaticamente)
    palavras = texto.split()
    
    # Junta as palavras com exatamente um espaço entre elas
    mensagem_formatada = " ".join(palavras)
    
    return mensagem_formatada


# Lê a entrada do usuário
entrada = input()

# Processa e exibe a mensagem formatada
saida = formatar_mensagem(entrada)
print(saida)
