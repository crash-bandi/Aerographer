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

"""launch configuration resource.

    Dynamically generated Generic Crawler resource class is placed here.
"""

RESOURCE_DEFINITION = {
    "resourceType": "LaunchConfigurations",
    "idAttribute": "LaunchConfigurationName",
    "paginator": "describe_launch_configurations",
    "page_marker": None,
    "scanParameters": {},
    "responseSchema": {
        "LaunchConfigurationName": str,
        "LaunchConfigurationARN": str,
        "ImageId": str,
        "KeyName": str,
        "SecurityGroups": [str],
        "ClassicLinkVPCId": str,
        "ClassicLinkVPCSecurityGroups": [str],
        "UserData": str,
        "InstanceType": str,
        "KernelId": str,
        "RamdiskId": str,
        "BlockDeviceMappings": [
            {
                "VirtualName": str,
                "DeviceName": str,
                "Ebs": {
                    "SnapshotId": str,
                    "VolumeSize": int,
                    "VolumeType": str,
                    "DeleteOnTermination": bool,
                    "Iops": int,
                    "Encrypted": bool,
                    "Throughput": int,
                },
                "NoDevice": bool,
            }
        ],
        "InstanceMonitoring": {"Enabled": bool},
        "SpotPrice": str,
        "IamInstanceProfile": str,
        "CreatedTime": str,
        "EbsOptimized": bool,
        "AssociatePublicIpAddress": bool,
        "PlacementTenancy": str,
        "MetadataOptions": {
            "HttpTokens": str,
            "HttpPutResponseHopLimit": int,
            "HttpEndpoint": str,
        },
    },
}
