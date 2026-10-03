import math
from functools import cache
import quanscient as qs

class Expressions:
    @qs.cachedproperty
    def radius(self) -> float:
        """
        Heat source spot radius, matched to the solder ribbon width (0.002 m), so radius = half-width = 0.001 m
        """
        return 0.001

    @qs.cachedproperty
    def V(self) -> float:
        """
        Soldering head travel speed, 1 cm/s - a typical ribbon soldering speed. Traverses the 0.1 m wafer length in 10 s.
        """
        return 0.01

    @qs.cachedproperty
    def P(self) -> float:
        """
        Soldering heat source power [W]. Swept from 45 W to 70 W.
        """
        return 60.0


expr = Expressions()
