from cassandra.cluster import Cluster

def main():
    cluster = Cluster(port=9042)
    session = cluster.connect()
    print("well done")

if __name__ == "__main__":
    main()
