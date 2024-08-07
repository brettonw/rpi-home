from enum import StrEnum

WIRES = "wires"
DEFAULT_WIRES = 2
PT = "pt"
PT100 = "PT100"
PT1000 = "PT1000"
DEFAULT_PT = PT100
RTD_NOMINAL = "rtd_nominal"
REF_RESISTOR = "ref_resistor"
SELECT_PIN = "select_pin"
DEFAULT_SELECT_PIN = "D5" # from the max31865 instructions

RESISTANCE = "resistance"

class UnitOfResistance(StrEnum):
    OHM = "Ω"
