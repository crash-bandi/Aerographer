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

"""key_metadata resource.

    Dynamically generated Generic Crawler resource class is placed here.
"""

RESOURCE_DEFINITION = {
    "resourceType": "KeyMetadata",
    "idAttribute": "KeyId",
    "paginator": "describe_key",
    "page_marker": None,
    "scanParameters": {},
    "responseSchema": {
        "AWSAccountId": str,
        "KeyId": str,
        "Arn": str,
        "CreationDate": str,
        "Enabled": bool,
        "Description": str,
        "KeyUsage": str,
        "KeyState": str,
        "DeletionDate": str,
        "ValidTo": str,
        "Origin": str,
        "CustomKeyStoreId": str,
        "CloudHsmClusterId": str,
        "ExpirationModel": str,
        "KeyManager": str,
        "CustomerMasterKeySpec": str,
        "KeySpec": str,
        "EncryptionAlgorithms": [str],
        "SigningAlgorithms": [str],
        "MultiRegion": bool,
        "MultiRegionConfiguration": {
            "MultiRegionKeyType": str,
            "PrimaryKey": {"Arn": str, "Region": str},
            "ReplicaKeys": [{"Arn": str, "Region": str}],
        },
        "PendingDeletionWindowInDays": int,
        "MacAlgorithms": [str],
    },
}
