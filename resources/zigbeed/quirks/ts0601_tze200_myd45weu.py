"""Tuya temp and humidity sensors."""

from typing import Any, Dict

from zigpy.profiles import zha
from zigpy.quirks import CustomDevice
from zigpy.zcl.clusters.general import Basic, Groups, Ota, Scenes, Time
from zigpy.zcl.clusters.measurement import (
    RelativeHumidity,
    SoilMoisture,
    TemperatureMeasurement,
)

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

class TuyaSoilMoisture(SoilMoisture, TuyaLocalCluster):
    """Tuya local SoilMoisture cluster with a device RH_MULTIPLIER factor if required."""

class TuyaRelativeHumidity(RelativeHumidity, TuyaLocalCluster):
    """Tuya local RelativeHumidity cluster with a device RH_MULTIPLIER factor."""

class SoilManufCluster(TuyaMCUCluster):
    """Tuya Manufacturer Cluster with Temperature and Humidity data points."""

    dp_to_attribute: Dict[int, DPToAttributeMapping] = {
        5: DPToAttributeMapping(
            TuyaTemperatureMeasurement.ep_attribute,
            "measured_value",
            dp_type=TuyaDPType.VALUE,
            converter=lambda x: x * 100,
        ),
        3: DPToAttributeMapping(
            TuyaSoilMoisture.ep_attribute,
            "measured_value",
            dp_type=TuyaDPType.VALUE,
            converter=lambda x: x * 100,
        ),
        15: DPToAttributeMapping(
            TuyaPowerConfigurationCluster2AAA.ep_attribute,
            "battery_percentage_remaining",
            dp_type=TuyaDPType.VALUE,
        ),
    }

    data_point_handlers = {
        3: "_dp_2_attr_update",
        5: "_dp_2_attr_update",
        15: "_dp_2_attr_update",
    }


class TuyaSoilSensor(CustomDevice):
    """Tuya temp and humidity sensor (variation 03)."""

    signature = {
        # "profile_id": 260,
        # "device_type": "0x0051",
        # "in_clusters": ["0x0000","0x0004","0x0005","0xef00"],
        # "out_clusters": ["0x000a","0x0019"]
        MODELS_INFO: [("_TZE200_myd45weu", "TS0601")],
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
                    SoilManufCluster,
                    TuyaTemperatureMeasurement,
                    TuyaSoilMoisture,
                    TuyaPowerConfigurationCluster2AAA,
                ],
                OUTPUT_CLUSTERS: [Ota.cluster_id, Time.cluster_id],
            }
        },
    }
