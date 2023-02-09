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

"""table resource.

    Dynamically generated Generic Crawler resource class is placed here.
"""

RESOURCE_DEFINITION = {
    "resourceType": "Table",
    "idAttribute": "TableId",
    "paginator": "describe_table",
    "page_marker": None,
    "scanParameters": {},
    "responseSchema": {
        "AttributeDefinitions": [{"AttributeName": str, "AttributeType": str}],
        "TableName": str,
        "KeySchema": [{"AttributeName": str, "KeyType": str}],
        "TableStatus": str,
        "CreationDateTime": str,
        "ProvisionedThroughput": {
            "LastIncreaseDateTime": str,
            "LastDecreaseDateTime": str,
            "NumberOfDecreasesToday": str,
            "ReadCapacityUnits": int,
            "WriteCapacityUnits": int,
        },
        "TableSizeBytes": int,
        "ItemCount": int,
        "TableArn": str,
        "TableId": str,
        "BillingModeSummary": {
            "BillingMode": str,
            "LastUpdateToPayPerRequestDateTime": str,
        },
        "LocalSecondaryIndexes": [
            {
                "IndexName": str,
                "KeySchema": [{"AttributeName": str, "KeyType": str}],
                "Projection": {"ProjectionType": str, "NonKeyAttributes": [str]},
                "IndexSizeBytes": int,
                "ItemCount": int,
                "IndexArn": str,
            }
        ],
        "GlobalSecondaryIndexes": [
            {
                "IndexName": str,
                "KeySchema": [{"AttributeName": str, "KeyType": str}],
                "Projection": {"ProjectionType": str, "NonKeyAttributes": [str]},
                "IndexStatus": str,
                "Backfilling": bool,
                "ProvisionedThroughput": {
                    "LastIncreaseDateTime": str,
                    "LastDecreaseDateTime": str,
                    "NumberOfDecreasesToday": int,
                    "ReadCapacityUnits": int,
                    "WriteCapacityUnits": int,
                },
                "IndexSizeBytes": int,
                "ItemCount": int,
                "IndexArn": str,
            }
        ],
        "StreamSpecification": {"StreamEnabled": bool, "StreamViewType": str},
        "LatestStreamLabel": str,
        "LatestStreamArn": str,
        "GlobalTableVersion": str,
        "Replicas": [
            {
                "RegionName": str,
                "ReplicaStatus": str,
                "ReplicaStatusDescription": str,
                "ReplicaStatusPercentProgress": str,
                "KMSMasterKeyId": str,
                "ProvisionedThroughputOverride": {"ReadCapacityUnits": int},
                "GlobalSecondaryIndexes": [
                    {
                        "IndexName": str,
                        "ProvisionedThroughputOverride": {"ReadCapacityUnits": int},
                    }
                ],
                "ReplicaInaccessibleDateTime": str,
                "ReplicaTableClassSummary": {
                    "TableClass": str,
                    "LastUpdateDateTime": str,
                },
            }
        ],
        "RestoreSummary": {
            "SourceBackupArn": str,
            "SourceTableArn": str,
            "RestoreDateTime": str,
            "RestoreInProgress": bool,
        },
        "SSEDescription": {
            "Status": str,
            "SSEType": str,
            "KMSMasterKeyArn": str,
            "InaccessibleEncryptionDateTime": str,
        },
        "ArchivalSummary": {
            "ArchivalDateTime": str,
            "ArchivalReason": str,
            "ArchivalBackupArn": str,
        },
        "TableClassSummary": {"TableClass": str, "LastUpdateDateTime": str},
    },
}
