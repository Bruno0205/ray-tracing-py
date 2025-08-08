import numpy as np
from entidades import Esfera, Plane, Mesh
from vectors import Ponto, Vetor
from fonte_de_luz import Luz
from ray import Ray

"""
Fórmula que queremos satisfazer:
I = Iluminação_Local + k_r * I_refletida + k_t * I_refratada
Onde Iluminação_Local = I_a * k_a + sum_lights( I_l * [ k_d * (N · L) + k_s * (R · V)^n ] )
"""

#vai servir p limitar um valor entre mínimo e máximo, como garantir que a luz não passe de 255 nem seja negativa
def clamp(minimum, x, maximum):
    return max(minimum, min(x, maximum))

def find_closest_intersection(
    ray, entidades, profundidade_reflexao, profundidade_refracao
):
    """
    Encontra a entidade mais próxima e o ponto de interseção com base no raio fornecido.
    """                                                           

    color = [0, 0, 0]                                            
    min_distance = float("inf")                                    

    for entidade in entidades:                                     
        intersection = entidade.__intersect_line__(                
            (ray.origin),                                          
            (ray.direction),                                      
        )                                                          
        if intersection:                                          
            distance_vetor = Vetor(intersection[0], intersection[1], intersection[2])     
            distance = ray.origin.__distance__(distance_vetor)     
            if distance < min_distance:                            
                min_distance = distance                            
                color = phong(                                     
                    entidade,                                      
                    [Luz(0, 5, 5, [255, 255, 255])],               
                    Ponto(intersection[0], intersection[1], intersection[2]), 
                    ray.origin,                                   
                    entidades,                                     
                    profundidade_reflexao,                         
                    profundidade_refracao,                         
                )                                                  
    return color                                                   

def refract(V, N, n_in, n_out):                    
    """                                            
    Calcula o vetor de refração usando a Lei de Snell.
    """                                            
    n = n_in / n_out                               
    cos_teta_1 = np.dot(N, -V)                     
    inner = 1 - n**2 * (1 - cos_teta_1**2)         
    if inner < 0:                                  
        # Reflexão total interna, não tem refração 
        return None                                
    cos_teta_2 = np.sqrt(inner)                    
    V_refratado = n * V + (n * cos_teta_1 - cos_teta_2) * N 
    if cos_teta_1 <= 0:                            
        V_refratado = n * V + (n * cos_teta_1 + cos_teta_2) * N 
    return V_refratado

#calcula a cor no ponto onde o raio bateu
def phong(entidade, luzes, ponto_intersec, camera_position, entidades, profundidade_reflexao=0, profundidade_refracao=0):

    Ia = np.array([50, 50, 50])  #intensidade da luz ambiente (claridade) -> I_a na fórmula

    #vetor da superfície até a câmera (de onde estamos olhando)
    V = np.array([
        camera_position.x - ponto_intersec.x,
        camera_position.y - ponto_intersec.y,
        camera_position.z - ponto_intersec.z,
    ])
    V = V / np.linalg.norm(V)  #normaliza V

    #Agora precisamos do vetor normal N no ponto onde o raio bateu
    N = None

    if isinstance(entidade, Esfera):
        #P/ uma esfera, a normal é radial (vai do centro -> ponto de intersecção)
        N = np.array([
            ponto_intersec.x - entidade.center.x,
            ponto_intersec.y - entidade.center.y,
            ponto_intersec.z - entidade.center.z,
        ])

    elif isinstance(entidade, Plane):
        #P/ 1 plano, a normal é constante
        N = np.array([
            entidade.normal.x,
            entidade.normal.y,
            entidade.normal.z,
        ])

    elif isinstance(entidade, Mesh):
        #P/ uma malaha, pode ter uma normal calculada no ponto
        N = np.array([
            ponto_intersec.x,
            ponto_intersec.y,
            ponto_intersec.z,
        ])

    #vemos se tem normal e normalizamos (sempre queremos vetores unitários)
    if N is not None and np.linalg.norm(N) != 0:
        N = N / np.linalg.norm(N)

    #iluminação começa zerada (isso será o somatório la que chamamos de sum_lights)
    i_sum = np.array([0.0, 0.0, 0.0])
    entidade.color = np.array(entidade.color)

    #para cada luz no cenário vamos somar sua contribuição
    for luz in luzes:
        luz.I = np.array(luz.I)  # I_l na fórmula (intensidade da luz pontual)

        #vetor da superfície até a luz
        L = np.array([
            luz.x - ponto_intersec.x,
            luz.y - ponto_intersec.y,
            luz.z - ponto_intersec.z,
        ])
        L = L / np.linalg.norm(L)  # normaliza L

        # R = vetor de reflexão (espelho)
        R = 2 * N * (N.dot(L)) - L

        # N.L mede o quão de frente está para a luz
        N_dot_L = clamp(0, N.dot(L), 1) #(N · L) faz parte da difusa

        # R.V mede o brilho espelhado na direção da câmera
        R_dot_V = clamp(0, R.dot(V), 1) # (R · V) faz parte da especular

        #-----Componente difusa-----
        # I_difusa = I_l * k_d * (N · L)
        I_difusa = luz.I * entidade.color * entidade.k_difuso * N_dot_L

        #-----Componente especular-----
        # I_especular = I_l * k_s * (R · V)^n
        I_especular = luz.I * entidade.k_especular * (R_dot_V**entidade.n_rugosidade)

        #Soma essas contribuições para essa luz
        i_sum += I_difusa + I_especular # sum_lights

    #Agora somamos a luz ambiente (independe de luzes pontuais)
    # I_a * k_a (luz ambiente)
    cor = (Ia * entidade.k_ambiental) + i_sum

    if profundidade_reflexao >= 3 and profundidade_refracao >= 3:
        return [51, 51, 51]

    # Adicionar reflexão recursiva
    if profundidade_reflexao < 3 and entidade.k_reflexao > 0: # Adicionado 'and entidade.k_reflexao > 0' para otimização
        N_dot_V = N.dot(V)
        refletido_direcao = 2 * N * (N_dot_V) - V
        refletido_direcao = refletido_direcao / np.linalg.norm(refletido_direcao)

        # A origem do raio refletido precisa ser um pouco deslocada para fora da superfície
        # para evitar que ele atinja o próprio objeto que o refletiu.
        epsilon = 0.0001
        offset_normal = N * epsilon

        # Criamos um novo Ponto de origem, já com o deslocamento
        origem_com_offset = Ponto(ponto_intersec.x + offset_normal[0],
                                ponto_intersec.y + offset_normal[1],
                                ponto_intersec.z + offset_normal[2])

        raio_refletido = Ray(
            origem_com_offset, # Usamos a nova origem deslocada
            Vetor(refletido_direcao[0], refletido_direcao[1], refletido_direcao[2]),
        )
        cor_refletida = find_closest_intersection(
            raio_refletido,
            entidades,
            profundidade_reflexao=profundidade_reflexao + 1,
            profundidade_refracao=profundidade_refracao,
        )
        if cor_refletida: # Checa se a cor refletida não é nula
            Ir = np.array(cor_refletida)
            cor = cor + entidade.k_reflexao * Ir

    #Refração recursiva
    if profundidade_refracao < 3:                                
        if entidade.indice_refracao != 0:                        
            if isinstance(entidade, Esfera):                     
                V_dot_N = np.dot(V, N)                           
                if V_dot_N <= 0:                                 
                    N = N * -1                                   
                    V_dot_N = np.dot(V, N)                       
                if np.dot(V, N) > 0:                             
                    refracao_direcao = refract(                  
                        V, N * -1, n_in=entidade.indice_refracao, n_out=1.0  
                    )                                            
                else:                                            
                    refracao_direcao = refract(                  
                        V, N, n_in=1.0, n_out=entidade.indice_refracao       
                    )                                            
            else:                                                
                refracao_direcao = refract(                      
                    V, N, n_in=1.0, n_out=entidade.indice_refracao          
                )                                                
            if refracao_direcao is not None:                     
                refracao_direcao = refracao_direcao / np.linalg.norm(refracao_direcao) 
                #refracao_origem = ponto_intersec                 
                refracao_origem = Ponto(
                    ponto_intersec.x + N[0] * 1e-4,
                    ponto_intersec.y + N[1] * 1e-4,
                    ponto_intersec.z + N[2] * 1e-4
                )

                raio_refratado = Ray(                            
                    Ponto(refracao_origem.x, refracao_origem.y, refracao_origem.z),    
                    Vetor(                                       
                        refracao_direcao[0], refracao_direcao[1], refracao_direcao[2]  
                    ),                                           
                )                                                
                cor_refratada = find_closest_intersection(       
                    raio_refratado,                              
                    entidades,                                   
                    profundidade_refracao=profundidade_refracao + 1, 
                    profundidade_reflexao=profundidade_reflexao,     
                )                                                
                It = np.array(cor_refratada)                     
                cor = cor + entidade.k_refracao * It   

    cor_final = [min(255, max(0, int(i))) for i in cor] #garantia que cada canal RGB fique entre 0 e 255 (sem estouro)

    return cor_final
