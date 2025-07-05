from vectors import Ponto, Vetor
from entidades import Esfera, Mesh, Plane
from camera import Camera
from ray_casting import RayCasting
from transformation import Transformacao


def main():

    ray_casting = RayCasting(hres=500, vres=500)
    
    plano = Plane(
         point=Ponto(0, 3, 0),
         normal=Vetor(0, 1, 0),
         color=(255, 0, 0),
     )

    esfera = Esfera(
        center=Ponto(2, 0, 0),
        radius=4,
        color=(0, 128, 0),
    )

    """
    p0 = Ponto(5, 0, 0) #A
    p1 = Ponto(0, 5, 0) #B
    p2 = Ponto(-5, 0, 0) #C
    p3 = Ponto(0, -5, 0) #D
    p4 = Ponto(0, 0, 5) #E

    v1 = p1.__sub__(p0) #B-A
    v2 = p4.__sub__(p0) #E-A
    normal1 = v1.__cross__(v2).__normalize__()

    v3 = p2.__sub__(p1)  #C-B
    v4 = p4.__sub__(p1) #E-B
    normal2 = v3.__cross__(v4).__normalize__()

    v5 = p3.__sub__(p2) #D-C
    v6 = p4.__sub__(p2) #E-C
    normal3 = v5.__cross__(v6).__normalize__()

    v7 = p0.__sub__(p3) #A-D
    v8 = p4.__sub__(p3) #E-D
    normal4 = v7.__cross__(v8).__normalize__()

    mesh = Mesh(
        triangle_quantity=4,
        vertices_quantity=5,
        vertices=[p0, p1, p2, p3, p4],
        triangle_normals=[normal1, normal2, normal3, normal4],
        color=(0, 25, 0),
        triangle_tuple_vertices=[(0, 1, 4), (1, 2, 4), (2, 3, 4), (0, 3, 4)], #Basicamente (A,B,E) (B,C,E) (C,D,E) (A,D,E)
        vertex_normals=[],
    )
    """
    #"""
    p0a = Ponto(2, 0, 0)
    p1a = Ponto(-2, 2, 0)
    p2a = Ponto(-2, -2, 0)


    v1a = p1a.__sub__(p0a)
    v2a = p2a.__sub__(p0a)
    normala = v1a.__cross__(v2a).__normalize__()

    mesh = Mesh(
        triangle_quantity=1,
        vertices_quantity=3,
        vertices=[p0a, p1a, p2a],
        triangle_normals=[normala],
        color=(0, 255, 255),
        triangle_tuple_vertices=[(0, 1, 2)],
        vertex_normals=[],
    )
    #"""
    #esfera = Transformacao.translate_sphere(esfera, 10, 0, 0)

    camera = Camera(
        target=Ponto(0, 0, 0),
        #position=Ponto(0, 0, 10), #Camera 1
        position=Ponto(0, 10, 2), #Camera 3
        up=Vetor(0, -1, 0)
    )

    entidades = [mesh]

    ray_casting.__generate_image__(entidades, 1, camera)

'''
    
    # Criando a matriz de rotação (45 graus em torno do eixo Y)
    # O ângulo deve ser em radianos
    angulo_rad = math.radians(30)
    matriz_rotacao = Transformacao.criar_matriz_rotacao_x(angulo_rad)
    
    # Criando a matriz de translação (mover 3 unidades para a direita)
    #matriz_translacao = Transformacao.criar_matriz_translacao(3, 0, 0)

    # Combinando as transformações: Rotação primeiro, depois Translação.
    # A ordem da multiplicação é importante: a transformação à direita é aplicada primeiro.
    #matriz_combinada = matriz_translacao @ matriz_rotacao

    # Aplicando a matriz combinada ao nosso objeto Mesh
    mesh_transformada = Transformacao.aplicar_transformacao_malha(mesh, matriz_rotacao)

    # --- 4. RENDERIZAÇÃO DA IMAGEM "DEPOIS" ---
    
    print("--- Renderizando a cena TRANSFORMADA. ---")
    ray_casting_depois = RayCasting(hres=400, vres=400)
    entidades_depois = [mesh_transformada]
    
    camera = Camera(
        target=Ponto(0, 0, 0),
        #position=Ponto(15, -3, 10), #Camera 1
        position=Ponto(0, 10, 5), #Camera 3
        up=Vetor(0, -1, 0)
    )
    
    ray_casting_depois.__generate_image__(entidades_depois, 1, camera)
    #'''
main()





""" 
#Entrega 1 - Interseção plano/esfera

    camera = Camera(
        target=Ponto(5, 0, 0),
        position=Ponto(0, 5, 0),
        up=Vetor(0, 1, 0),
        hres=300,
        vres=300
    )

    #normal_plano = (Ponto(4, 0, 0) - camera.position).__normalize__()
    normal_plano = Vetor(0, 1, 0)

    #point_plano = Ponto(7, 0, 0)
    point_plano = Ponto(0, 0, 0)

    plano = Plane(
        point=point_plano,
        normal=normal_plano,
        color=(255, 0, 0),
    )

    esfera = Esfera(center=Ponto(4, 0, 0), radius=1, color=(0, 0, 100))
    esfera2 = Esfera(center=Ponto(6, 0, 0), radius=1, color=(0, 200, 0))

    entidades = [esfera, esfera2, plano]

    raycaster = RayCasting(hres=camera.hres, vres=camera.vres)
    raycaster.__generate_image__(entidades, distancia=1, camera=camera)

main()
"""
