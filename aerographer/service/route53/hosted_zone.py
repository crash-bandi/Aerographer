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

"""hosted zone resource.

    Dynamically generated Generic Crawler resource class is placed here.
"""

RESOURCE_DEFINITION = {
    "resourceType": "HostedZones",
    "idAttribute": "Id",
    "paginator": "list_hosted_zones",
    "page_marker": None,
    "scanParameters": {},
    "responseSchema": {
        "Id": str,
        "Name": str,
        "CallerReference": str,
        "Config": {"Comment": str, "PrivateZone": bool},
        "ResourceRecordSetCount": int,
        "LinkedService": {"ServicePrincipal": str, "Description": str},
    },
}
