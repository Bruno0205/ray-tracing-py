"""Módulo que contém a classe FonteDeLuz."""

class Luz:
    """"Classe que representa uma fonte de luz no espaço 
    
    - Cada luz é um ponto, que determina sua localização --->  l(x, y, z) onde,x, y e z e R.
    - A Intensidade da luz é representada um vetor, que representa a cor RGB 
    """
    def __init__(self, x, y, z, I):
        self.x = x # Coordenada x da posição da luz
        self.y = y # Coordenada y da posição da luz
        self.z = z # Coordenada z da posição da luz
        self.I = I # Intensidade da luz
    #Exemplo: Luz(2, 1, 0, [153, 153, 153]) cria uma luz em (2, 1, 0) com intensidade cinza