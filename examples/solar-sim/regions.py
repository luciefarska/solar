from tagmappings import tag_mappings

class PhysicalRegions:
    def __init__(self):
        self._max_physical_region = 117

    @property
    def wafer_volume(self) -> int:
        """
        Wafer_volume
        Consists of volume entities [1]
        """
        return 100

    @property
    def monocrystalline_silicon_target(self) -> int:
        """
        Monocrystalline silicon target
        Consists of volume entities [1]
        """
        return 101

    @property
    def aluminium_target(self) -> int:
        """
        Aluminium target
        Consists of volume entities [28]
        """
        return 102

    @property
    def copper_target(self) -> int:
        """
        Copper target
        Consists of volume entities [82]
        """
        return 103

    @property
    def solder_layer_2_volume(self) -> int:
        """
        Solder_layer_2_volume
        Consists of volume entities [109]
        """
        return 105

    @property
    def solder_layer_volume(self) -> int:
        """
        Solder_layer_volume
        Consists of volume entities [55]
        """
        return 106

    @property
    def solder_all_volumes(self) -> int:
        """
        Solder_all_volumes
        Consists of volume entities [55, 109]
        """
        return 107

    @property
    def convection_target(self) -> int:
        """
        Convection target
        Consists of surface entities [135, 140, 141]
        """
        return 108

    @property
    def heat_source_target(self) -> int:
        """
        Heat source target
        Consists of surface entities [135]
        """
        return 109

    @property
    def wafer_top_surface(self) -> int:
        """
        Wafer_top_surface
        Consists of surface entities [80, 140, 141]
        """
        return 110

    @property
    def thermal_expansion_target(self) -> int:
        """
        Thermal expansion target
        Consists of volume entities [1, 28, 55, 82, 109]
        """
        return 111

    @property
    def constraint_target(self) -> int:
        """
        Constraint target
        Consists of point entities [16]
        """
        return 112

    @property
    def constraint_2_target(self) -> int:
        """
        Constraint 2 target
        Consists of point entities [13]
        """
        return 113

    @property
    def constraint_3_target(self) -> int:
        """
        Constraint 3 target
        Consists of point entities [115]
        """
        return 114

    @property
    def copper_volume(self) -> int:
        """
        Copper_volume
        Consists of volume entities [82]
        """
        return 115

    @property
    def aluminium_volume(self) -> int:
        """
        Aluminium_volume
        Consists of volume entities [28]
        """
        return 116

    @property
    def all(self) -> int:
        """
        All
        Consists of volume entities [1, 28, 55, 82, 109]
        """
        return 117

    def get_next_free(self, how_many = 1) -> int:
        self._max_physical_region += how_many
        return self._max_physical_region

    def get_region_data(self):
        """
        Returns the region data (dimensions, physical region numbers, entity tags)
        for every region in the simulation
        """
        return tag_mappings.map_region_data((
            [3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 3, 0, 0, 0, 3, 3, 3],
            [100, 101, 102, 103, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117],
            [[1], [1], [28], [82], [109], [55], [55, 109], [140, 141, 135], [135], [80, 140, 141], [1, 28, 55, 82, 109], [16], [13], [115], [82], [28], [1, 28, 55, 82, 109]],
        ))


reg = PhysicalRegions()
