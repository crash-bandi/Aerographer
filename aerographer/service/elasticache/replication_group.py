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

"""replication_group resource.

    Dynamically generated Generic Crawler resource class is placed here.
"""

RESOURCE_DEFINITION = {
    "resourceType": "ReplicationGroups",
    "idAttribute": "ReplicationGroupId",
    "paginator": "describe_replication_groups",
    "page_marker": None,
    "scanParameters": {},
    "responseSchema": {
        "ReplicationGroupId": str,
        "Description": str,
        "GlobalReplicationGroupInfo": {
            "GlobalReplicationGroupId": str,
            "GlobalReplicationGroupMemberRole": str,
        },
        "Status": str,
        "PendingModifiedValues": {
            "PrimaryClusterId": str,
            "AutomaticFailoverStatus": str,
            "Resharding": {"SlotMigration": {"ProgressPercentage": float}},
            "AuthTokenStatus": str,
            "UserGroups": {"UserGroupIdsToAdd": [str], "UserGroupIdsToRemove": [str]},
            "LogDeliveryConfigurations": [
                {
                    "LogType": str,
                    "DestinationType": str,
                    "DestinationDetails": {
                        "CloudWatchLogsDetails": {"LogGroup": str},
                        "KinesisFirehoseDetails": {"DeliveryStream": str},
                    },
                    "LogFormat": str,
                }
            ],
        },
        "MemberClusters": [str],
        "NodeGroups": [
            {
                "NodeGroupId": str,
                "Status": str,
                "PrimaryEndpoint": {"Address": str, "Port": int},
                "ReaderEndpoint": {"Address": str, "Port": int},
                "Slots": str,
                "NodeGroupMembers": [
                    {
                        "CacheClusterId": str,
                        "CacheNodeId": str,
                        "ReadEndpoint": {"Address": str, "Port": int},
                        "PreferredAvailabilityZone": str,
                        "PreferredOutpostArn": str,
                        "CurrentRole": str,
                    }
                ],
            }
        ],
        "SnapshottingClusterId": str,
        "AutomaticFailover": str,
        "MultiAZ": str,
        "ConfigurationEndpoint": {"Address": str, "Port": int},
        "SnapshotRetentionLimit": int,
        "SnapshotWindow": str,
        "ClusterEnabled": bool,
        "CacheNodeType": str,
        "AuthTokenEnabled": bool,
        "AuthTokenLastModifiedDate": str,
        "TransitEncryptionEnabled": bool,
        "AtRestEncryptionEnabled": bool,
        "MemberClustersOutpostArns": [str],
        "KmsKeyId": str,
        "ARN": str,
        "UserGroupIds": [str],
        "LogDeliveryConfigurations": [
            {
                "LogType": str,
                "DestinationType": str,
                "DestinationDetails": {
                    "CloudWatchLogsDetails": {"LogGroup": str},
                    "KinesisFirehoseDetails": {"DeliveryStream": str},
                },
                "LogFormat": str,
                "Status": str,
                "Message": str,
            }
        ],
        "ReplicationGroupCreateTime": str,
        "DataTiering": str,
    },
}
