def calcular_regressao_linear(x: list, y: list):
    if len(x) != len(y) or len(x) == 0:
        raise ValueError("Listas de entrada inválidas.")
    
    n = len(x)
    media_x = sum(x) / n
    media_y = sum(y) / n
    
    numerador = sum((x[i] - media_x) * (y[i] - media_y) for i in range(n))
    denominador = sum((x[i] - media_x) ** 2 for i in range(n))
    
    if denominador == 0:
        raise ValueError("Erro: Dados sem variação em X (impossível ajustar reta).")
        
    a = numerador / denominador
    b = media_y - a * media_x
    return a, b

def prever_energia(x_val: float, a: float, b: float) -> float:
    return a * x_val + b