from vectors import Ponto, Vetor
from entidades import Mesh
from camera import Camera
from ray_casting import RayCasting
from obj_reader import ObjReader

def main():

    caminho_obj = "python-ray-tracing-main/inputs/octaedron.obj"
    obj = ObjReader(caminho_obj)

    #Lê vértices e faces do modelo
    vertices = obj.get_vertices()
    faces = obj.get_faces()

    print(f"Vertices lidos: {len(vertices)}")
    print(f"Faces lidas: {len(faces)}")

    #Aq vamos somar as coords de cada eixo para calc as médias de seus pontos para achar o seu centro na linha 24
    xs = [v.x for v in vertices]
    ys = [v.y for v in vertices]
    zs = [v.z for v in vertices]

    #Achando o centro podemos enfim ir para a linha 29 
    cx = sum(xs) / len(xs)
    cy = sum(ys) / len(ys)
    cz = sum(zs) / len(zs)

    #Onde aqui vamos mover os vértices para a origem fazendo subtrações com as médias obtidas acima
    for i, v in enumerate(vertices):
        vertices[i] = Ponto(v.x - cx, v.y - cy, v.z - cz)

    #Define material padrão se não tiver
    if obj.cur_material is None:
        class DefaultMaterial:
            ka = Vetor(0.1, 0.1, 0.1)  # Ambiente
            kd = Vetor(0.7, 0.7, 0.7)  # Difusa
            ks = Vetor(0.2, 0.2, 0.2)  # Especular
            ke = Vetor(0, 0, 0)        # Emissão
            ns = 10                    # Brilho
            ni = 1.0                   # Índice refração
            d = 1.0                    # Transparência
        obj.cur_material = DefaultMaterial()

    triangle_tuple_vertices = []
    triangle_normals = []

    #Calculo normais das faces
    for face in faces:
        triangle_tuple_vertices.append(tuple(face.vertice_indices))

        p0 = vertices[face.vertice_indices[0]]
        p1 = vertices[face.vertice_indices[1]]
        p2 = vertices[face.vertice_indices[2]]

        v1 = p1.__sub__(p0)
        v2 = p2.__sub__(p0)
        normal = v1.__cross__(v2).__normalize__()
        triangle_normals.append(normal)

    #Crio a malha
    mesh = Mesh(
        triangle_quantity=len(faces),
        vertices_quantity=len(vertices),
        vertices=vertices,
        triangle_normals=triangle_normals,
        color=(180, 180, 180),  # Cor cinza
        triangle_tuple_vertices=triangle_tuple_vertices,
        vertex_normals=[],
    )

    camera = Camera(
        target=Ponto(0, 0, 0),
        position=Ponto(0, 2, 5), # Posição
        up=Vetor(0, 1, 0),       # Vetor para cima
    )

    ray_casting = RayCasting(hres=300, vres=300)
    entidades = [mesh]

    ray_casting.__generate_image__(entidades, 1, camera)

main()
