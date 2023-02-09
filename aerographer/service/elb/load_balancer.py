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

"""load_balancer resource.

    Dynamically generated Generic Crawler resource class is placed here.
"""

RESOURCE_DEFINITION = {
    "resourceType": "LoadBalancerDescriptions",
    "idAttribute": "LoadBalancerName",
    "paginator": "describe_load_balancers",
    "page_marker": None,
    "scanParameters": {},
    "responseSchema": {
        "LoadBalancerName": str,
        "DNSName": str,
        "CanonicalHostedZoneName": str,
        "CanonicalHostedZoneNameID": str,
        "ListenerDescriptions": [
            {
                "Listener": {
                    "Protocol": str,
                    "LoadBalancerPort": int,
                    "InstanceProtocol": str,
                    "InstancePort": int,
                    "SSLCertificateId": str,
                },
                "PolicyNames": [str],
            }
        ],
        "Policies": {
            "AppCookieStickinessPolicies": [{"PolicyName": str, "CookieName": str}],
            "LBCookieStickinessPolicies": [
                {"PolicyName": str, "CookieExpirationPeriod": int}
            ],
            "OtherPolicies": [str],
        },
        "BackendServerDescriptions": [{"InstancePort": int, "PolicyNames": [str]}],
        "AvailabilityZones": [str],
        "Subnets": [str],
        "VPCId": str,
        "Instances": [{"InstanceId": str}],
        "HealthCheck": {
            "Target": str,
            "Interval": int,
            "Timeout": int,
            "UnhealthyThreshold": int,
            "HealthyThreshold": int,
        },
        "SourceSecurityGroup": {"OwnerAlias": str, "GroupName": str},
        "SecurityGroups": [str],
        "CreatedTime": str,
        "Scheme": str,
    },
}
