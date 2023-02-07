""" Copyright 2023 Jason Lines.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

"""fleet resource.

    Dynamically generated Generic Crawler resource class is placed here.
"""

RESOURCE_DEFINITION = {
    "resourceType": "Fleets",
    "idAttribute": "FleetId",
    "paginator": "describe_fleets",
    "page_marker": None,
    "scanParameters": {},
    "responseSchema": {
        "ActivityStatus": str,
        "CreateTime": str,
        "FleetId": str,
        "FleetState": str,
        "ClientToken": str,
        "ExcessCapacityTerminationPolicy": str,
        "FulfilledCapacity": float,
        "FulfilledOnDemandCapacity": float,
        "LaunchTemplateConfigs": [
            {
                "LaunchTemplateSpecification": {
                    "LaunchTemplateId": str,
                    "LaunchTemplateName": str,
                    "Version": str,
                },
                "Overrides": [
                    {
                        "InstanceType": str,
                        "MaxPrice": str,
                        "SubnetId": str,
                        "AvailabilityZone": str,
                        "WeightedCapacity": float,
                        "Priority": float,
                        "Placement": {"GroupName": str},
                        "InstanceRequirements": {
                            "VCpuCount": {"Min": int, "Max": int},
                            "MemoryMiB": {"Min": int, "Max": int},
                            "CpuManufacturers": [str],
                            "MemoryGiBPerVCpu": {"Min": float, "Max": float},
                            "ExcludedInstanceTypes": [str],
                            "InstanceGenerations": [str],
                            "SpotMaxPricePercentageOverLowestPrice": int,
                            "OnDemandMaxPricePercentageOverLowestPrice": int,
                            "BareMetal": str,
                            "BurstablePerformance": str,
                            "RequireHibernateSupport": bool,
                            "NetworkInterfaceCount": {"Min": int, "Max": int},
                            "LocalStorage": str,
                            "LocalStorageTypes": [str],
                            "TotalLocalStorageGB": {"Min": float, "Max": float},
                            "BaselineEbsBandwidthMbps": {"Min": int, "Max": int},
                            "AcceleratorTypes": [str],
                            "AcceleratorCount": {"Min": int, "Max": int},
                            "AcceleratorManufacturers": [str],
                            "AcceleratorNames": [str],
                            "AcceleratorTotalMemoryMiB": {"Min": int, "Max": int},
                        },
                    }
                ],
            }
        ],
        "TargetCapacitySpecification": {
            "TotalTargetCapacity": int,
            "OnDemandTargetCapacity": int,
            "SpotTargetCapacity": int,
            "DefaultTargetCapacityType": str,
            "TargetCapacityUnitType": str,
        },
        "TerminateInstancesWithExpiration": bool,
        "Type": str,
        "ValidFrom": str,
        "ValidUntil": str,
        "ReplaceUnhealthyInstances": bool,
        "SpotOptions": {
            "AllocationStrategy": str,
            "MaintenanceStrategies": {
                "CapacityRebalance": {
                    "ReplacementStrategy": str,
                    "TerminationDelay": int,
                }
            },
            "InstanceInterruptionBehavior": str,
            "InstancePoolsToUseCount": int,
            "SingleInstanceType": bool,
            "SingleAvailabilityZone": bool,
            "MinTargetCapacity": int,
            "MaxTotalPrice": str,
        },
        "OnDemandOptions": {
            "AllocationStrategy": str,
            "CapacityReservationOptions": {"UsageStrategy": str},
            "SingleInstanceType": bool,
            "SingleAvailabilityZone": bool,
            "MinTargetCapacity": int,
            "MaxTotalPrice": str,
        },
        "Tags": [{"Key": str, "Value": str}],
        "Errors": [
            {
                "LaunchTemplateAndOverrides": {
                    "LaunchTemplateSpecification": {
                        "LaunchTemplateId": str,
                        "LaunchTemplateName": str,
                        "Version": str,
                    },
                    "Overrides": {
                        "InstanceType": str,
                        "MaxPrice": str,
                        "SubnetId": str,
                        "AvailabilityZone": str,
                        "WeightedCapacity": float,
                        "Priority": float,
                        "Placement": {"GroupName": str},
                        "InstanceRequirements": {
                            "VCpuCount": {"Min": int, "Max": int},
                            "MemoryMiB": {"Min": int, "Max": int},
                            "CpuManufacturers": [str],
                            "MemoryGiBPerVCpu": {"Min": float, "Max": float},
                            "ExcludedInstanceTypes": [str],
                            "InstanceGenerations": [str],
                            "SpotMaxPricePercentageOverLowestPrice": int,
                            "OnDemandMaxPricePercentageOverLowestPrice": int,
                            "BareMetal": str,
                            "BurstablePerformance": str,
                            "RequireHibernateSupport": bool,
                            "NetworkInterfaceCount": {"Min": int, "Max": int},
                            "LocalStorage": str,
                            "LocalStorageTypes": [str],
                            "TotalLocalStorageGB": {"Min": float, "Max": float},
                            "BaselineEbsBandwidthMbps": {"Min": int, "Max": int},
                            "AcceleratorTypes": [str],
                            "AcceleratorCount": {"Min": int, "Max": int},
                            "AcceleratorManufacturers": [str],
                            "AcceleratorNames": [str],
                            "AcceleratorTotalMemoryMiB": {"Min": int, "Max": int},
                        },
                    },
                },
                "Lifecycle": str,
                "ErrorCode": str,
                "ErrorMessage": str,
            }
        ],
        "Instances": [
            {
                "LaunchTemplateAndOverrides": {
                    "LaunchTemplateSpecification": {
                        "LaunchTemplateId": str,
                        "LaunchTemplateName": str,
                        "Version": str,
                    },
                    "Overrides": {
                        "InstanceType": str,
                        "MaxPrice": str,
                        "SubnetId": str,
                        "AvailabilityZone": str,
                        "WeightedCapacity": float,
                        "Priority": float,
                        "Placement": {"GroupName": str},
                        "InstanceRequirements": {
                            "VCpuCount": {"Min": int, "Max": int},
                            "MemoryMiB": {"Min": int, "Max": int},
                            "CpuManufacturers": [str],
                            "MemoryGiBPerVCpu": {"Min": float, "Max": float},
                            "ExcludedInstanceTypes": [str],
                            "InstanceGenerations": [str],
                            "SpotMaxPricePercentageOverLowestPrice": int,
                            "OnDemandMaxPricePercentageOverLowestPrice": int,
                            "BareMetal": str,
                            "BurstablePerformance": str,
                            "RequireHibernateSupport": bool,
                            "NetworkInterfaceCount": {"Min": int, "Max": int},
                            "LocalStorage": str,
                            "LocalStorageTypes": [str],
                            "TotalLocalStorageGB": {"Min": float, "Max": float},
                            "BaselineEbsBandwidthMbps": {"Min": int, "Max": int},
                            "AcceleratorTypes": [str],
                            "AcceleratorCount": {"Min": int, "Max": int},
                            "AcceleratorManufacturers": [str],
                            "AcceleratorNames": [str],
                            "AcceleratorTotalMemoryMiB": {"Min": int, "Max": int},
                        },
                    },
                },
                "Lifecycle": str,
                "InstanceIds": [str],
                "InstanceType": str,
                "Platform": str,
            }
        ],
        "Context": str,
    },
}
