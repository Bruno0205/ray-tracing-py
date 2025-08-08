import cv2 as cv
import numpy as np
from vectors import Ponto, Vetor
from entidades import Esfera, Plane, SuperficieRevolucao
from camera import Camera, Ray
from ray_casting import RayCasting
from fonte_de_luz import Luz

def main():


#-------------------------------TAÇA---------------------------------------------
    pontos_taca = [
        (2.5, 0.0, 0),  
        (0.5, 0.1, 0),  
        (0.01, 2.0, 0),  
        (0.01, 3.5, 0),  
        (2.5, 4.0, 0),  
        (2.0, 5.0, 0),  
        (3.0, 5.5, 0),  
        (3.5, 6.0, 0)   
    ]
    
    taca = SuperficieRevolucao(
        color=(0.9, 0.9, 1.0), 
        controle_pts=pontos_taca,
        k_difuso=0.6,
        k_ambiental=0.3,
        k_especular=0.8,
        n_rugosidade=128,
        k_reflexao=0.3
    )


#-------------------------------ERLENMEYER----------------------------------------------
    pontos_garrafa_lab = [
        (2.5, 0.0, 0),  
        (4.0, 1.5, 0),  
        (1.0, 3.0, 0),  
        (2.0, 4.0, 0), 
        (0.5, 5.0, 0),  
        (0.5, 5.5, 0),  
        (1.5, 6.0, 0)   

    ]

    garrafa_lab = SuperficieRevolucao(
        color=(0.9, 0.7, 0.1),
        controle_pts=pontos_garrafa_lab,
        k_difuso=0.5,
        k_ambiental=0.3,
        k_especular=0.9,
        n_rugosidade=128,
        k_reflexao=0.5 
    )

#-------------------------------GARRAFA PET----------------------------------------------
    pontos_garrafa_pet = [
        (1.4, 0.1, 0), 
        (2.0, -0.2, 0), 
        (2.0, 0.5, 0),  
        (2.0, 8.0, 0),  
        (2.0, 9.0, 0), 
        (2.0, 10.0, 0), 
        (1.5, 11.0, 0), 
        (0.5, 12.0, 0), 
        (0.6, 13.2, 0), 
        (0.5, 13.5, 0)  
    ]

    pontos_garrafa_pet1 = [
        (1.4, 0.1, 0),  
        (2.0, -0.2, 0), 
        (2.0, 8.0, 0),  
    ]

    pontos_garrafa_pet2 = [
        (2.0, 8.0, 0),  
        (2.0, 9.0, 0), 
        (2.0, 10.0, 0), 
        (1.5, 11.0, 0), 
    ]

    pontos_garrafa_pet3 = [
        (1.5, 11.0, 0), 
        (0.6, 13.2, 0), 
        (0.5, 13.5, 0)  
    ]


    garrafa_pet = SuperficieRevolucao(
        color=(0.8, 0.9, 1.0), 
        controle_pts=pontos_garrafa_pet,
        k_difuso=0.5,
        k_ambiental=0.3,
        k_especular=0.9,
        n_rugosidade=128,
        k_reflexao=0.7 
    )

    garrafa_pet_inf = SuperficieRevolucao(
        color=(0, 0, 0), 
        controle_pts=pontos_garrafa_pet1,
        k_difuso=0.7,
        k_ambiental=0.3,
        k_especular=0,
        n_rugosidade=64,
        k_reflexao=0.7 
    )

    garrafa_pet_rot = SuperficieRevolucao(
        color=(0, 0, 1.0), 
        controle_pts=pontos_garrafa_pet2,
        k_difuso=0.7,
        k_ambiental=0.3,
        k_especular=0.6,
        n_rugosidade=64,
        k_reflexao=0.7 
    )

    garrafa_pet_sup = SuperficieRevolucao(
        color=(0, 0, 0), 
        controle_pts=pontos_garrafa_pet3,
        k_difuso=0.7,
        k_ambiental=0.3,
        k_especular=0,
        n_rugosidade=64,
        k_reflexao=0.7 
    )

#---------------------------------------TAMPA---------------------------------------------
    pontos_tampa = [
        (0.6, 13.5, 0),  
        (0.6, 14.2, 0),  
        (0.6, 14.3, 0),  
    ]

    tampa_garrafa = SuperficieRevolucao(
        color=(0, 0, 1.0), 
        controle_pts=pontos_tampa,
        k_difuso=0.7,
        k_ambiental=0.3,
        k_especular=0,
        n_rugosidade=64
    )

#------------------------------------ESFERA------------------------------------------------

    esfera_colorida = Esfera(
        center=Ponto(1, 1, -5), 
        radius=1, 
        color=(0, 0, 1), 
        k_difuso=1,
        k_ambiental=0.2,
        k_especular=0.2,
    )

#------------------------------------------------------------------------------------------

    chao = Plane(point=Ponto(0,-0.1,0), normal=Vetor(0,1,0), color=(0.2,0.2,0.2), k_difuso=0.9)
    parede = Plane(point=Ponto(-7,0,0), normal=Vetor(1,0,0), color=(1,1,1), k_difuso=0.9)
    
    entidades = [garrafa_pet_sup, garrafa_pet_rot, garrafa_pet_inf, tampa_garrafa, chao, parede]
    #entidades = [garrafa_pet, chao, parede]

    ray_casting = RayCasting(hres=600, vres=600)
    camera = Camera(
        target=Ponto(0, 7, 0), 
        position=Ponto(30, 6, -5),
        up=Vetor(0, 1, 0),
    )
    
    luzes = [
        Luz(10, 10, -10, [255, 255, 255]),
        Luz(-10, 5, -5, [200, 200, 255])
    ]

    ray_casting.__generate_image__(entidades, luzes, 1, camera)


if __name__ == "__main__":
    main()