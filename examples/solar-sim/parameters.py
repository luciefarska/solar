from functools import cache
import quanscient as qs
from expressions import expr
from materials import mat
from regions import reg

class Parameters:
    @cache
    def k(self) -> qs.parameter:
        """
        Thermal conductivity
        """
        p = qs.parameter(1, 1)

        p.setvalue(reg.monocrystalline_silicon_target, mat.monocrystalline_silicon.k())
        p.setvalue(reg.aluminium_target, mat.aluminium.k())
        p.setvalue(reg.copper_target, mat.copper.k())
        p.setvalue(reg.solder_all_volumes, mat.solder.k())

        return p

    @cache
    def rho(self) -> qs.parameter:
        """
        Density
        """
        p = qs.parameter(1, 1)

        p.setvalue(reg.monocrystalline_silicon_target, mat.monocrystalline_silicon.rho())
        p.setvalue(reg.aluminium_target, mat.aluminium.rho())
        p.setvalue(reg.copper_target, mat.copper.rho())
        p.setvalue(reg.solder_all_volumes, mat.solder.rho())

        return p

    @cache
    def cp(self) -> qs.parameter:
        """
        Heat capacity
        """
        p = qs.parameter(1, 1)

        p.setvalue(reg.monocrystalline_silicon_target, mat.monocrystalline_silicon.cp())
        p.setvalue(reg.aluminium_target, mat.aluminium.cp())
        p.setvalue(reg.copper_target, mat.copper.cp())
        p.setvalue(reg.solder_all_volumes, mat.solder.cp())

        return p

    @cache
    def H(self) -> qs.parameter:
        """
        Elasticity matrix
        """
        p = qs.parameter(6, 6)

        p.setvalue(reg.monocrystalline_silicon_target, mat.monocrystalline_silicon.H())
        p.setvalue(reg.aluminium_target, mat.aluminium.H())
        p.setvalue(reg.copper_target, mat.copper.H())
        p.setvalue(reg.solder_all_volumes, mat.solder.H())

        return p

    @cache
    def alpha(self) -> qs.parameter:
        """
        Coefficient of thermal expansion
        """
        p = qs.parameter(1, 1)

        p.setvalue(reg.monocrystalline_silicon_target, mat.monocrystalline_silicon.alpha())
        p.setvalue(reg.aluminium_target, mat.aluminium.alpha())
        p.setvalue(reg.copper_target, mat.copper.alpha())
        p.setvalue(reg.solder_all_volumes, mat.solder.alpha())

        return p


par = Parameters()
