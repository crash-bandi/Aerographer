<p align="left">
    <a href="https://www.python.org/downloads/release/python-3100/">
        <img src="https://img.shields.io/badge/python-3.10-blue.svg" /></a>
    <a href="https://github.com/crash-bandi/Aerographer/releases">
        <img src="https://img.shields.io/badge/version-1.2.4-blue" /></a>
    <a href="https://github.com/crash-bandi/Aerographer/actions">
        <img src="https://github.com/crash-bandi/Aerographer/workflows/Tests/badge.svg?branch=release%2Fv1.2.4">
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

The `crawler` class is how aerographer identifies the specific information required for executing the desired scan. It is designed to provide a wide range of flexibility for specifying specific details about how the scan should be performed.

## Parameters

### profiles (Optional)

- What account profiles to scan with. This can be a single profile, or multiple profiles in a comma delimited string if multiple accounts should be scanned at the same time.

### regions

- What regions within the specific accounts (profiles) should be scanned. This can be a single region or multiple regions in a comma delimited string if multiple regions should be scanned at the same time.

### role (Optional)

- What role to assume to scan with. This must only be the **name** of the role, not the entire role ARN. the ARN is generated based on the AWS credentials used. If multiple accounts are being scanned at the same time and role assumption is required, the role in every account must have the same name.

### services (Optional)

- What resources will be scanned. This can be either a specific resource, or it can be an entire service. **Default is '\*'.**

```python
from aerographer.crawler import Crawler

crawler = Crawler(
    services=["ec2.security_group"], # <--- will only scan security groups.
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
    services=["*"], # <--- will scan all services
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
    services=["*"],
    skip=["ssm", "elb.tag"], # <--- will scan all services except the ssm service and the elb.tag resource.
    ...
)
```

### evaluations (Optional)

- The file or module where evalution functions are located. Only items specified in `services` will have their evaluations automatically run, however all resources provided for all `@evalutation include` decorator parameter will be automatically scanned. Therefore it is important to only specify the required evaluations to limit scanned resources to only those required, as unrequired scans can become costly.

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

## WHITEBOARD

The `WHITEBOARD` is an automatically created instance of the `aerographer.whiteboard.Whiteboard` class. It is basic class that allows easy recording and display of data. You may create your own instance of the `Whiteboard` class, however the `WHITEBOARD` instance is what aerographer uses for recording generated data.

A simple message can be recorded using the `scribble` method

```python
from aerographer.whiteboard import WHITEBOARD

WHITEBOARD.scribble(title='my scribble', msg='important information')
```

scribbles get written to the scribbles section of the `WHITEBOARD`. You can also create and use your own sections.

```python
from aerographer.whiteboard import WHITEBOARD

WHITEBOARD.new_section(new_section='my section')
WHITEBOARD.write(section='my section', title='important', msg='it is looking mightly cloudy out')
```

Sections and entries can to retrieved and removed as well. It is important to note that anything returned is a copy, not a reference. This means any changes _must_ be written back into the WHITEBOARD. By default, entries cannot be overwritten unless the `overwrite=True` parameter is provided.

```python
from aerographer.whiteboard import WHITEBOARD

my_section = WHITEBOARD.get_section(section='my section')
my_message = WHITEBOARD.get(section='my section', title='important')

WHITEBOARD.write(section='my section', title='important', msg='clear skies ahead', overwrite=True)

WHITEBOARD.erase(section='my section', title='important')
WHITEBOARD.remove_section(section='my section')
```

You can write any type of data to the `WHITEBOARD`

```python
from aerographer.whiteboard import WHITEBOARD

info = {
    'foo': [
        'bar1',
        'bar2',
        'bar3',
    ]
    'bob':'bill',
    'important': True
}

my_message = WHITEBOARD.write(section='my section', title='important' msg=info)
```

Calling the `print` function will print out to contents of the `WHITEBOARD`, using `pprint` for attempted asthetically pleasing formatting.

```python
from aerographer.whiteboard import WHITEBOARD

WHITEBOARD.print()
```

---

## evaluation

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
from aerographer.scan import SURVEY

@evaluation(service='ec2', resource='security_group', include=['ec2.network_interface'])
def security_group_check_interface(self) -> Result:
    if [eni for eni in SURVEY['ec2']['network_interface'].values() for group in eni.data.Groups if self.id == group.GroupId]
        return Result(message='Group applied to interfaces', status=True)
    return Result(message='Group not applied to interfaces', status=False)
```

It is possible to trigger ad-hoc evaluations on specific resource instances as well, if they have not been triggered automatically. Call the `evaluate` method of the resource instance and providing the evaluation method name.

```python
from aerographer.evaluations import evaluation, Result
from aerographer.scan import SURVEY

@evaluation(service='ec2', resource='network_interface'):
def in_use(self) -> bool:
    if self.data.Status != 'available':
        return True
    return False

@evaluation(service='ec2', resource='security_group', include=['ec2.network_interface'])
def security_group_check_interface(self) -> Result:
    for eni in [eni for eni in SURVEY['ec2']['network_interface'].values() for group in eni.data.Groups if self.id == group.GroupId]
        if eni.evaluate('in_use'):
            return Result(message='Group applied to an active interfaces', status=True)
        else:
            return Result(message='Group applied to all inactive interfaces', status=False)
    return Result(message='Group not applied to interfaces', status=False)
```

---

## Result

Returning a `Result` object from an evaluation recorded on the resource instance `results` attribute. They are also automatically inserted as an entry in the `WHITEBOARD`.

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

A `Result` is written to the `WHITEBOARD` with the format:

```python
WHITEBOARD.write(
    section='evaluations',
    title=f'{eval_func.__name__}:{self.id}',
    msg={'finding': result.message, 'passed':result.status}
)
```

While an evaluation will function properly if something other than a `Result` is returned, only a returned `Result` object will be automatically recorded.

```python
from aerographer.evaluations import evaluation

@evaluation(service='ec2', resource='security_group')
def security_group_evaluation(self) -> bool:
    ...
    return True # <--- Will not be automatically recorded
```

---

## SURVEY

The entire scan dataset can be access from the `SURVEY` dictionary

```python
from aerographer.crawler import Crawler
from aerographer.scan import SURVEY

crawler = Crawler(
    services=["ec2.security_group"],
    profiles=["default"],
    regions=["us-east-1"],
    evaluations=["evaluations"]
)

crawler.scan()

for id, group in SURVEY['ec2']['security_group'].items():
    print(id, group)
```

The scan data is held in the `data` attribute of the resource instance.<br />
The resource data attribute is in the structure of the resource data returned by boto3. example: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_regions > `Returns`

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

crawler data structure is this:

```json
{
  "Endpoint": "string",
  "RegionName": "string",
  "OptInStatus": "string"
}
```

This is an example of using `SURVEY` and `resource.data` to check if a security group has a specific tag.

```python
from aerographer.scan import SURVEY

def check_name_tag() -> Result:
    """return list of security groups with `Name` tag."""
    has_name_tag = []

    for group in SURVEY['ec2']['security_group'].values():
        if [tag for tag in group.data.Tags if tag.Key == 'Name']:
            has_name_tag.append(group.id)

    return has_name_tag
```

---

## ENVIRONMENTAL VARIABLES

Environmental variables can be used to provide property values.

**AG_LOGGING_LEVEL:** Set logging level. options: 'none', 'critical', 'error', 'warn', 'info', 'debug'.

**AG_AWS_PROFILES:** Comma delimited list of profiles to use.

**AG_AWS_ROLE:** Name of role to assume. Role name only, not full ARN.

**AG_AWS_REGIONS:** Comma delimited list of regions to scan.

**AG_SERVICE_DEFINITIONS:** Custom service definitions property file location.

---

## CLI

- to do

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
- route53.hosted_zone
- route53.record_set
- ssm.parameter

        
More Resources
--------------

* `NOTICE <https://github.com/crash-bandi/Aerographer/blob/main/NOTICE>`__
* `License <https://github.com/crash-bandi/Aerographer/blob/main/LICENSE>`__
