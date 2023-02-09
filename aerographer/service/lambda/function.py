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

"""function resource.

    Dynamically generated Generic Crawler resource class is placed here.
"""

RESOURCE_DEFINITION = {
    "resourceType": "Functions",
    "idAttribute": "FunctionName",
    "paginator": "list_functions",
    "page_marker": None,
    "scanParameters": {},
    "responseSchema": {
        "FunctionName": str,
        "FunctionArn": str,
        "Runtime": str,
        "Role": str,
        "Handler": str,
        "CodeSize": int,
        "Description": str,
        "Timeout": int,
        "MemorySize": int,
        "LastModified": str,
        "CodeSha256": str,
        "Version": str,
        "VpcConfig": {"SubnetIds": [str], "SecurityGroupIds": [str], "VpcId": str},
        "DeadLetterConfig": {"TargetArn": str},
        "Environment": {
            "Variables": [{"key": str, "value": str}],
            "Error": {"ErrorCode": str, "Message": str},
        },
        "KMSKeyArn": str,
        "TracingConfig": {"Mode": str},
        "MasterArn": str,
        "RevisionId": str,
        "Layers": [
            {
                "Arn": str,
                "CodeSize": int,
                "SigningProfileVersionArn": str,
                "SigningJobArn": str,
            }
        ],
        "State": str,
        "StateReason": str,
        "StateReasonCode": str,
        "LastUpdateStatus": str,
        "LastUpdateStatusReason": str,
        "LastUpdateStatusReasonCode": str,
        "FileSystemConfigs": [{"Arn": str, "LocalMountPath": str}],
        "PackageType": str,
        "ImageConfigResponse": {
            "ImageConfig": {
                "EntryPoint": [str],
                "Command": [str],
                "WorkingDirectory": str,
            },
            "Error": {"ErrorCode": str, "Message": str},
        },
        "SigningProfileVersionArn": str,
        "SigningJobArn": str,
        "Architectures": [str],
        "EphemeralStorage": {"Size": int},
        "SnapStart": {"ApplyOn": str, "OptimizationStatus": str},
    },
}
