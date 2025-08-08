import numpy as np
import math
from phong_with_args import refract
from vectors import Ponto, Vetor
from entidades import Mesh, Esfera, Plane
from camera import Camera
from ray_casting import RayCasting
from toro import Toro

def main():

    camera = Camera(
        target=Ponto(0, 0, 0),
        position=Ponto(-1.5, -1.5, 1),
        up=Vetor(0, 0, 1),
    )

    toro = Toro(
        centro_y = 0, 
        centro_z = 0, 
        R = 0.5, 
        r = 0.2, 
        cor = (0.5, 0, 0.5)
    )
    
    malha_toro = toro.triangulate(math.pi/12) # Espaçamento pequeno para mais detalhes (renderização demorada)
    entidades = [malha_toro]

    ray_casting = RayCasting(hres = 500, vres = 500)

    ray_casting.__generate_image__(entidades, 1, camera)

main() 