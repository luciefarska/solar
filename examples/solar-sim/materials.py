import math
from functools import cache
from typing import cast
import quanscient as qs
from expressions import expr
from regions import reg

class Aluminium:
    @cache
    def alpha(self):
        """
        Coefficient of thermal expansion
        """
        return 2.31e-05

    @cache
    def c(self):
        """
        Speed of sound
        """
        return 6320.0

    @cache
    def cp(self):
        """
        Heat capacity
        """
        return 897.0

    @cache
    def E(self):
        """
        Young's modulus
        """
        return 3.5e+09

    @cache
    def epsilon(self):
        """
        Electric permittivity
        """
        return qs.getepsilon0()

    @cache
    def H(self):
        """
        Elasticity matrix
        """
        return qs.EnutoH(self.E(), self.nu())

    @cache
    def k(self):
        """
        Thermal conductivity
        """
        return 237.0

    @cache
    def mu(self):
        """
        Magnetic permeability
        """
        return qs.getmu0()

    @cache
    def nu(self):
        """
        Poisson's ratio
        """
        return 0.35

    @cache
    def rho(self):
        """
        Density
        """
        return 2700.0

    @cache
    def sigma(self):
        """
        Electric conductivity
        """
        return 3.69e+07


class Copper:
    @cache
    def alpha(self):
        """
        Coefficient of thermal expansion
        """
        return 1.65e-05

    @cache
    def cp(self):
        """
        Heat capacity
        """
        return 384.4

    @cache
    def E(self):
        """
        Young's modulus
        """
        return 1.3e+11

    @cache
    def H(self):
        """
        Elasticity matrix
        """
        return qs.EnutoH(self.E(), self.nu())

    @cache
    def k(self):
        """
        Thermal conductivity
        """
        return 406.0

    @cache
    def nu(self):
        """
        Poisson's ratio
        """
        return 0.33

    @cache
    def rho(self):
        """
        Density
        """
        return 8960.0


class MonocrystallineSilicon:
    @cache
    def alpha(self):
        """
        Coefficient of thermal expansion
        """
        return 3.36e-06

    @cache
    def cp(self):
        """
        Heat capacity
        """
        return 816.5

    @cache
    def E(self):
        """
        Young's modulus
        """
        return 1.3e+11

    @cache
    def H(self):
        """
        Elasticity matrix
        """
        return qs.EnutoH(self.E(), self.nu())

    @cache
    def k(self):
        """
        Thermal conductivity
        """
        return 237.0

    @cache
    def nu(self):
        """
        Poisson's ratio
        """
        return 0.28

    @cache
    def rho(self):
        """
        Density
        """
        return 2320.0


class Solder:
    @cache
    def alpha(self):
        """
        Coefficient of thermal expansion
        """
        return 2.35e-05

    @cache
    def cp(self):
        """
        Heat capacity
        """
        return 180.0

    @cache
    def E(self):
        """
        Young's modulus
        """
        return 2.73e+10

    @cache
    def H(self):
        """
        Elasticity matrix
        """
        return qs.EnutoH(self.E(), self.nu())

    @cache
    def k(self):
        """
        Thermal conductivity
        """
        return 70.0

    @cache
    def nu(self):
        """
        Poisson's ratio
        """
        return 0.25

    @cache
    def rho(self):
        """
        Density
        """
        return 7370.0


class Materials:
    @property
    @cache
    def aluminium(self) -> Aluminium:
        return Aluminium()

    @property
    @cache
    def copper(self) -> Copper:
        return Copper()

    @property
    @cache
    def monocrystalline_silicon(self) -> MonocrystallineSilicon:
        return MonocrystallineSilicon()

    @property
    @cache
    def solder(self) -> Solder:
        return Solder()


mat = Materials()
