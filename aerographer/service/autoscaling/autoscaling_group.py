""" Copyright 2023 Jason Lines.

Licensed under the Apache License, Version 2.0 (the 'License');
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an 'AS IS' BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

"""autoscaling group resource.

    Dynamically generated Generic Crawler resource class is placed here.
"""

RESOURCE_DEFINITION = {
    'resourceType': 'AutoScalingGroups',
    'idAttribute': 'AutoScalingGroupName',
    'paginator': 'describe_auto_scaling_groups',
    'page_marker': None,
    'scanParameters': {},
    'responseSchema': {
        'AutoScalingGroupName': str,
        'AutoScalingGroupARN': str,
        'LaunchConfigurationName': str,
        'LaunchTemplate': {
            'LaunchTemplateId': str,
            'LaunchTemplateName': str,
            'Version': str,
        },
        'MixedInstancesPolicy': {
            'LaunchTemplate': {
                'LaunchTemplateSpecification': {
                    'LaunchTemplateId': str,
                    'LaunchTemplateName': str,
                    'Version': str,
                },
                'Overrides': [
                    {
                        'InstanceType': str,
                        'WeightedCapacity': str,
                        'LaunchTemplateSpecification': {
                            'LaunchTemplateId': str,
                            'LaunchTemplateName': str,
                            'Version': str,
                        },
                        'InstanceRequirements': {
                            'VCpuCount': {'Min': int, 'Max': int},
                            'MemoryMiB': {'Min': int, 'Max': int},
                            'CpuManufacturers': [str],
                            'MemoryGiBPerVCpu': {'Min': float, 'Max': float},
                            'ExcludedInstanceTypes': [str],
                            'InstanceGenerations': [str],
                            'SpotMaxPricePercentageOverLowestPrice': int,
                            'OnDemandMaxPricePercentageOverLowestPrice': int,
                            'BareMetal': str,
                            'BurstablePerformance': str,
                            'RequireHibernateSupport': bool,
                            'NetworkInterfaceCount': {'Min': int, 'Max': int},
                            'LocalStorage': 'included',
                            'LocalStorageTypes': [str],
                            'TotalLocalStorageGB': {'Min': float, 'Max': float},
                            'BaselineEbsBandwidthMbps': {'Min': int, 'Max': int},
                            'AcceleratorTypes': [str],
                            'AcceleratorCount': {'Min': int, 'Max': int},
                            'AcceleratorManufacturers': [str],
                            'AcceleratorNames': [str],
                            'AcceleratorTotalMemoryMiB': {'Min': int, 'Max': int},
                        },
                    }
                ],
            },
            'InstancesDistribution': {
                'OnDemandAllocationStrategy': str,
                'OnDemandBaseCapacity': int,
                'OnDemandPercentageAboveBaseCapacity': int,
                'SpotAllocationStrategy': str,
                'SpotInstancePools': int,
                'SpotMaxPrice': str,
            },
        },
        'MinSize': int,
        'MaxSize': int,
        'DesiredCapacity': int,
        'PredictedCapacity': int,
        'DefaultCooldown': int,
        'AvailabilityZones': [str],
        'LoadBalancerNames': [str],
        'TargetGroupARNs': [str],
        'HealthCheckType': str,
        'HealthCheckGracePeriod': int,
        'Instances': [
            {
                'InstanceId': str,
                'InstanceType': str,
                'AvailabilityZone': str,
                'LifecycleState': str,
                'HealthStatus': str,
                'LaunchConfigurationName': str,
                'LaunchTemplate': {
                    'LaunchTemplateId': str,
                    'LaunchTemplateName': str,
                    'Version': str,
                },
                'ProtectedFromScaleIn': bool,
                'WeightedCapacity': str,
            }
        ],
        'CreatedTime': str,
        'SuspendedProcesses': [{'ProcessName': str, 'SuspensionReason': str}],
        'PlacementGroup': str,
        'VPCZoneIdentifier': str,
        'EnabledMetrics': [{'Metric': str, 'Granularity': str}],
        'Status': str,
        'Tags': [
            {
                'ResourceId': str,
                'ResourceType': str,
                'Key': str,
                'Value': str,
                'PropagateAtLaunch': bool,
            }
        ],
        'TerminationPolicies': [str],
        'NewInstancesProtectedFromScaleIn': bool,
        'ServiceLinkedRoleARN': str,
        'MaxInstanceLifetime': int,
        'CapacityRebalance': bool,
        'WarmPoolConfiguration': {
            'MaxGroupPreparedCapacity': int,
            'MinSize': int,
            'PoolState': str,
            'Status': str,
            'InstanceReusePolicy': {'ReuseOnScaleIn': bool},
        },
        'WarmPoolSize': int,
        'Context': str,
        'DesiredCapacityType': str,
        'DefaultInstanceWarmup': int,
        'TrafficSources': [
            {'Identifier': str},
        ],
    },
}
