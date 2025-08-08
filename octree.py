import numpy as np

class BoundingBox:
    def __init__(self, min_point, max_point):
        self.min_point = min_point  # Ponto (x, y, z)
        self.max_point = max_point  # Ponto (x, y, z)

    def contains(self, obj):
        # Verifica se o objeto está dentro da bounding box
        # Assumimos que obj tem um método get_bounds() -> (min_point, max_point)
        obj_min, obj_max = obj.get_bounds()
        return (
            self.min_point.x <= obj_min.x and self.max_point.x >= obj_max.x and
            self.min_point.y <= obj_min.y and self.max_point.y >= obj_max.y and
            self.min_point.z <= obj_min.z and self.max_point.z >= obj_max.z
        )

    def intersects_ray(self, ray):
        # Algoritmo de interseção Ray-AABB (Axis-Aligned Bounding Box)
        tmin = (self.min_point.x - ray.origin.x) / ray.direction.x if ray.direction.x != 0 else -np.inf
        tmax = (self.max_point.x - ray.origin.x) / ray.direction.x if ray.direction.x != 0 else np.inf
        if tmin > tmax: tmin, tmax = tmax, tmin

        tymin = (self.min_point.y - ray.origin.y) / ray.direction.y if ray.direction.y != 0 else -np.inf
        tymax = (self.max_point.y - ray.origin.y) / ray.direction.y if ray.direction.y != 0 else np.inf
        if tymin > tymax: tymin, tymax = tymax, tymin

        if (tmin > tymax) or (tymin > tmax):
            return False
        if tymin > tmin:
            tmin = tymin
        if tymax < tmax:
            tmax = tymax

        tzmin = (self.min_point.z - ray.origin.z) / ray.direction.z if ray.direction.z != 0 else -np.inf
        tzmax = (self.max_point.z - ray.origin.z) / ray.direction.z if ray.direction.z != 0 else np.inf
        if tzmin > tzmax: tzmin, tzmax = tzmax, tzmin

        if (tmin > tzmax) or (tzmin > tmax):
            return False
        return True

class OctreeNode:
    def __init__(self, bounding_box, depth=0, max_depth=5, max_objects=4):
        self.bounding_box = bounding_box
        self.children = []
        self.objects = []
        self.depth = depth
        self.max_depth = max_depth
        self.max_objects = max_objects

    def insert(self, obj):
        if self.children:
            for child in self.children:
                if child.bounding_box.contains(obj):
                    child.insert(obj)
                    return
        self.objects.append(obj)
        if len(self.objects) > self.max_objects and self.depth < self.max_depth:
            self.subdivide()

    def subdivide(self):
        min_p = self.bounding_box.min_point
        max_p = self.bounding_box.max_point
        mid = type(min_p)(
            (min_p.x + max_p.x) / 2,
            (min_p.y + max_p.y) / 2,
            (min_p.z + max_p.z) / 2
        )
        # Cria as 8 subdivisões (octantes)
        octants = [
            BoundingBox(type(min_p)(x0, y0, z0), type(min_p)(x1, y1, z1))
            for x0, x1 in [(min_p.x, mid.x), (mid.x, max_p.x)]
            for y0, y1 in [(min_p.y, mid.y), (mid.y, max_p.y)]
            for z0, z1 in [(min_p.z, mid.z), (mid.z, max_p.z)]
        ]
        self.children = [OctreeNode(oct, self.depth+1, self.max_depth, self.max_objects) for oct in octants]
        objs = self.objects
        self.objects = []
        for obj in objs:
            inserted = False
            for child in self.children:
                if child.bounding_box.contains(obj):
                    child.insert(obj)
                    inserted = True
                    break
            if not inserted:
                self.objects.append(obj)

    def query_ray(self, ray):
        if not self.bounding_box.intersects_ray(ray):
            return []
        found = []
        for obj in self.objects:
            found.append(obj)
        for child in self.children:
            found.extend(child.query_ray(ray))
        return found
