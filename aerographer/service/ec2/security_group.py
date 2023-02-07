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

"""security_group resource.

    Dynamically generated Generic Crawler resource class is placed here.
"""

RESOURCE_DEFINITION = {
    "resourceType": "SecurityGroups",
    "idAttribute": "GroupId",
    "paginator": "describe_security_groups",
    "page_marker": None,
    "scanParameters": {},
    "responseSchema": {
        "Description": str,
        "GroupName": str,
        "IpPermissions": [
            {
                "FromPort": int,
                "IpProtocol": str,
                "IpRanges": [{"CidrIp": str, "Description": str}],
                "Ipv6Ranges": [{"CidrIpv6": str, "Description": str}],
                "PrefixListIds": [{"Description": str, "PrefixListId": str}],
                "ToPort": int,
                "UserIdGroupPairs": [
                    {
                        "Description": str,
                        "GroupId": str,
                        "GroupName": str,
                        "PeeringStatus": str,
                        "UserId": str,
                        "VpcId": str,
                        "VpcPeeringConnectionId": str,
                    }
                ],
            }
        ],
        "OwnerId": str,
        "GroupId": str,
        "IpPermissionsEgress": [
            {
                "FromPort": int,
                "IpProtocol": str,
                "IpRanges": [{"CidrIp": str, "Description": str}],
                "Ipv6Ranges": [{"CidrIpv6": str, "Description": str}],
                "PrefixListIds": [{"Description": str, "PrefixListId": str}],
                "ToPort": int,
                "UserIdGroupPairs": [
                    {
                        "Description": str,
                        "GroupId": str,
                        "GroupName": str,
                        "PeeringStatus": str,
                        "UserId": str,
                        "VpcId": str,
                        "VpcPeeringConnectionId": str,
                    }
                ],
            }
        ],
        "Tags": [{"Key": str, "Value": str}],
        "VpcId": str,
    },
}
