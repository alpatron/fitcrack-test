"""This module contains exception classes that the page objects may throw to indicate failure."""

class InvalidStateError(Exception):
    """Indicates that a page object could not perform an action because of invalid state
    of the web Webadmin UI.
    """
