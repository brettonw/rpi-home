from enum import StrEnum
from typing import Final

# these are mimics for home assistant, to eliminate the installation dependency on that large
# package during install at the client

# capture the initial state of the namespace
_initial_namespace = set(globals().keys())

# The unit of measurement if applicable
ATTR_UNIT_OF_MEASUREMENT: Final = "unit_of_measurement"


# #### UNITS OF MEASUREMENT ####
# Apparent power units
class UnitOfApparentPower(StrEnum):
    """Apparent power units."""

    VOLT_AMPERE = "VA"


# Power units
class UnitOfPower(StrEnum):
    """Power units."""

    WATT = "W"
    KILO_WATT = "kW"
    BTU_PER_HOUR = "BTU/h"


# Reactive power units
POWER_VOLT_AMPERE_REACTIVE: Final = "var"


# Energy units
class UnitOfEnergy(StrEnum):
    """Energy units."""

    GIGA_JOULE = "GJ"
    KILO_WATT_HOUR = "kWh"
    MEGA_JOULE = "MJ"
    MEGA_WATT_HOUR = "MWh"
    WATT_HOUR = "Wh"


# Electric_current units
class UnitOfElectricCurrent(StrEnum):
    """Electric current units."""

    MILLIAMPERE = "mA"
    AMPERE = "A"


# Electric_potential units
class UnitOfElectricPotential(StrEnum):
    """Electric potential units."""

    MILLIVOLT = "mV"
    VOLT = "V"


# Degree units
DEGREE: Final = "°"

# Currency units
CURRENCY_EURO: Final = "€"
CURRENCY_DOLLAR: Final = "$"
CURRENCY_CENT: Final = "¢"


# Temperature units
class UnitOfTemperature(StrEnum):
    """Temperature units."""

    CELSIUS = "°C"
    FAHRENHEIT = "°F"
    KELVIN = "K"


# Time units
class UnitOfTime(StrEnum):
    """Time units."""

    MICROSECONDS = "μs"
    MILLISECONDS = "ms"
    SECONDS = "s"
    MINUTES = "min"
    HOURS = "h"
    DAYS = "d"
    WEEKS = "w"
    MONTHS = "m"
    YEARS = "y"


# Length units
class UnitOfLength(StrEnum):
    """Length units."""

    MILLIMETERS = "mm"
    CENTIMETERS = "cm"
    METERS = "m"
    KILOMETERS = "km"
    INCHES = "in"
    FEET = "ft"
    YARDS = "yd"
    MILES = "mi"


# Frequency units
class UnitOfFrequency(StrEnum):
    """Frequency units."""

    HERTZ = "Hz"
    KILOHERTZ = "kHz"
    MEGAHERTZ = "MHz"
    GIGAHERTZ = "GHz"


# Pressure units
class UnitOfPressure(StrEnum):
    """Pressure units."""

    PA = "Pa"
    HPA = "hPa"
    KPA = "kPa"
    BAR = "bar"
    CBAR = "cbar"
    MBAR = "mbar"
    MMHG = "mmHg"
    INHG = "inHg"
    PSI = "psi"


# Sound pressure units
class UnitOfSoundPressure(StrEnum):
    """Sound pressure units."""

    DECIBEL = "dB"
    WEIGHTED_DECIBEL_A = "dBA"


# Volume units
class UnitOfVolume(StrEnum):
    """Volume units."""

    CUBIC_FEET = "ft³"
    CENTUM_CUBIC_FEET = "CCF"
    CUBIC_METERS = "m³"
    LITERS = "L"
    MILLILITERS = "mL"
    GALLONS = "gal"
    """Assumed to be US gallons in conversion utilities.

    British/Imperial gallons are not yet supported"""
    FLUID_OUNCES = "fl. oz."
    """Assumed to be US fluid ounces in conversion utilities.

    British/Imperial fluid ounces are not yet supported"""


# Volume Flow Rate units
class UnitOfVolumeFlowRate(StrEnum):
    """Volume flow rate units."""

    CUBIC_METERS_PER_HOUR = "m³/h"
    CUBIC_FEET_PER_MINUTE = "ft³/min"
    LITERS_PER_MINUTE = "L/min"
    GALLONS_PER_MINUTE = "gal/min"


# Area units
AREA_SQUARE_METERS: Final = "m²"


# Mass units
class UnitOfMass(StrEnum):
    """Mass units."""

    GRAMS = "g"
    KILOGRAMS = "kg"
    MILLIGRAMS = "mg"
    MICROGRAMS = "µg"
    OUNCES = "oz"
    POUNDS = "lb"
    STONES = "st"


# Conductivity units
class UnitOfConductivity(StrEnum):
    """Conductivity units."""

    SIEMENS = "S/cm"
    MICROSIEMENS = "µS/cm"
    MILLISIEMENS = "mS/cm"


# Light units
LIGHT_LUX: Final = "lx"

# UV Index units
UV_INDEX: Final = "UV index"

# Percentage units
PERCENTAGE: Final = "%"

# Rotational speed units
REVOLUTIONS_PER_MINUTE: Final = "rpm"


# Irradiance units
class UnitOfIrradiance(StrEnum):
    """Irradiance units."""

    WATTS_PER_SQUARE_METER = "W/m²"
    BTUS_PER_HOUR_SQUARE_FOOT = "BTU/(h⋅ft²)"


# Irradiation units


class UnitOfVolumetricFlux(StrEnum):
    """Volumetric flux, commonly used for precipitation intensity.

    The derivation of these units is a volume of rain amassing in a container
    with constant cross section in a given time
    """

    INCHES_PER_DAY = "in/d"
    """Derived from in³/(in²⋅d)"""

    INCHES_PER_HOUR = "in/h"
    """Derived from in³/(in²⋅h)"""

    MILLIMETERS_PER_DAY = "mm/d"
    """Derived from mm³/(mm²⋅d)"""

    MILLIMETERS_PER_HOUR = "mm/h"
    """Derived from mm³/(mm²⋅h)"""


class UnitOfPrecipitationDepth(StrEnum):
    """Precipitation depth.

    The derivation of these units is a volume of rain amassing in a container
    with constant cross section
    """

    INCHES = "in"
    """Derived from in³/in²"""

    MILLIMETERS = "mm"
    """Derived from mm³/mm²"""

    CENTIMETERS = "cm"
    """Derived from cm³/cm²"""


# Concentration units
CONCENTRATION_MICROGRAMS_PER_CUBIC_METER: Final = "µg/m³"
CONCENTRATION_MILLIGRAMS_PER_CUBIC_METER: Final = "mg/m³"
CONCENTRATION_MICROGRAMS_PER_CUBIC_FOOT: Final = "μg/ft³"
CONCENTRATION_PARTS_PER_CUBIC_METER: Final = "p/m³"
CONCENTRATION_PARTS_PER_MILLION: Final = "ppm"
CONCENTRATION_PARTS_PER_BILLION: Final = "ppb"


# Speed units
class UnitOfSpeed(StrEnum):
    """Speed units."""

    BEAUFORT = "Beaufort"
    FEET_PER_SECOND = "ft/s"
    METERS_PER_SECOND = "m/s"
    KILOMETERS_PER_HOUR = "km/h"
    KNOTS = "kn"
    MILES_PER_HOUR = "mph"


# Signal_strength units
SIGNAL_STRENGTH_DECIBELS: Final = "dB"
SIGNAL_STRENGTH_DECIBELS_MILLIWATT: Final = "dBm"


# Data units
class UnitOfInformation(StrEnum):
    """Information units."""

    BITS = "bit"
    KILOBITS = "kbit"
    MEGABITS = "Mbit"
    GIGABITS = "Gbit"
    BYTES = "B"
    KILOBYTES = "kB"
    MEGABYTES = "MB"
    GIGABYTES = "GB"
    TERABYTES = "TB"
    PETABYTES = "PB"
    EXABYTES = "EB"
    ZETTABYTES = "ZB"
    YOTTABYTES = "YB"
    KIBIBYTES = "KiB"
    MEBIBYTES = "MiB"
    GIBIBYTES = "GiB"
    TEBIBYTES = "TiB"
    PEBIBYTES = "PiB"
    EXBIBYTES = "EiB"
    ZEBIBYTES = "ZiB"
    YOBIBYTES = "YiB"


# Data_rate units
class UnitOfDataRate(StrEnum):
    """Data rate units."""

    BITS_PER_SECOND = "bit/s"
    KILOBITS_PER_SECOND = "kbit/s"
    MEGABITS_PER_SECOND = "Mbit/s"
    GIGABITS_PER_SECOND = "Gbit/s"
    BYTES_PER_SECOND = "B/s"
    KILOBYTES_PER_SECOND = "kB/s"
    MEGABYTES_PER_SECOND = "MB/s"
    GIGABYTES_PER_SECOND = "GB/s"
    KIBIBYTES_PER_SECOND = "KiB/s"
    MEBIBYTES_PER_SECOND = "MiB/s"
    GIBIBYTES_PER_SECOND = "GiB/s"


class SensorDeviceClass(StrEnum):
    """Device class for sensors."""

    # Non-numerical device classes
    DATE = "date"
    """Date.

    Unit of measurement: `None`

    ISO8601 format: https://en.wikipedia.org/wiki/ISO_8601
    """

    ENUM = "enum"
    """Enumeration.

    Provides a fixed list of options the state of the sensor can be in.

    Unit of measurement: `None`
    """

    TIMESTAMP = "timestamp"
    """Timestamp.

    Unit of measurement: `None`

    ISO8601 format: https://en.wikipedia.org/wiki/ISO_8601
    """

    # Numerical device classes, these should be aligned with NumberDeviceClass
    APPARENT_POWER = "apparent_power"
    """Apparent power.

    Unit of measurement: `VA`
    """

    AQI = "aqi"
    """Air Quality Index.

    Unit of measurement: `None`
    """

    ATMOSPHERIC_PRESSURE = "atmospheric_pressure"
    """Atmospheric pressure.

    Unit of measurement: `UnitOfPressure` units
    """

    BATTERY = "battery"
    """Percentage of battery that is left.

    Unit of measurement: `%`
    """

    CO = "carbon_monoxide"
    """Carbon Monoxide gas concentration.

    Unit of measurement: `ppm` (parts per million)
    """

    CO2 = "carbon_dioxide"
    """Carbon Dioxide gas concentration.

    Unit of measurement: `ppm` (parts per million)
    """

    CONDUCTIVITY = "conductivity"
    """Conductivity.

    Unit of measurement: `S/cm`, `mS/cm`, `µS/cm`
    """

    CURRENT = "current"
    """Current.

    Unit of measurement: `A`, `mA`
    """

    DATA_RATE = "data_rate"
    """Data rate.

    Unit of measurement: UnitOfDataRate
    """

    DATA_SIZE = "data_size"
    """Data size.

    Unit of measurement: UnitOfInformation
    """

    DISTANCE = "distance"
    """Generic distance.

    Unit of measurement: `LENGTH_*` units
    - SI /metric: `mm`, `cm`, `m`, `km`
    - USCS / imperial: `in`, `ft`, `yd`, `mi`
    """

    DURATION = "duration"
    """Fixed duration.

    Unit of measurement: `d`, `h`, `min`, `s`, `ms`
    """

    ENERGY = "energy"
    """Energy.

    Use this device class for sensors measuring energy consumption, for example
    electric energy consumption.
    Unit of measurement: `Wh`, `kWh`, `MWh`, `MJ`, `GJ`
    """

    ENERGY_STORAGE = "energy_storage"
    """Stored energy.

    Use this device class for sensors measuring stored energy, for example the amount
    of electric energy currently stored in a battery or the capacity of a battery.

    Unit of measurement: `Wh`, `kWh`, `MWh`, `MJ`, `GJ`
    """

    FREQUENCY = "frequency"
    """Frequency.

    Unit of measurement: `Hz`, `kHz`, `MHz`, `GHz`
    """

    GAS = "gas"
    """Gas.

    Unit of measurement:
    - SI / metric: `m³`
    - USCS / imperial: `ft³`, `CCF`
    """

    HUMIDITY = "humidity"
    """Relative humidity.

    Unit of measurement: `%`
    """

    ILLUMINANCE = "illuminance"
    """Illuminance.

    Unit of measurement: `lx`
    """

    IRRADIANCE = "irradiance"
    """Irradiance.

    Unit of measurement:
    - SI / metric: `W/m²`
    - USCS / imperial: `BTU/(h⋅ft²)`
    """

    MOISTURE = "moisture"
    """Moisture.

    Unit of measurement: `%`
    """

    MONETARY = "monetary"
    """Amount of money.

    Unit of measurement: ISO4217 currency code

    See https://en.wikipedia.org/wiki/ISO_4217#Active_codes for active codes
    """

    NITROGEN_DIOXIDE = "nitrogen_dioxide"
    """Amount of NO2.

    Unit of measurement: `µg/m³`
    """

    NITROGEN_MONOXIDE = "nitrogen_monoxide"
    """Amount of NO.

    Unit of measurement: `µg/m³`
    """

    NITROUS_OXIDE = "nitrous_oxide"
    """Amount of N2O.

    Unit of measurement: `µg/m³`
    """

    OZONE = "ozone"
    """Amount of O3.

    Unit of measurement: `µg/m³`
    """

    PH = "ph"
    """Potential hydrogen (acidity/alkalinity).

    Unit of measurement: Unitless
    """

    PM1 = "pm1"
    """Particulate matter <= 1 μm.

    Unit of measurement: `µg/m³`
    """

    PM10 = "pm10"
    """Particulate matter <= 10 μm.

    Unit of measurement: `µg/m³`
    """

    PM25 = "pm25"
    """Particulate matter <= 2.5 μm.

    Unit of measurement: `µg/m³`
    """

    POWER_FACTOR = "power_factor"
    """Power factor.

    Unit of measurement: `%`, `None`
    """

    POWER = "power"
    """Power.

    Unit of measurement: `W`, `kW`
    """

    PRECIPITATION = "precipitation"
    """Accumulated precipitation.

    Unit of measurement: UnitOfPrecipitationDepth
    - SI / metric: `cm`, `mm`
    - USCS / imperial: `in`
    """

    PRECIPITATION_INTENSITY = "precipitation_intensity"
    """Precipitation intensity.

    Unit of measurement: UnitOfVolumetricFlux
    - SI /metric: `mm/d`, `mm/h`
    - USCS / imperial: `in/d`, `in/h`
    """

    PRESSURE = "pressure"
    """Pressure.

    Unit of measurement:
    - `mbar`, `cbar`, `bar`
    - `Pa`, `hPa`, `kPa`
    - `inHg`
    - `psi`
    """

    REACTIVE_POWER = "reactive_power"
    """Reactive power.

    Unit of measurement: `var`
    """

    SIGNAL_STRENGTH = "signal_strength"
    """Signal strength.

    Unit of measurement: `dB`, `dBm`
    """

    SOUND_PRESSURE = "sound_pressure"
    """Sound pressure.

    Unit of measurement: `dB`, `dBA`
    """

    SPEED = "speed"
    """Generic speed.

    Unit of measurement: `SPEED_*` units or `UnitOfVolumetricFlux`
    - SI /metric: `mm/d`, `mm/h`, `m/s`, `km/h`
    - USCS / imperial: `in/d`, `in/h`, `ft/s`, `mph`
    - Nautical: `kn`
    - Beaufort: `Beaufort`
    """

    SULPHUR_DIOXIDE = "sulphur_dioxide"
    """Amount of SO2.

    Unit of measurement: `µg/m³`
    """

    TEMPERATURE = "temperature"
    """Temperature.

    Unit of measurement: `°C`, `°F`, `K`
    """

    VOLATILE_ORGANIC_COMPOUNDS = "volatile_organic_compounds"
    """Amount of VOC.

    Unit of measurement: `µg/m³`
    """

    VOLATILE_ORGANIC_COMPOUNDS_PARTS = "volatile_organic_compounds_parts"
    """Ratio of VOC.

    Unit of measurement: `ppm`, `ppb`
    """

    VOLTAGE = "voltage"
    """Voltage.

    Unit of measurement: `V`, `mV`
    """

    VOLUME = "volume"
    """Generic volume.

    Unit of measurement: `VOLUME_*` units
    - SI / metric: `mL`, `L`, `m³`
    - USCS / imperial: `ft³`, `CCF`, `fl. oz.`, `gal` (warning: volumes expressed in
    USCS/imperial units are currently assumed to be US volumes)
    """

    VOLUME_STORAGE = "volume_storage"
    """Generic stored volume.

    Use this device class for sensors measuring stored volume, for example the amount
    of fuel in a fuel tank.

    Unit of measurement: `VOLUME_*` units
    - SI / metric: `mL`, `L`, `m³`
    - USCS / imperial: `ft³`, `CCF`, `fl. oz.`, `gal` (warning: volumes expressed in
    USCS/imperial units are currently assumed to be US volumes)
    """

    VOLUME_FLOW_RATE = "volume_flow_rate"
    """Generic flow rate

    Unit of measurement: UnitOfVolumeFlowRate
    - SI / metric: `m³/h`, `L/min`
    - USCS / imperial: `ft³/min`, `gal/min`
    """

    WATER = "water"
    """Water.

    Unit of measurement:
    - SI / metric: `m³`, `L`
    - USCS / imperial: `ft³`, `CCF`, `gal` (warning: volumes expressed in
    USCS/imperial units are currently assumed to be US volumes)
    """

    WEIGHT = "weight"
    """Generic weight, represents a measurement of an object's mass.

    Weight is used instead of mass to fit with every day language.

    Unit of measurement: `MASS_*` units
    - SI / metric: `µg`, `mg`, `g`, `kg`
    - USCS / imperial: `oz`, `lb`
    """

    WIND_SPEED = "wind_speed"
    """Wind speed.

    Unit of measurement: `SPEED_*` units
    - SI /metric: `m/s`, `km/h`
    - USCS / imperial: `ft/s`, `mph`
    - Nautical: `kn`
    - Beaufort: `Beaufort`
    """


DEVICE_CLASS_UNITS: dict[SensorDeviceClass, set[type[StrEnum] | str | None]] = {
    SensorDeviceClass.APPARENT_POWER: set(UnitOfApparentPower),
    SensorDeviceClass.AQI: {None},
    SensorDeviceClass.ATMOSPHERIC_PRESSURE: set(UnitOfPressure),
    SensorDeviceClass.BATTERY: {PERCENTAGE},
    SensorDeviceClass.CO: {CONCENTRATION_PARTS_PER_MILLION},
    SensorDeviceClass.CO2: {CONCENTRATION_PARTS_PER_MILLION},
    SensorDeviceClass.CONDUCTIVITY: set(UnitOfConductivity),
    SensorDeviceClass.CURRENT: set(UnitOfElectricCurrent),
    SensorDeviceClass.DATA_RATE: set(UnitOfDataRate),
    SensorDeviceClass.DATA_SIZE: set(UnitOfInformation),
    SensorDeviceClass.DISTANCE: set(UnitOfLength),
    SensorDeviceClass.DURATION: {
        UnitOfTime.DAYS,
        UnitOfTime.HOURS,
        UnitOfTime.MINUTES,
        UnitOfTime.SECONDS,
        UnitOfTime.MILLISECONDS,
    },
    SensorDeviceClass.ENERGY: set(UnitOfEnergy),
    SensorDeviceClass.ENERGY_STORAGE: set(UnitOfEnergy),
    SensorDeviceClass.FREQUENCY: set(UnitOfFrequency),
    SensorDeviceClass.GAS: {
        UnitOfVolume.CENTUM_CUBIC_FEET,
        UnitOfVolume.CUBIC_FEET,
        UnitOfVolume.CUBIC_METERS,
    },
    SensorDeviceClass.HUMIDITY: {PERCENTAGE},
    SensorDeviceClass.ILLUMINANCE: {LIGHT_LUX},
    SensorDeviceClass.IRRADIANCE: set(UnitOfIrradiance),
    SensorDeviceClass.MOISTURE: {PERCENTAGE},
    SensorDeviceClass.NITROGEN_DIOXIDE: {CONCENTRATION_MICROGRAMS_PER_CUBIC_METER},
    SensorDeviceClass.NITROGEN_MONOXIDE: {CONCENTRATION_MICROGRAMS_PER_CUBIC_METER},
    SensorDeviceClass.NITROUS_OXIDE: {CONCENTRATION_MICROGRAMS_PER_CUBIC_METER},
    SensorDeviceClass.OZONE: {CONCENTRATION_MICROGRAMS_PER_CUBIC_METER},
    SensorDeviceClass.PH: {None},
    SensorDeviceClass.PM1: {CONCENTRATION_MICROGRAMS_PER_CUBIC_METER},
    SensorDeviceClass.PM10: {CONCENTRATION_MICROGRAMS_PER_CUBIC_METER},
    SensorDeviceClass.PM25: {CONCENTRATION_MICROGRAMS_PER_CUBIC_METER},
    SensorDeviceClass.POWER_FACTOR: {PERCENTAGE, None},
    SensorDeviceClass.POWER: {UnitOfPower.WATT, UnitOfPower.KILO_WATT},
    SensorDeviceClass.PRECIPITATION: set(UnitOfPrecipitationDepth),
    SensorDeviceClass.PRECIPITATION_INTENSITY: set(UnitOfVolumetricFlux),
    SensorDeviceClass.PRESSURE: set(UnitOfPressure),
    SensorDeviceClass.REACTIVE_POWER: {POWER_VOLT_AMPERE_REACTIVE},
    SensorDeviceClass.SIGNAL_STRENGTH: {
        SIGNAL_STRENGTH_DECIBELS,
        SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    },
    SensorDeviceClass.SOUND_PRESSURE: set(UnitOfSoundPressure),
    SensorDeviceClass.SPEED: set(UnitOfSpeed).union(set(UnitOfVolumetricFlux)),
    SensorDeviceClass.SULPHUR_DIOXIDE: {CONCENTRATION_MICROGRAMS_PER_CUBIC_METER},
    SensorDeviceClass.TEMPERATURE: set(UnitOfTemperature),
    SensorDeviceClass.VOLATILE_ORGANIC_COMPOUNDS: {
        CONCENTRATION_MICROGRAMS_PER_CUBIC_METER
    },
    SensorDeviceClass.VOLATILE_ORGANIC_COMPOUNDS_PARTS: {
        CONCENTRATION_PARTS_PER_BILLION,
        CONCENTRATION_PARTS_PER_MILLION,
    },
    SensorDeviceClass.VOLTAGE: set(UnitOfElectricPotential),
    SensorDeviceClass.VOLUME: set(UnitOfVolume),
    SensorDeviceClass.VOLUME_FLOW_RATE: set(UnitOfVolumeFlowRate),
    SensorDeviceClass.VOLUME_STORAGE: set(UnitOfVolume),
    SensorDeviceClass.WATER: {
        UnitOfVolume.CENTUM_CUBIC_FEET,
        UnitOfVolume.CUBIC_FEET,
        UnitOfVolume.CUBIC_METERS,
        UnitOfVolume.GALLONS,
        UnitOfVolume.LITERS,
    },
    SensorDeviceClass.WEIGHT: set(UnitOfMass),
    SensorDeviceClass.WIND_SPEED: set(UnitOfSpeed),
}

# capture the current state of the namespace
_current_namespace = set(globals().keys())

# dynamically create __all__ to include all variables defined in this module (not imported)
__all__ = [name for name in (_current_namespace - _initial_namespace)]
