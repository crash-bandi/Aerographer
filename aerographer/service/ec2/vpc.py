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

"""vpc resource.

    Dynamically generated Generic Crawler resource class is placed here.
"""

RESOURCE_DEFINITION = {
    "resourceType": "Vpcs",
    "idAttribute": "VpcId",
    "paginator": "describe_vpcs",
    "page_marker": None,
    "scanParameters": {},
    "responseSchema": {
        "CidrBlock": str,
        "DhcpOptionsId": str,
        "State": str,
        "VpcId": str,
        "OwnerId": str,
        "InstanceTenancy": str,
        "Ipv6CidrBlockAssociationSet": [
            {
                "AssociationId": str,
                "Ipv6CidrBlock": str,
                "Ipv6CidrBlockState": {"State": str, "StatusMessage": str},
                "NetworkBorderGroup": str,
                "Ipv6Pool": str,
            }
        ],
        "CidrBlockAssociationSet": [
            {
                "AssociationId": str,
                "CidrBlock": str,
                "CidrBlockState": {"State": str, "StatusMessage": str},
            }
        ],
        "IsDefault": bool,
        "Tags": [{"Key": str, "Value": str}],
    },
}
