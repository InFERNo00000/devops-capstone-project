"""Run Nose with compatibility aliases removed from newer Python versions."""

import collections
import collections.abc  # pylint: disable=import-error
import inspect

from nose import main

if not hasattr(collections, "Callable"):
    collections.Callable = collections.abc.Callable
if not hasattr(inspect, "getargspec"):
    inspect.getargspec = inspect.getfullargspec

main()
