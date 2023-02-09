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

"""launch_template resource.

    Dynamically generated Generic Crawler resource class is placed here.
"""

RESOURCE_DEFINITION = {
    "resourceType": "LaunchTemplates",
    "idAttribute": "LaunchTemplateId",
    "paginator": "describe_launch_templates",
    "page_marker": None,
    "scanParameters": {},
    "responseSchema": {
        "LaunchTemplateId": str,
        "LaunchTemplateName": str,
        "CreateTime": str,
        "CreatedBy": str,
        "DefaultVersionNumber": int,
        "LatestVersionNumber": int,
        "Tags": [{"Key": str, "Value": str}],
    },
}
