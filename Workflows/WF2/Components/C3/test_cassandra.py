from cassandra.cluster import Cluster

def main():
    cluster = Cluster(["cassandra"])
    session = cluster.connect()
    print("well done")

if __name__ == "__main__":
    main()

