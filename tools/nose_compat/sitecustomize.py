"""Compatibility aliases for Nose's deprecated Python standard-library APIs."""

import collections
import collections.abc  # pylint: disable=import-error
import inspect

if not hasattr(collections, "Callable"):
    collections.Callable = collections.abc.Callable
if not hasattr(inspect, "getargspec"):
    inspect.getargspec = inspect.getfullargspec
