from vectorshape.curvilinear_solid import CurvilinearSolid


class Torus(CurvilinearSolid):
    def __init__(self, pos_arr: tuple[float, float, float]):
        super().__init__(pos_arr)
