import os
os.system("curl --unix-socket /var/run/docker.sock http:/v1.40/services/cass | python  -m json.tool >> /app/src/cassInfo.txt  ")
os.system("cat /app/src/cassInfo.txt")