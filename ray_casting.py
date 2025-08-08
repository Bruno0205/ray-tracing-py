import cv2 as cv
import numpy as np
from camera import Camera, Ray
from octree import BoundingBox, OctreeNode


class RayCasting:

    def __init__(self, hres, vres):
        self.hres = hres
        self.vres = vres
        self.image = np.zeros((self.vres, self.hres, 3), dtype=np.uint8)
        self.total_pixels = self.vres * self.hres
        self.processed_pixels = 0

    def __generate_image__(self, targets, luzes, distancia, camera: Camera, use_octree=True, window_name="imagem"):
        import time
        u = camera.u
        v = camera.v
        w = camera.w
        start = time.time()
        if use_octree:
            # Construir bounding box global da cena
            all_min = [float('inf'), float('inf'), float('inf')]
            all_max = [float('-inf'), float('-inf'), float('-inf')]
            for obj in targets:
                min_pt, max_pt = obj.get_bounds()
                all_min[0] = min(all_min[0], min_pt.x)
                all_min[1] = min(all_min[1], min_pt.y)
                all_min[2] = min(all_min[2], min_pt.z)
                all_max[0] = max(all_max[0], max_pt.x)
                all_max[1] = max(all_max[1], max_pt.y)
                all_max[2] = max(all_max[2], max_pt.z)
            scene_bbox = BoundingBox(
                type(camera.position)(*all_min),
                type(camera.position)(*all_max)
            )
            octree = OctreeNode(scene_bbox)
            for obj in targets:
                octree.insert(obj)

        for i in range(self.vres): #p/ cada pixel da tela (i, j), gera um raio partindo da câmera 
            for j in range(self.hres):
                ray = Ray(
                    origin=camera.position, #origem é sempre a pos da cam
                    direction=(
                        w.__mul_escalar__(distancia) # aponta da câmera para o target
                        + v.__mul_escalar__(2 * 0.5 * (j / self.hres - 0.5)) #vetor horizontal da câmera
                        + u.__mul_escalar__(2 * 0.5 * (i / self.vres - 0.5)) #vetor vertical da câmera
                    ),
                )
                if use_octree:
                    # Consultar octree para obter apenas objetos relevantes
                    relevant_targets = octree.query_ray(ray)
                    color = camera.__intersect__(ray, relevant_targets, luzes) #pega a cor de um objeto que o raio colidir
                else:
                    color = camera.__intersect__(ray, targets, luzes)
                self.image[i, j] = color
                self.processed_pixels += 1
                
            print(f"Carregando: {self.processed_pixels / self.total_pixels * 100:.2f}%")
        end = time.time()
        print(f"Tempo de renderização (use_octree={use_octree}): {end - start:.2f} segundos")
        cv.imshow(window_name, self.image)
        # Não bloqueia, permite abrir várias janelas
        cv.waitKey(1)
 