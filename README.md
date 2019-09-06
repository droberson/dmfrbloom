# dmfrbloom
Bloom filters with Python standard library.

## Examples
Normal bloom filter. Expects 10,000 elements with 99.99% accuracy:
```
>>> from dmfrbloom.bloomfilter import BloomFilter
>>> bf = BloomFilter(10000, 0.01)
>>> bf.add("test")
>>> bf.lookup("test")
True
>>> bf.lookup("not in filter")
False
>>> bf.save("/home/daniel/filter")
>>> bf2 = BloomFilter(1, 0.1)
>>> bf2.load("/home/daniel/filter")
>>> bf2.lookup("test")
True
>>> bf2.lookup("also not in filter")
False
```

Time-based filter. 10k elements, 99.99% accuracy, results decay after
60 seconds:
```
>>> from dmfrbloom.timefilter import TimeFilter
>>> tf = TimeFilter(10000, 0.01, 60)
>>> tf.add("asdf")
>>> tf.lookup("asdf")
True
>>> import time
>>> time.sleep(60)
>>> tf.lookup("asdf")
False
```
