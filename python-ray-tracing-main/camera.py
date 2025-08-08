import cv2 as cv
import numpy as np
from vectors import Ponto, Vetor
from phong_with_args import phong, clamp
from fonte_de_luz import Luz
from ray import Ray
from entidades import Esfera

class Ray:
    def __init__(self, origin: "Ponto", direction: "Vetor"):
        #define a origem e a direção do raio
        self.origin = origin
        self.direction = direction

    def __str__(self): return f"Ray({self.origin}, {self.direction})"
    def __repr__(self): return self.__str__()
    
    #pega um ponto no raio a uma dist t
    def get_point(self, t: float) -> "Ponto": return self.origin + (self.direction.__mul_escalar__(t))
    
    #soma dois raios (origem e direção)
    def __add__(self, other: "Ray") -> "Ray": return Ray(self.origin.__add__(other.origin), self.direction.__add__(other.direction))
    
    def __sub__(self, other: "Ray") -> "Ray": return Ray(self.origin.__sub__(other.origin), self.direction.__sub__(other.direction))
    def __mul__(self, other: float) -> "Ray": return Ray(self.origin.__mul__(other), self.direction.__mul__(other))
    def __truediv__(self, other: float) -> "Ray": return Ray(self.origin.__truediv__(other), self.direction.__truediv__(other))

class Camera:
    def __init__(self, target: "Ponto", position: "Ponto", up: "Vetor", vres: int = 300, hres: int = 300):
        #inicializa a câmera c/ pos, alvo e vetor up
        self.position = position
        self.target = target
        self.up = up

        #vetor w aponta p/ o alvo (target)
        self.w: "Vetor" = self.target.__sub__(self.position)
        #vetor v é o "right", ortogonal a w e up
        self.v: "Vetor" = self.up.__cross__(self.w)

        #normaliza os vetores p/ serem unitários
        self.w = self.w.__normalize__()
        self.v = self.v.__normalize__()

        #vetor u é o "up" real, corrigido p/ o sistema de coords
        self.u: "Vetor" = self.w.__cross__(self.v).__mul_escalar__(-1)
        self.u = self.u.__normalize__()

        self.vres = vres
        self.hres = hres

    def __intersect__(self, ray: "Ray", targets: list, luzes: list) -> list:
        smallest_distance = float("inf")
        closest_target = None
        intersection_point = None

        for target in targets:
            intersection = target.__intersect_line__(ray.origin, ray.direction)
            
            if intersection:
                p_intersec = Ponto(intersection[0], intersection[1], intersection[2])
                distance = ray.origin.__distance__(p_intersec)
                if distance < smallest_distance and distance > 1e-4:
                    smallest_distance, closest_target, intersection_point = distance, target, p_intersec

        if closest_target:
            #Se encontrou um objeto, a função phong decide como colori-lo.
            return phong(
                closest_target, luzes, intersection_point,
                ray.origin, 
                targets, 0, 0
            )
        
        # Se não encontrou nada, retorna preto.
        return [0, 0, 0]