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

"""record set resource.

    Dynamically generated Generic Crawler resource class is placed here.
"""

RESOURCE_DEFINITION = {
    "resourceType": "ResourceRecordSets",
    "idAttribute": "Id",
    "paginator": "list_resource_record_sets",
    "page_marker": None,
    "scanParameters": {},
    "responseSchema": {
        "Name": str,
        "Id": str,
        "HostedZoneId": str,
        "Type": str,
        "SetIdentifier": str,
        "Weight": int,
        "Region": str,
        "GeoLocation": {
            "ContinentCode": str,
            "CountryCode": str,
            "SubdivisionCode": str,
        },
        "Failover": str,
        "MultiValueAnswer": bool,
        "TTL": int,
        "ResourceRecords": [{"Value": str}],
        "AliasTarget": {
            "HostedZoneId": str,
            "DNSName": str,
            "EvaluateTargetHealth": bool,
        },
        "HealthCheckId": str,
        "TrafficPolicyInstanceId": str,
        "CidrRoutingConfig": {"CollectionId": str, "LocationName": str},
    },
}
