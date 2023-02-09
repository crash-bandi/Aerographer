<p align="left">
    <a href="https://www.python.org/downloads/release/python-3100/">
        <img src="https://img.shields.io/badge/python-3.10+-blue.svg" /></a>
    <a href="https://github.com/crash-bandi/Aerographer/releases">
        <img src="https://img.shields.io/badge/version-0.0.1-blue" /></a>
    <a href="https://github.com/crash-bandi/Aerographer/actions">
        <img src="https://github.com/crash-bandi/Aerographer/workflows/Tests/badge.svg?branch=release%2Fv0.0.1">
    <a href="https://github.com/crash-bandi/Aerographer/actions">
        <img src="https://img.shields.io/badge/coverage-17%25-red" /></a>
    <a href="https://www.apache.org/licenses/LICENSE-2.0.txt">
        <img src="http://img.shields.io/pypi/l/boto3.svg?style=flat" /></a>
</p>

Aerographer is a python utility for collecting and analysing information about cloud resources. It can be used as an imported python module, or evoked directly from a command line interface. While there are many options for collecting information from cloud platform, areographer provides a unique way to build custom analysis actions to run the collected information through. A simple decorator can be used on any external function that the module will automatically find and apply to the specified cloud resource data. This creates an simple way to collect and process data without the need to build the complex mechanisms required for the actual data retrieval process. The module takes care of the dynamic creation and execution of cloud crawlers, all you need to do is write the functions to act on the data.
<br /><br />

# Installation

From GitHub:

```bash
$ python -m pip install git+ssh://git@github.com/crash-bandi/Aerographer.git@latest
```

<br />

# Basic Usage

Create the following file structure<br />
--> main.py<br />
--> evaluations<br />
----> \_\_init\_\_.py<br />
----> security_group.py

Create a custom evaluation. This example returns a `Result` with a message of the resource id and a status of passing.

```python
#security_group.py
from aerographer.evaluations import evaluation, Result

@evaluation(service='ec2', resource='security_group')
def security_group_evaluation(self):
    return Result(message=self.id, status=True)
```

Create a `crawler` instance and run a scan, then print out the evaluation results in `WHITEBOARD`.

```python
# main.py
import logging

from aerographer.crawler import Crawler
from aerographer.scan import SURVEY

logger = logging.getLogger('aerographer')
logger.setLevel(logging.INFO)

crawler = Crawler(
    services=["ec2.security_group"],
    profiles=["default"],
    regions=["us-east-1"],
    evaluations=["evaluations"]
)

crawler.scan()
```

<br />

# Advanced Usage

The `Crawler` class is how aerographer identifies the specific information required for executing the desired scan. It is designed to provide a wide range of flexibility for specifying details about how the scan should be performed.

## Parameters

### profiles (Optional)

- What account profiles to scan with. This must be a list.

### regions

- What regions within the specific accounts (profiles) should be scanned. This must be a list.

### role (Optional)

- What role to assume to scan with. This must be the list of full role ARN's. Take note that a scan wil be ran for every unique profile:role pair.

### services (Optional)

- What resources will be scanned. This can be either a specific resource, or it can be an entire service. Can be string or list. **Default is '[]'**

```python
from aerographer.crawler import Crawler

crawler = Crawler(
    services="ec2.security_group", # <--- will only scan security groups.
    ...
)

crawler = Crawler(
    services=["ec2"], # <--- will scan all resources under the ec2 service.
    ...
)

crawler = Crawler(
    services=["ec2.network_interface", "ec2.security_group", "autoscaling"], # <--- will scan the network interface and security group resources, and all resources under the autoscaling service.
    ...
)

crawler = Crawler(
    services=[], # <--- will scan all services
    ...
)
```

### skip (Optional)

- What resources to skip. This allows a service level scan to be run, but skips the provided list resources.

```python
from aerographer.crawler import Crawler

crawler = Crawler(
    services=["ec2"],
    skip=["ec2.vpc"], # <--- will scan all resources under the ec2 service except the vpc resource.
    ...
)

crawler = Crawler(
    services=[],
    skip=["ssm", "elb.tag"], # <--- will scan all services except the ssm service and the elb.tag resource.
    ...
)
```

### evaluations (Optional)

- The file or module where evalution functions are located. Only services specified in `services` will have their evaluations automatically run, however all services provided for all `@evalutation(include=[<services>]` decorator parameters will be automatically scanned. Therefore it is important to only specify the required evaluations to limit scanned resources to only those required, as unrequired scans can extend scan time.

```python
from aerographer.crawler import Crawler

crawler = Crawler(
    evaluations=["security_group.py","network_interface.py"], # <--- will look in these files for functions with the @evaluation decorator.
    ...
)

crawler = Crawler(
    evaluations=["evaluations"], # <--- will look in the `evaluations` module for functions with the @evaluation decorator. sub-modules are recursively checked.
    ...
)
```

---

## Evaluation

An evaluation is a function that get automatically applied to the specific resource type, and is automatically run during the `crawler.scan()` process.

The `@evaluation` decorator is used to identify a function as an `evaluation`. The service and resource parameters must be specific in the decorator declaration.

```python
from aerographer.evaluations import evaluation

@evaluation(service='ec2', resource='security_group')
def security_group_evaluation(self):
    ...
```

Additionally, any scan information from other resources that the evaluation depends on can be identified by providing a list of dependant resources in the `include` evaluation parameter. This will trigger the `crawler.scan()` operation to automatically gather this information.

```python
from aerographer.evaluations import evaluation, Result
from aerographer.survey import SURVEY

@evaluation(service='ec2', resource='security_group', include=['ec2.network_interface'])
def security_group_check_interface(self) -> Result:
    if SURVEY.ec2.network_interface.get_resources().where('GroupId', 'eq', self.id).get():
        return Result(message='Group applied to interfaces', status=True)
    return Result(message='Group not applied to interfaces', status=False)
```

It is possible to trigger ad-hoc evaluations on specific resource instances as well, if they have not been triggered automatically. Call the `evaluate` method of the resource instance and providing the evaluation method name.

```python
from aerographer.evaluations import evaluation, Result
from aerographer.scan import SURVEY

@evaluation(service='ec2', resource='network_interface'):
def in_use(self) -> Result:
    if self.data.Status != 'available':
        return Result("", True)
    return Result("", False)

@evaluation(service='ec2', resource='security_group', include=['ec2.network_interface'])
def security_group_check_interface(self) -> Result:
    for eni in SURVEY.ec2.network_interface.get_resources().where('Groups.*.GroupId', 'eq', self.id):
        if eni.evaluate('in_use'):
            return Result(message='Group applied to an active interfaces', status=True)
        else:
            return Result(message='Group applied to all inactive interfaces', status=False)
    return Result(message='Group not applied to interfaces', status=False)
```

---

## Result

Evaluation functions must return a `Result` object. Evaluation results are recorded on the resource instance `results` attribute.

```python
from aerographer.evaluations import evaluation, Result

@evaluation(service='ec2', resource='security_group')
def security_group_evaluation(self) -> Result:
    ...
    return Result(message=self.id, status=True) # <--- Properly returned Result object
```

A `Result` object is written to the resources's `results` attribute with the format (eval_func.**name**, result.message, result.status):

```python
[
    ('security_group_check_interface','Group applied to interfaces', True),
    ('security_group_check_tag','Tag missing', False)
]
```

---

## SURVEY

The entire scan data collection is accessed from the `SURVEY`. `SURVEY` can be imported, and `crawler.scan()` returns it. 
`SURVEY` and all underlaying objects are read-only. Attempts to modify any data will raise an exception.

```python
from aerographer.crawler import Crawler
from aerographer.survey import SURVEY

crawler = Crawler(
    services=["ec2.security_group"],
    profiles=["default"],
    regions=["us-east-1"],
    evaluations=["evaluations"]
)

crawler.scan()

for group in SURVEY.ec2.security_group.get_resources():
    print(group.id)
```

The resource attributes are in the structure of the data returned by boto3. example: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_regions >

boto3 returns this:

```json
{
  "Regions": [
    {
      "Endpoint": "string",
      "RegionName": "string",
      "OptInStatus": "string"
    }
  ]
}
```

Resource attributes are accessed as object attribues.

```python
region.Endpoint
region.RegionName
region.OptInStatus
```

Resource attribute access goes as many levels deep as the returned data structure does.

```python
kms_key.MultiRegionConfiguration.PrimaryKey.Arn
```

This is an example of using `SURVEY` and `resource` to check if a security group has a specific tag.

```python
from aerographer.survey import SURVEY

def check_name_tag() -> list[str]:
    """return list of security groups with `Name` tag."""
    has_name_tag = []

    for group in SURVEY.ec2.security_group.get_resources():
        if [tag for tag in group.Tags if tag.Key == 'Name']:
            has_name_tag.append(group.id)

    return has_name_tag
```

The `SURVEY` class can either be traversed with dot notation, or with get functions.

```python
SURVEY.ec2 == SURVEY.get_service('ec2')
SURVEY.iam.role == SURVEY.get_service('iam').get_resource_type('role')
```
A list of available `services`, `resource types`, and `resources` can be accessed through a class attribute

```python
SURVEY.services
SURVEY.ec2.resource_types
SURVEY.ec2.security_group.resources
```

Resource objects are accessed by either the `get_resources()` or `get_resource()` function at every level.

```python
SURVEY.get_resources()                      # <--- returns all resources in the survey
SURVEY.kms.get_resources()               # <--- returns all resources in the kms service
SURVEY.ec2.instance.get_resources()  # <--- returns all resources in the ec2.instance resource type
SURVEY.get_resource('sg-01234567890')
SURVEY.ec2.security_group.get_resource('sg-01234567890')
```

The `SURVEY` class has simple filtering capabilities provided with the `where()` function chained with the `get_resources()` function. The `where()` function can be chained as many times as desired. The `where_not()` is also available, and operates exactly the same as the `where()` function, but filters resources where the query does not match.

The `where()` function takes three arguements. `attribute`, `condition`, and `values`.

**attribute:** is a `string` dot notation path to the desired attribute location. List index indicators can be either a number for a specific index, or `*` for all indexes in the list.

**condition:** is the comparision to perform between `attribute` and `values`. Comparision actions follow normal python type requirements. ie: `"a" > 1 == TypeError`

The following conditions are supported:
* 'eq': equal
* 'ne': not equal
* 'gt': greater than
* 'lt': less than
* 'contains': contains
* 'not_contains': does not contain
* 'startswith': starts with
* 'endswith': ends with

**values:** is a list of values to match values at the `attribute` location.

```python
SURVEY.ec2.instance.get_resources().where('id', 'eq', 'i-123abc456def')
SURVEY.get_resources().where('Tags.*.Key', 'eq', 'stage').where_not('Tags.*.Value', 'eq', 'prod')
```

The `where()` function returns a generator like object, so in cases where a resolved iterator is required (such as an `if` statement), end the filter statement with the `get()` function to convert the return value to a list.

```python
if SURVEY.ec2.instances.get_resources().where('Platform', 'eq', 'Windows').get():   # <--- returns list
	...
	
for key in SURVEY.kms.keys.get_resources().where_not('Enabled', 'eq', True):    # <--- returns generator
	...
```
---

## ENVIRONMENTAL VARIABLES

Environmental variables can be used to provide property values.

**AG_LOGGING_LEVEL:** Set logging level. options: 'none', 'critical', 'error', 'warn', 'info', 'debug'.

**AG_AWS_PROFILES:** Comma delimited list of profiles to use.

**AG_AWS_ROLE:** Name of role to assume. Role name only, not full ARN.

**AG_AWS_REGIONS:** Comma delimited list of regions to scan.

---

## CONFIGURING AWS CREDENTIALS

Aerographer uses two internal methods for determining what AWS credentials to use. The first is the 'profiles' parameter provided during instantiation of the `Crawler` class. If the 'profile' parameter is not provided, Aerographer will look for the `AG_AWS_PROFILES` environmental variable. If both checks fail, Aerographer will fail back to the process natively used by Boto3. This is described in detail at the link below.

https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html

---

# Currently supported resource scans

**AWS**

- autoscaling.autoscaling_group
- autoscaling.launch_configuration
- dynamodb.table_id
- dynamodb.table
- ec2.fleet
- ec2.instance
- ec2.launch_template
- ec2.launch_template_version
- ec2.network_interface
- ec2.security_group
- ec2.spot_fleet_request
- ec2.subnet
- ec2.vpc
- efs.filesystem
- elasticache.cache_cluster
- elasticache.replication_group
- elasticache.replication_group_tag
- elb.load_balancer
- elb.tag
- elbv2.load_balancer
- elbv2.tag
- iam.role
- iam.role_policy
- iam.role_policy_id
- iam.role_attached_policy
- iam.policy
- iam.policy_document
- iam.aws_managed_policy
- iam.aws_managed_policy_document
- kms.key_metadata
- kms.key_rotation
- kms.key
- lambda.function
- route53.hosted_zone
- route53.record_set
- ssm.parameter

        
More Resources
--------------

* [NOTICE](https://github.com/crash-bandi/Aerographer/blob/main/NOTICE)
* [License](https://github.com/crash-bandi/Aerographer/blob/main/LICENSE)
