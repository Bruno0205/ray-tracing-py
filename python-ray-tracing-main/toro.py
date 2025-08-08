import math
import numpy as np
from entidades import Mesh
from vectors import Ponto

def toRadians(espacamento):
    """
    Transforma os valores que serão utilizados para a triangularização com base no espaçamento fornecido para radianos

    O espaçamento representa o espaçamento angular (em radianos) entre pontos consecutivos na superfície do toro
    Valores menores resultam em mais pontos e aumenta o detalhamento da malha

   """
    # Gera valores de 0 até 2pi + espacamento para cobrir toda a superfície
    valores = np.arange(0, 2 * math.pi + espacamento, espacamento)
    
    # Remove último valor se passar de 2pi
    if valores[-1] > 2 * math.pi:
        valores = valores[:-1]
    
    # inclui 2pi se não estiver
    if valores[-1] < 2 * math.pi:
        valores = np.append(valores, 2 * math.pi)
    
    return valores

class Toro:
    """
    Classe que representa um toro no espaço 3D
    
    O toro é definido por sua posição, dois raios e propriedades visuais
    
    A classe converte a representação discreta do toro em uma malha triangularizada
    """

    def __init__(self, centro_y, centro_z, R, r, cor):
        self.centro_y = centro_y
        self.centro_z = centro_z
        self.R = R # Raio Maior (> r)
        self.r = r # Raio Menor (> 0)
        self.cor = cor

    def point_on_surface(self, theta, alpha):
        """
        Calcula um ponto específico na superfície do toro com base em theta e alpha

        Com base na parametrização abaixo, converte theta e alpha em coordenadas 3D de um ponto na superfície

        x = (R + r * cos(theta)) * cos(alpha)
        y = r * sin(theta)
        z = (R + r * cos(theta)) * sin(alpha)

        Onde theta é o ângulo do "tubo", [0, 2pi] e alpha é o ângulo ao redor do eixo vertical, [0, 2pi]
        """ 
        x = (self.R + self.r * math.cos(theta)) * math.cos(alpha)
        y = self.r * math.sin(theta)
        z = (self.R + self.r * math.cos(theta)) * math.sin(alpha)
        
        return Ponto(x, y, z)
    
    def triangulate(self, espacamento):
        """ Triangulariza o objeto com base no espaçamento fornecido """
        pontos_superficie = [] # Lista dos pontos na superfície
        theta_values = toRadians(espacamento)
        alpha_values = toRadians(espacamento)

        # Gera todos os pontos da superfície em ordem
        for theta in theta_values:
            for alpha in alpha_values:
                ponto = self.point_on_surface(theta, alpha)
                pontos_superficie.append(ponto)

        triangulos = []

        # Número de divisões em theta por dimensão
        n = len(theta_values) - 1 
        """
        Geração dos triângulos:
        
        Cada divisão da grade se tornam dois triângulos
        Cada triângulo é formado por três pontos, então cada triângulo é representado por uma tupla de três índices
        O número de triângulos é n * n * 2
        
        (i,j+1) -------- (i+1,j+1)
           |  \             |
           |    \     T2    |
           |      \         |
           | T1     \       |
           |          \     |
        (i,j) -------- (i+1,j)
        """
        for i in range(n): 
            for j in range(n):
                triangulos.append((
                    i * (n + 1) + j,        # Ponto atual
                    (i + 1) * (n + 1) + j,  # Ponto de baixo
                    i * (n + 1) + j + 1     # Ponto da direita
                ))

                triangulos.append((
                    (i + 1) * (n + 1) + j,      # Ponto de baixo
                    (i + 1) * (n + 1) + j + 1,  # Ponto de baixo e a direita
                    i * (n + 1) + j + 1         # Ponto da direita
                ))

        lista_normais = []

        # Calcula as normais dos triângulos
        for triangulo in triangulos:
            # Calcula os 3 vértices do triângulo da iteração corrente 
            p0 = np.array([pontos_superficie[triangulo[0]].x, 
                           pontos_superficie[triangulo[0]].y, 
                           pontos_superficie[triangulo[0]].z])
            
            p1 = np.array([pontos_superficie[triangulo[1]].x, 
                           pontos_superficie[triangulo[1]].y, 
                           pontos_superficie[triangulo[1]].z])
            
            p2 = np.array([pontos_superficie[triangulo[2]].x, 
                           pontos_superficie[triangulo[2]].y, 
                           pontos_superficie[triangulo[2]].z])
            
            # Calcula a normal do triângulo da iteração corrente
            normal = np.cross(p1 - p0, p2 - p0)
            norma = np.linalg.norm(normal)
            normal = normal / norma
            
            lista_normais.append(normal.tolist())

        malha = Mesh(
            triangle_quantity=len(triangulos),
            vertices_quantity=len(pontos_superficie),
            vertices=pontos_superficie,
            triangle_tuple_vertices=triangulos,
            triangle_normals=lista_normais,
            vertex_normals=[],
            color=self.cor,
            k_ambiental=0.2,
            k_difuso=0.3,
            k_especular=0.8,
            n_rugosidade=100,
            k_reflexao=0.6,
            k_refracao=0,
            indice_refracao=0
        )
        
        return malha