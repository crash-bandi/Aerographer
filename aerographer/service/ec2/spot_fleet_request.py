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

"""spot fleet request resource.

    Dynamically generated Generic Crawler resource class is placed here.
"""

RESOURCE_DEFINITION = {
    "resourceType": "SpotFleetRequestConfigs",
    "idAttribute": "SpotFleetRequestId",
    "paginator": "describe_spot_fleet_requests",
    "page_marker": None,
    "scanParameters": {},
    "responseSchema": {
        "ActivityStatus": str,
        "CreateTime": str,
        "SpotFleetRequestConfig": {
            "AllocationStrategy": str,
            "OnDemandAllocationStrategy": str,
            "SpotMaintenanceStrategies": {
                "CapacityRebalance": {
                    "ReplacementStrategy": str,
                    "TerminationDelay": int,
                }
            },
            "ClientToken": str,
            "ExcessCapacityTerminationPolicy": str,
            "FulfilledCapacity": float,
            "OnDemandFulfilledCapacity": float,
            "IamFleetRole": str,
            "LaunchSpecifications": [
                {
                    "SecurityGroups": [{"GroupName": str, "GroupId": str}],
                    "AddressingType": str,
                    "BlockDeviceMappings": [
                        {
                            "DeviceName": str,
                            "VirtualName": str,
                            "Ebs": {
                                "DeleteOnTermination": bool,
                                "Iops": int,
                                "SnapshotId": str,
                                "VolumeSize": int,
                                "VolumeType": str,
                                "KmsKeyId": str,
                                "Throughput": int,
                                "OutpostArn": str,
                                "Encrypted": bool,
                            },
                            "NoDevice": str,
                        }
                    ],
                    "EbsOptimized": bool,
                    "IamInstanceProfile": {"Arn": str, "Name": str},
                    "ImageId": str,
                    "InstanceType": str,
                    "KernelId": str,
                    "KeyName": str,
                    "Monitoring": {"Enabled": bool},
                    "NetworkInterfaces": [
                        {
                            "AssociatePublicIpAddress": bool,
                            "DeleteOnTermination": bool,
                            "Description": str,
                            "DeviceIndex": int,
                            "Groups": [str],
                            "Ipv6AddressCount": int,
                            "Ipv6Addresses": [{"Ipv6Address": str}],
                            "NetworkInterfaceId": str,
                            "PrivateIpAddress": str,
                            "PrivateIpAddresses": [
                                {"Primary": bool, "PrivateIpAddress": str}
                            ],
                            "SecondaryPrivateIpAddressCount": int,
                            "SubnetId": str,
                            "AssociateCarrierIpAddress": bool,
                            "InterfaceType": str,
                            "NetworkCardIndex": int,
                            "Ipv4Prefixes": [{"Ipv4Prefix": str}],
                            "Ipv4PrefixCount": int,
                            "Ipv6Prefixes": [{"Ipv6Prefix": str}],
                            "Ipv6PrefixCount": int,
                        }
                    ],
                    "Placement": {
                        "AvailabilityZone": str,
                        "GroupName": str,
                        "Tenancy": str,
                    },
                    "RamdiskId": str,
                    "SpotPrice": str,
                    "SubnetId": str,
                    "UserData": str,
                    "WeightedCapacity": float,
                    "TagSpecifications": [
                        {"ResourceType": str, "Tags": [{"Key": str, "Value": str}]}
                    ],
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
                            "SpotPrice": str,
                            "SubnetId": str,
                            "AvailabilityZone": str,
                            "WeightedCapacity": float,
                            "Priority": float,
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
            "SpotPrice": str,
            "TargetCapacity": int,
            "OnDemandTargetCapacity": int,
            "OnDemandMaxTotalPrice": str,
            "SpotMaxTotalPrice": str,
            "TerminateInstancesWithExpiration": bool,
            "Type": str,
            "ValidFrom": str,
            "ValidUntil": str,
            "ReplaceUnhealthyInstances": bool,
            "InstanceInterruptionBehavior": str,
            "LoadBalancersConfig": {
                "ClassicLoadBalancersConfig": {"ClassicLoadBalancers": [{"Name": str}]},
                "TargetGroupsConfig": {"TargetGroups": [{"Arn": str}]},
            },
            "InstancePoolsToUseCount": int,
            "Context": str,
            "TargetCapacityUnitType": str,
            "TagSpecifications": [
                {"ResourceType": str, "Tags": [{"Key": str, "Value": str}]}
            ],
        },
        "SpotFleetRequestId": str,
        "SpotFleetRequestState": str,
        "Tags": [{"Key": str, "Value": str}],
    },
}
