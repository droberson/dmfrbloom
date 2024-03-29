""" bloomfilter.py - Bloom filters using Python standard library. """

from math import ceil, log

try:
    import mmh3
except ImportError:
    import dmfrbloom.pymmh3 as mmh3

from .bitfield import BitField


class BloomFilter():
    """BloomFilter class - Implements bloom filters using the standard library.

        Attributes:
            size (int) - size of the filter in bits.
            hashcount (int) - number of hashes per element.
            filter - (BitField object) - bitfield containing the filter.
    """
    def __init__(self, expected_items, fp_rate):
        self.size = self.ideal_size(expected_items, fp_rate)
        self.hashcount = self.ideal_hashcount(expected_items)
        self.filter = BitField(self.size)

    def add(self, element):
        """BloomFilter.add() - Add an element to the filter.

        Args:
            element (str) - Element to add to the filter.

        Returns:
            Nothing.
        """
        for seed in range(self.hashcount):
            result = mmh3.hash(str(element), seed) % self.size
            self.filter.setbit(result)

    def lookup(self, element):
        """BloomFilter.lookup() - Check if element exists in the filter.

        Args:
            element (str) - Element to look up.

        Returns:
            Nothing.
        """
        for seed in range(self.hashcount):
            result = mmh3.hash(str(element), seed) % self.size
            if self.filter.getbit(result) is False:
                return False
        return True

    def save(self, path):
        """BloomFilter.save() - Save the filter's current state to a file.

        Args:
            path (str) - Location to save the file

        Returns:
            Nothing.

        TODO: error checking if file cant be written.
        """
        with open(path, "wb") as filterfile:
            filterfile.write(self.size.to_bytes(16, byteorder="little"))
            filterfile.write(self.hashcount.to_bytes(16, byteorder="little"))
            filterfile.write(self.filter.bitfield)

    def load(self, path):
        """BloomFilter.load() - Load a saved filter.

        Args:
            path (str) - Location of filter to load.

        TODO: error check if this exists + is readable!
        """
        with open(path, "rb") as filterfile:
            self.size = int.from_bytes(filterfile.read(16), byteorder="little")
            self.hashcount = \
                int.from_bytes(filterfile.read(16), byteorder="little")
            self.filter.bitfield = filterfile.read()

    @staticmethod
    def accuracy(size, hashcount, elements):
        """BloomFilter.accuracy() - Calculate a filter's accuracy given
                                    size, hash count, and expected number
                                    of elements.

        Args:
            size (int) - Size of filter.
            hashcount (int) - Number of hashes per element.
            elements (int) - Number of expected elements.

        Returns:
            float containing a filter's percentage of accuracy.
        """
        # fp = (1 - [1 - 1 / size] ^ hashcount * expected_items ^ hashcount
        false_positive = \
            (1 - (1 - 1 / size) ** (hashcount * int(elements))) \
            ** hashcount
        print('FALSE: ', false_positive)
        return round(100 - false_positive * 100, 4)

    @staticmethod
    def ideal_size(expected, fp_rate):
        """BloomFilter.ideal_size() - Calculate ideal filter size given an
                                      expected number of elements and desired
                                      rate of false positives.

        Args:
            expected (int) - Expected number of elements in the filter.
            fp_rate (int) - Acceptable rate of false positives. Ex: 0.01 will
                            tolerate 0.01% chance of false positives.

        Returns:
            Ideal size.
        """
        return int(-(expected * log(fp_rate)) / (log(2) ** 2))

    def ideal_hashcount(self, expected):
        """BloomFilter.ideal_hashcount() - Calculate ideal number of hashes to
                                           perform given the expected number of
                                           elements to be stored in the filter.

        Args:
            expected (int) - Expected number of elements.

        Returns:
            Ideal number of hashes (int).
        """
        # ideal = (size / expected items) * log(2)
        return int((self.size / int(expected)) * log(2))

    @property
    def bytesize(self):
        """BloomFilter.bytesize() - Get size of filter.

        Args:
            None

        Returns:
            Size of filter (int)
        """
        return ceil(self.size / 8)

    @property
    def bytesize_human(self):
        """BloomFilter.bytesize_human() - Get human-readable size of filter.

        Stole this from someone on StackOverflow but don't remember where.

        Args:
            None.

        Returns:
            Filter size (str).
        """
        suffix = ['bytes', 'Kb', 'Mb', 'Gb', 'Tb', 'Pb', 'Eb', 'Zb', 'Yb']
        order = int(log(ceil(self.size) / 8, 2) / 10) if self.size else 0
        rounded = round(ceil(self.size / 8) / (1 << (order * 10)), 4)
        return str(rounded) + suffix[order]
