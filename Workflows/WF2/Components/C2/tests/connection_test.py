#!/usr/bin/env python
'''A file that test whether it is possible to connect to Cassandra
'''

from cassandra.cluster import Cluster

__author__ = "Randeep Ahlawat"
__version__ = "1.0.0"
__maintainer__ = "Randeep Ahlawat"
__email__ = "randeep.ahalwat@utdallas.edu"
__status__ = "Development"


def main():
    cluster = Cluster(port=9042)
    cluster.connect()
    print("well done")


if __name__ == "__main__":
    main()
