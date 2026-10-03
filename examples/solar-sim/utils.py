import math
import quanscient as qs

class Empty:
    pass

class Dynamic:
    def __getattr__(self, attr):
        if attr not in self.__dict__:
            self.__dict__[attr] = Empty()
        return self.__dict__[attr]

class Variables:
    step_index: float
    start_time: float
    time_step: float
    end_time: float
    num_time_steps: float
    discrete: float | list[float]

class Mesh:
    mesh: qs.mesh
    skin: int

class Fields:
    u: qs.field
    T: qs.field

class DerivedFields:
    sigma: qs.parameter

class Ports(Dynamic):
    pass

# Deprecated
class Consts(Variables):
    pass
