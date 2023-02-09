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

"""cache_cluster resource.

    Dynamically generated Generic Crawler resource class is placed here.
"""

RESOURCE_DEFINITION = {
    "resourceType": "CacheClusters",
    "idAttribute": "CacheClusterId",
    "paginator": "describe_cache_clusters",
    "page_marker": None,
    "scanParameters": {},
    "responseSchema": {
        "CacheClusterId": str,
        "ConfigurationEndpoint": {"Address": str, "Port": int},
        "ClientDownloadLandingPage": str,
        "CacheNodeType": str,
        "Engine": str,
        "EngineVersion": str,
        "CacheClusterStatus": str,
        "NumCacheNodes": int,
        "PreferredAvailabilityZone": str,
        "PreferredOutpostArn": str,
        "CacheClusterCreateTime": str,
        "PreferredMaintenanceWindow": str,
        "PendingModifiedValues": {
            "NumCacheNodes": int,
            "CacheNodeIdsToRemove": [str],
            "EngineVersion": str,
            "CacheNodeType": str,
            "AuthTokenStatus": str,
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
        "NotificationConfiguration": {"TopicArn": str, "TopicStatus": str},
        "CacheSecurityGroups": [{"CacheSecurityGroupName": str, "Status": str}],
        "CacheParameterGroup": {
            "CacheParameterGroupName": str,
            "ParameterApplyStatus": str,
            "CacheNodeIdsToReboot": [str],
        },
        "CacheSubnetGroupName": str,
        "CacheNodes": [
            {
                "CacheNodeId": str,
                "CacheNodeStatus": str,
                "CacheNodeCreateTime": str,
                "Endpoint": {"Address": str, "Port": int},
                "ParameterGroupStatus": str,
                "SourceCacheNodeId": str,
                "CustomerAvailabilityZone": str,
                "CustomerOutpostArn": str,
            }
        ],
        "AutoMinorVersionUpgrade": bool,
        "SecurityGroups": [{"SecurityGroupId": str, "Status": str}],
        "ReplicationGroupId": str,
        "SnapshotRetentionLimit": int,
        "SnapshotWindow": str,
        "AuthTokenEnabled": bool,
        "AuthTokenLastModifiedDate": str,
        "TransitEncryptionEnabled": bool,
        "AtRestEncryptionEnabled": bool,
        "ARN": str,
        "ReplicationGroupLogDeliveryEnabled": bool,
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
    },
}
