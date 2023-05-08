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

"""instanceresource.

    Dynamically generated Generic Crawler resource class is placed here.
"""

RESOURCE_DEFINITION = {
    "resourceType": "Instances",
    "idAttribute": "InstanceId",
    "paginator": "describe_instances",
    "page_marker": None,
    "scanParameters": {},
    "responseSchema": {
        "AmiLaunchIndex": int,
        "ImageId": str,
        "InstanceId": str,
        "InstanceType": str,
        "KernelId": str,
        "KeyName": str,
        "LaunchTime": str,
        "Monitoring": {"State": str},
        "Placement": {
            "AvailabilityZone": str,
            "Affinity": str,
            "GroupName": str,
            "PartitionNumber": int,
            "HostId": str,
            "Tenancy": str,
            "SpreadDomain": str,
            "HostResourceGroupArn": str,
        },
        "Platform": "Windows",
        "PrivateDnsName": str,
        "PrivateIpAddress": str,
        "ProductCodes": [{"ProductCodeId": str, "ProductCodeType": str}],
        "PublicDnsName": str,
        "PublicIpAddress": str,
        "RamdiskId": str,
        "State": {"Code": int, "Name": str},
        "StateTransitionReason": str,
        "SubnetId": str,
        "VpcId": str,
        "Architecture": str,
        "BlockDeviceMappings": [
            {
                "DeviceName": str,
                "Ebs": {
                    "AttachTime": str,
                    "DeleteOnTermination": bool,
                    "Status": str,
                    "VolumeId": str,
                },
            }
        ],
        "ClientToken": str,
        "EbsOptimized": bool,
        "EnaSupport": bool,
        "Hypervisor": str,
        "IamInstanceProfile": {"Arn": str, "Id": str},
        "InstanceLifecycle": str,
        "ElasticGpuAssociations": [
            {
                "ElasticGpuId": str,
                "ElasticGpuAssociationId": str,
                "ElasticGpuAssociationState": str,
                "ElasticGpuAssociationTime": str,
            }
        ],
        "ElasticInferenceAcceleratorAssociations": [
            {
                "ElasticInferenceAcceleratorArn": str,
                "ElasticInferenceAcceleratorAssociationId": str,
                "ElasticInferenceAcceleratorAssociationState": str,
                "ElasticInferenceAcceleratorAssociationTime": str,
            }
        ],
        "NetworkInterfaces": [
            {
                "Association": {
                    "CarrierIp": str,
                    "CustomerOwnedIp": str,
                    "IpOwnerId": str,
                    "PublicDnsName": str,
                    "PublicIp": str,
                },
                "Attachment": {
                    "AttachTime": str,
                    "AttachmentId": str,
                    "DeleteOnTermination": bool,
                    "DeviceIndex": int,
                    "Status": str,
                    "NetworkCardIndex": int,
                },
                "Description": str,
                "Groups": [{"GroupName": str, "GroupId": str}],
                "Ipv6Addresses": [{"Ipv6Address": str}],
                "MacAddress": str,
                "NetworkInterfaceId": str,
                "OwnerId": str,
                "PrivateDnsName": str,
                "PrivateIpAddress": str,
                "PrivateIpAddresses": [
                    {
                        "Association": {
                            "CarrierIp": str,
                            "CustomerOwnedIp": str,
                            "IpOwnerId": str,
                            "PublicDnsName": str,
                            "PublicIp": str,
                        },
                        "Primary": bool,
                        "PrivateDnsName": str,
                        "PrivateIpAddress": str,
                    }
                ],
                "SourceDestCheck": bool,
                "Status": str,
                "SubnetId": str,
                "VpcId": str,
                "InterfaceType": str,
                "Ipv4Prefixes": [{"Ipv4Prefix": str}],
                "Ipv6Prefixes": [{"Ipv6Prefix": str}],
            }
        ],
        "OutpostArn": str,
        "RootDeviceName": str,
        "RootDeviceType": str,
        "SecurityGroups": [{"GroupName": str, "GroupId": str}],
        "SourceDestCheck": bool,
        "SpotInstanceRequestId": str,
        "SriovNetSupport": str,
        "StateReason": {"Code": str, "Message": str},
        "Tags": [{"Key": str, "Value": str}],
        "VirtualizationType": str,
        "CpuOptions": {"CoreCount": int, "ThreadsPerCore": int},
        "CapacityReservationId": str,
        "CapacityReservationSpecification": {
            "CapacityReservationPreference": str,
            "CapacityReservationTarget": {
                "CapacityReservationId": str,
                "CapacityReservationResourceGroupArn": str,
            },
        },
        "HibernationOptions": {"Configured": bool},
        "Licenses": [{"LicenseConfigurationArn": str}],
        "MetadataOptions": {
            "State": str,
            "HttpTokens": str,
            "HttpPutResponseHopLimit": int,
            "HttpEndpoint": str,
            "HttpProtocolIpv6": str,
            "InstanceMetadataTags": str,
        },
        "EnclaveOptions": {"Enabled": bool},
        "BootMode": str,
        "PlatformDetails": str,
        "UsageOperation": str,
        "UsageOperationUpdateTime": str,
        "PrivateDnsNameOptions": {
            "HostnameType": str,
            "EnableResourceNameDnsARecord": bool,
            "EnableResourceNameDnsAAAARecord": bool,
        },
        "Ipv6Address": str,
        "MaintenanceOptions": {"AutoRecovery": str},
        "CurrentInstanceBootMode": str,
    },
}
