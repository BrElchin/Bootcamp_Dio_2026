def identificar_categoria_gadget(codigo):
    """
    Recebe uma string 'codigo' e retorna a categoria associada:
    - 'T': tablet
    - 'P': phone
    - 'N': notebook
    Se não corresponder, retorna 'unknown'.
    
    Args:
        codigo (str): Código do gadget (não vazio, sem espaços)
    
    Returns:
        str: Categoria do gadget: 'tablet', 'phone', 'notebook' ou 'unknown'
    """
    # Verifica se o código está vazio (proteção extra)
    if not codigo:
        return "unknown"
    
    # Pega apenas a primeira letra e converte para maiúscula (para evitar erro de case)
    primeira_letra = codigo[0].upper()
    
    # Mapeamento da categoria com base na primeira letra
    if primeira_letra == "T":
        return "tablet"
    elif primeira_letra == "P":
        return "phone"
    elif primeira_letra == "N":
        return "notebook"
    else:
        return "unknown"


# Leitura da entrada (remove possíveis espaços com strip)
codigo_gadget = input().strip()

# Chamada da função e exibição do resultado
categoria = identificar_categoria_gadget(codigo_gadget)
print(categoria)
