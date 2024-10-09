from enum import StrEnum
from aenum import extend_enum
from .const import SensorDeviceClass, DEVICE_CLASS_UNITS

# capture the initial state of the namespace
_initial_namespace = set(globals().keys())

# some constants that (arguably) *should* be in Home Assistant

# extend the SensorDeviceClass with our extra bits
for name, value in (
        ("CONCENTRATION", "concentration"),
        ("TOTAL_ALKALINITY", "total_alkalinity"),
        ("SALINITY", "salinity"),
        ("CALCIUM", "calcium"),
        ("MAGNESIUM", "magnesium")
):
    extend_enum(SensorDeviceClass, name, value)

class UnitOfConcentration(StrEnum):
    PARTS_PER_THOUSAND = "ppt"
    PARTS_PER_MILLION = "ppm"
    PARTS_PER_BILLION = "ppb"

# 1 meq/L = 50 mg/L = 2.8 dKH
# 1 dKH = 17.9 mg/L = 17.9 ppm
class UnitOfTotalAlkalinity(StrEnum):
    DEGREES_OF_CARBONATE_HARDNESS = "dKH"
    MILLIGRAMS_PER_LITER = "mg/L"
    MILLIEQUIVALENTS_PER_LITER = "meq/L"
    PARTS_PER_MILLION = "ppm"

DEVICE_CLASS_UNITS_EXTRA: dict[SensorDeviceClass, set[type[StrEnum] | str | None]] = {
    SensorDeviceClass.CONCENTRATION: set(UnitOfConcentration),
    SensorDeviceClass.TOTAL_ALKALINITY: set(UnitOfTotalAlkalinity),
    SensorDeviceClass.SALINITY: set(UnitOfConcentration),
    SensorDeviceClass.CALCIUM: set(UnitOfConcentration),
    SensorDeviceClass.MAGNESIUM: set(UnitOfConcentration)
}
DEVICE_CLASS_UNITS_EXTRA.update(DEVICE_CLASS_UNITS)

# capture the current state of the namespace
_current_namespace = set(globals().keys())

# dynamically create __all__ to include all variables defined in this module (not imported)
__all__ = [name for name in (_current_namespace - _initial_namespace)]
