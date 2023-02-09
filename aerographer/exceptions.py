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

"""Module exceptions.

Contains custom module exception classes.
"""


class InvalidLoggingLevelError(Exception):
    """Invalid logging level encountered."""


class InvalidServiceDefinitionError(Exception):
    """Invalid service definition encountered."""


class CrawlerNotFoundError(Exception):
    """Unable to find web crawler."""


class MetadataClassNotFoundError(Exception):
    """Unable to find web crawler metadata class."""


class PaginatorNotFoundError(Exception):
    """Unable for find paginator."""


class EvaluationModuleNotFoundError(Exception):
    """Invalid evaluations module encountered."""


class EvaluationModuleFailedToLoadError(Exception):
    """Unable to load evaluations module."""


class EvaluationMethodNotFoundError(Exception):
    """Invalid evaluation method name encountered."""


class EvaluationMethodNameError(Exception):
    """Invalid evaluation function name encountered."""


class EvaluationMethodResultOutputError(Exception):
    """Invalid evaluation function output type."""


class ActiveCrawlerScanError(Exception):
    """Ongoing crawler scan encountered."""


class FailedCrawlerScanError(Exception):
    """Failed crawler scan encountered."""


class TimeOutCrawlerScanError(Exception):
    """Crawler scan timeout encountered."""


class SurveyAttributeError(Exception):
    """Survery AttributeError encountered."""


class SurveySearchQueryError(Exception):
    """Error with survery query search encountered."""


class FrozenInstanceError(Exception):
    """Frozen crawler setattr encountered."""
