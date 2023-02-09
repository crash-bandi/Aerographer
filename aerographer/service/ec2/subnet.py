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

"""subnet resource.

    Dynamically generated Generic Crawler resource class is placed here.
"""

RESOURCE_DEFINITION = {
    "resourceType": "Subnets",
    "idAttribute": "SubnetId",
    "paginator": "describe_subnets",
    "page_marker": None,
    "scanParameters": {},
    "responseSchema": {
        "AvailabilityZone": str,
        "AvailabilityZoneId": str,
        "AvailableIpAddressCount": int,
        "CidrBlock": str,
        "DefaultForAz": bool,
        "EnableLniAtDeviceIndex": int,
        "MapPublicIpOnLaunch": bool,
        "MapCustomerOwnedIpOnLaunch": bool,
        "CustomerOwnedIpv4Pool": str,
        "State": str,
        "SubnetId": str,
        "VpcId": str,
        "OwnerId": str,
        "AssignIpv6AddressOnCreation": bool,
        "Ipv6CidrBlockAssociationSet": [
            {
                "AssociationId": str,
                "Ipv6CidrBlock": str,
                "Ipv6CidrBlockState": {"State": str, "StatusMessage": str},
            }
        ],
        "Tags": [{"Key": str, "Value": str}],
        "SubnetArn": str,
        "OutpostArn": str,
        "EnableDns64": bool,
        "Ipv6Native": bool,
        "PrivateDnsNameOptionsOnLaunch": {
            "HostnameType": str,
            "EnableResourceNameDnsARecord": bool,
            "EnableResourceNameDnsAAAARecord": bool,
        },
    },
}
