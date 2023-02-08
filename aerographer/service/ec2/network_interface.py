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

"""network_interface resource.

    Dynamically generated Generic Crawler resource class is placed here.
"""

RESOURCE_DEFINITION = {
    "resourceType": "NetworkInterfaces",
    "idAttribute": "NetworkInterfaceId",
    "paginator": "describe_network_interfaces",
    "page_marker": None,
    "scanParameters": {},
    "responseSchema": {
        "Association": {
            "AllocationId": str,
            "AssociationId": str,
            "IpOwnerId": str,
            "PublicDnsName": str,
            "PublicIp": str,
            "CustomerOwnedIp": str,
            "CarrierIp": str,
        },
        "Attachment": {
            "AttachTime": str,
            "AttachmentId": str,
            "DeleteOnTermination": bool,
            "DeviceIndex": int,
            "NetworkCardIndex": int,
            "InstanceId": str,
            "InstanceOwnerId": str,
            "Status": str,
        },
        "AvailabilityZone": str,
        "Description": str,
        "Groups": [{"GroupName": str, "GroupId": str}],
        "InterfaceType": str,
        "Ipv6Addresses": [{"Ipv6Address": str}],
        "MacAddress": str,
        "NetworkInterfaceId": str,
        "OutpostArn": str,
        "OwnerId": str,
        "PrivateDnsName": str,
        "PrivateIpAddress": str,
        "PrivateIpAddresses": [
            {
                "Association": {
                    "AllocationId": str,
                    "AssociationId": str,
                    "IpOwnerId": str,
                    "PublicDnsName": str,
                    "PublicIp": str,
                    "CustomerOwnedIp": str,
                    "CarrierIp": str,
                },
                "Primary": bool,
                "PrivateDnsName": str,
                "PrivateIpAddress": str,
            }
        ],
        "Ipv4Prefixes": [{"Ipv4Prefix": str}],
        "Ipv6Prefixes": [{"Ipv6Prefix": str}],
        "RequesterId": str,
        "RequesterManaged": bool,
        "SourceDestCheck": bool,
        "Status": str,
        "SubnetId": str,
        "TagSet": [{"Key": str, "Value": str}],
        "VpcId": str,
        "DenyAllIgwTraffic": bool,
        "Ipv6Native": bool,
        "Ipv6Address": str,
    },
}
