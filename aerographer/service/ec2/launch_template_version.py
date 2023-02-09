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

"""launch_template_version resource.

    Dynamically generated Generic Crawler resource class is placed here.
"""

RESOURCE_DEFINITION = {
    "resourceType": "LaunchTemplateVersions",
    "idAttribute": "LaunchTemplateId",
    "paginator": "describe_launch_template_versions",
    "page_marker": None,
    "scanParameters": {"Versions": ["$Default"]},
    "responseSchema": {
        "LaunchTemplateId": str,
        "LaunchTemplateName": str,
        "VersionNumber": int,
        "VersionDescription": str,
        "CreateTime": str,
        "CreatedBy": str,
        "DefaultVersion": bool,
        "LaunchTemplateData": {
            "KernelId": str,
            "EbsOptimized": bool,
            "IamInstanceProfile": {"Arn": str, "Name": str},
            "BlockDeviceMappings": [
                {
                    "DeviceName": str,
                    "VirtualName": str,
                    "Ebs": {
                        "Encrypted": bool,
                        "DeleteOnTermination": bool,
                        "Iops": int,
                        "KmsKeyId": str,
                        "SnapshotId": str,
                        "VolumeSize": int,
                        "VolumeType": str,
                        "Throughput": int,
                    },
                    "NoDevice": str,
                }
            ],
            "NetworkInterfaces": [
                {
                    "AssociateCarrierIpAddress": bool,
                    "AssociatePublicIpAddress": bool,
                    "DeleteOnTermination": bool,
                    "Description": str,
                    "DeviceIndex": int,
                    "Groups": [str],
                    "InterfaceType": str,
                    "Ipv6AddressCount": int,
                    "Ipv6Addresses": [{"Ipv6Address": str}],
                    "NetworkInterfaceId": str,
                    "PrivateIpAddress": str,
                    "PrivateIpAddresses": [{"Primary": bool, "PrivateIpAddress": str}],
                    "SecondaryPrivateIpAddressCount": int,
                    "SubnetId": str,
                    "NetworkCardIndex": int,
                    "Ipv4Prefixes": [{"Ipv4Prefix": str}],
                    "Ipv4PrefixCount": int,
                    "Ipv6Prefixes": [{"Ipv6Prefix": str}],
                    "Ipv6PrefixCount": int,
                }
            ],
            "ImageId": str,
            "InstanceType": str,
            "KeyName": str,
            "Monitoring": {"Enabled": bool},
            "Placement": {
                "AvailabilityZone": str,
                "Affinity": str,
                "GroupName": str,
                "HostId": str,
                "Tenancy": str,
                "SpreadDomain": str,
                "HostResourceGroupArn": str,
                "PartitionNumber": int,
            },
            "RamDiskId": str,
            "DisableApiTermination": bool,
            "InstanceInitiatedShutdownBehavior": str,
            "UserData": str,
            "TagSpecifications": [
                {"ResourceType": str, "Tags": [{"Key": str, "Value": str}]}
            ],
            "ElasticGpuSpecifications": [{"Type": str}],
            "ElasticInferenceAccelerators": [{"Type": str, "Count": int}],
            "SecurityGroupIds": [str],
            "SecurityGroups": [str],
            "InstanceMarketOptions": {
                "MarketType": str,
                "SpotOptions": {
                    "MaxPrice": str,
                    "SpotInstanceType": str,
                    "BlockDurationMinutes": int,
                    "ValidUntil": str,
                    "InstanceInterruptionBehavior": str,
                },
            },
            "CreditSpecification": {"CpuCredits": str},
            "CpuOptions": {"CoreCount": int, "ThreadsPerCore": int},
            "CapacityReservationSpecification": {
                "CapacityReservationPreference": str,
                "CapacityReservationTarget": {
                    "CapacityReservationId": str,
                    "CapacityReservationResourceGroupArn": str,
                },
            },
            "LicenseSpecifications": [{"LicenseConfigurationArn": str}],
            "HibernationOptions": {"Configured": bool},
            "MetadataOptions": {
                "State": str,
                "HttpTokens": str,
                "HttpPutResponseHopLimit": int,
                "HttpEndpoint": str,
                "HttpProtocolIpv6": str,
                "InstanceMetadataTags": str,
            },
            "EnclaveOptions": {"Enabled": bool},
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
            "PrivateDnsNameOptions": {
                "HostnameType": str,
                "EnableResourceNameDnsARecord": bool,
                "EnableResourceNameDnsAAAARecord": bool,
            },
            "MaintenanceOptions": {"AutoRecovery": str},
        },
    },
}
