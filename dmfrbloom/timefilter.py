""" timefilter.py - Time-decay bloom filters using Python standard library."""

import time
from math import log

try:
    import mmh3
except ImportError:
    import dmfrbloom.pymmh3 as mmh3


class TimeFilter():
    """TimeFilter class - Implements time-decaying bloom filters.

    Attributes:
        size (int)      - Size of the filter.
        hashcount (int) - Ideal number of hashes per filter element.
        filter (list)   - List of elements. Value is None or a timestamp.
        timeout (int)   - Seconds that elements should be valid.

    Args:
        expected (int)   - Expected number of elements.
        f_rate (float)   - Acceptable false positve rate. Ex: 0.001
        timeout (int)    - Number of second an element is valid for.
        precision (bool) - Use floating point for timestamps? True/False
    """
    def __init__(self, expected, fp_rate, timeout, precision=False):
        self.size = self.ideal_size(expected, fp_rate)
        self.hashcount = self.ideal_hashcount(self.size, expected)
        self.filter = [None] * self.size
        self.timeout = timeout
        self.precision = precision

    @staticmethod
    def ideal_size(expected, fp_rate):
        """ideal_size() - Calculate ideal filter size.
        Args:
            expected (int) - Expected number of elements to add to the filter.
            fp_rate (int) - Desired false positive rate. Ex: 0.01 for 99.99%
        Returns:
            Ideal size (int)
        """
        return int(-(expected * log(fp_rate)) / (log(2) ** 2))

    @staticmethod
    def ideal_hashcount(size, expected):
        """ideal_hashcount() - Calculate ideal number of hashes per element.
        Args:
            size (int) - Size of the filter.
            expected (int) - Expected number of elements.
        Returns:
            Ideal number of hashes to use per element.
        """
        return int((size / int(expected)) * log(2))

    def add(self, element):
        """add() - Add an element to the filter.
        Args:
            element (str) - Element to add to the filter.
        Returns:
            Nothing.
        """
        current_time = time.time() if self.precision else int(time.time())
        for seed in range(self.hashcount):
            result = mmh3.hash(str(element), seed) % self.size
            self.filter[result] = current_time

    def lookup(self, element):
        """lookup() - Check if an element exists in the filter. This also
                      reaps expired elements if they are found.
        Args:
            element (str) - Element to check for.
        Returns:
            True if element is likely to exist in the filter.
            False if the element definitely does not exist in the filter.
        """
        current_time = time.time()
        result = True
        for seed in range(self.hashcount):
            index = mmh3.hash(str(element), seed) % self.size
            if self.filter[index] is None:
                result = False
            elif current_time - self.filter[index] > self.timeout:
                self.filter[result] = None
                result = False
        return result
