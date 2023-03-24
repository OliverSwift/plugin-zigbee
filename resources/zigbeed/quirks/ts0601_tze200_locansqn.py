"""Tuya temp and humidity sensors."""

from typing import Any, Dict

from zigpy.profiles import zha
from zigpy.quirks import CustomDevice
from zigpy.zcl.clusters.general import Basic, Groups, Ota, Scenes, Time
from zigpy.zcl.clusters.measurement import RelativeHumidity, TemperatureMeasurement

from zhaquirks.const import (
    DEVICE_TYPE,
    ENDPOINTS,
    INPUT_CLUSTERS,
    MODELS_INFO,
    OUTPUT_CLUSTERS,
    PROFILE_ID,
    SKIP_CONFIGURATION,
)
from zhaquirks.tuya import TuyaLocalCluster, TuyaPowerConfigurationCluster2AAA
from zhaquirks.tuya.mcu import DPToAttributeMapping, TuyaDPType, TuyaMCUCluster


class TuyaTemperatureMeasurement(TemperatureMeasurement, TuyaLocalCluster):
    """Tuya local TemperatureMeasurement cluster."""

class TuyaRelativeHumidity(RelativeHumidity, TuyaLocalCluster):
    """Tuya local RelativeHumidity cluster with a device RH_MULTIPLIER factor."""

class TemperatureHumidityManufCluster(TuyaMCUCluster):
    """Tuya Manufacturer Cluster with Temperature and Humidity data points."""

    dp_to_attribute: Dict[int, DPToAttributeMapping] = {
        1: DPToAttributeMapping(
            TuyaTemperatureMeasurement.ep_attribute,
            "measured_value",
            dp_type=TuyaDPType.VALUE,
            converter=lambda x: x * 10,  # decidegree to centidegree
        ),
        2: DPToAttributeMapping(
            TuyaRelativeHumidity.ep_attribute,
            "measured_value",
            dp_type=TuyaDPType.VALUE,
            converter=lambda x: x * 100,
        ),
        4: DPToAttributeMapping(
            TuyaPowerConfigurationCluster2AAA.ep_attribute,
            "battery_percentage_remaining",
            dp_type=TuyaDPType.VALUE,
        ),
    }

    data_point_handlers = {
        1: "_dp_2_attr_update",
        2: "_dp_2_attr_update",
        4: "_dp_2_attr_update",
    }

class TZE200_locansqn(CustomDevice):
    """Tuya temp and humidity sensor"""

    signature = {
        # "profile_id": 260,
        # "device_type": "0x0051",
        # "in_clusters": ["0x0000","0x0004","0x0005","0xef00"],
        # "out_clusters": ["0x000a","0x0019"]
        MODELS_INFO: [("_TZE200_locansqn", "TS0601")],
        ENDPOINTS: {
            1: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.SMART_PLUG,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    TuyaMCUCluster.cluster_id,
                ],
                OUTPUT_CLUSTERS: [Ota.cluster_id, Time.cluster_id],
            }
        },
    }

    replacement = {
        SKIP_CONFIGURATION: True,
        ENDPOINTS: {
            1: {
                DEVICE_TYPE: zha.DeviceType.TEMPERATURE_SENSOR,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    TemperatureHumidityManufCluster,  # temp, humidity, and battery
                    TuyaTemperatureMeasurement,
                    TuyaRelativeHumidity,
                    TuyaPowerConfigurationCluster2AAA,
                ],
                OUTPUT_CLUSTERS: [Ota.cluster_id, Time.cluster_id],
            }
        },
    }
