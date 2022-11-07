"""Module exceptions.

Contains custom module exception classes.
"""


class InvalidLoggingLevelError(Exception):
    """Invalid logging level encountered."""


class InvalidServiceDefinitionsExceptionError(Exception):
    """Invalid service definition encountered."""


class EvaluationModuleNotFoundExecptionError(Exception):
    """Invalid evaluations module encountered."""


class EvaluationModuleFailedToLoadExecptionError(Exception):
    """Unable to load evaluations module."""


class EvaluationMethodNotFoundError(Exception):
    """Invalid valuation method name encountered."""


class CrawlerNotFoundExecptionError(Exception):
    """Unable to find web crawler."""


class MetadataClassNotFoundExecptionError(Exception):
    """Unable to find web crawler metadata class."""


class PaginatorNotFoundExecptionError(Exception):
    """Unable for find paginator."""


class ActiveCrawlerScanExceptionError(Exception):
    """Ongoing crawler scan encountered."""


class FailedCrawlerScanExceptionError(Exception):
    """Failed crawler scan encountered."""


class TimeOutCrawlerScanExceptionError(Exception):
    """Crawler scan timeout encountered."""


class WhiteboardCreateSectionError(Exception):
    """Whiteboard create section error encountered."""


class WhiteboardGetSectionError(Exception):
    """Whiteboard get section error encountered."""


class WhiteboardRemoveSectionError(Exception):
    """Whiteboard remove section error encountered."""


class WhiteboardWriteError(Exception):
    """Whiteboard write error encountered."""


class WhiteboardGetError(Exception):
    """Whiteboard get error encountered."""


class WhiteboardEraseError(Exception):
    """Whiteboard erase error encountered."""
