import cv2 as cv
import numpy as np
from vectors import Ponto, Vetor
from phong_with_args import phong
from fonte_de_luz import Luz
from ray import Ray


class Camera:
    def __init__(self, target, position, up, vres=300, hres=300):
        self.position = position
        self.target = target
        self.up = up

        self.w: "Vetor" = (self.target - self.position).__normalize__()
        self.v: "Vetor" = self.up.__cross__(self.w).__normalize__()
        self.u: "Vetor" = self.w.__cross__(self.v).__mul_escalar__(-1)
        self.vres = vres
        self.hres = hres

    def __intersect__(self, ray: "Ray", targets: list):
        smallest_distance = float("inf")
        color = [0, 0, 0]  # tudo começa preto

        for target in targets:
            intersection = target.__intersect_line__(ray.origin, ray.direction)
            if intersection:
                distance_vetor = Vetor(intersection[0], intersection[1], intersection[2])
                distance = ray.origin.__distance__(distance_vetor)
                if distance < smallest_distance:
                    smallest_distance = distance
                    color = phong(
                        target,
                        [
                            Luz(0, 5, 5, [255, 255, 255]),
                            Luz(5, 5, 5, [255, 255, 255]),
                            Luz(-5, 5, 5, [255, 255, 255]),
                            Luz(0, 5, -5, [255, 255, 255]),
                            Luz(5, 5, -5, [255, 255, 255]),
                            Luz(-5, 5, -5, [255, 255, 255]),
                            Luz(0, -5, 5, [255, 255, 255]),
                            Luz(5, -5, 5, [255, 255, 255]),
                        ],
                        Ponto(intersection[0], intersection[1], intersection[2]),
                        self.position,
                        targets,
                    )
        return color
