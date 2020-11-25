import re
import datetime
import csv
import os

DEBUG = False
FILE = "perdif7.txt"
DATA_PATH = "event-logs"
PATH = os.path.join(DATA_PATH, FILE)



regexs = [r"image pull", r"container create", r"container start", r"image pull ([A-Za-z/\-:]+)"]
results = [[], [], [], []]

def calc_times(res):
	format_string = "%Y-%m-%dT%H:%M:%S.%f"	 
	d1 = datetime.datetime.strptime(res[0], format_string)
	d2 = datetime.datetime.strptime(res[1], format_string)
	d3 = datetime.datetime.strptime(res[2], format_string)
	t1 = (d2 - d1).total_seconds()
	t2 = (d3 - d2).total_seconds()
	t3 = (d3 - d1).total_seconds()
	return (t1, t2, t3, res[3])
	
def get_times(path, regexs):
	with open(path) as f:
		lines = f.readlines()
		for line in lines:		
			for idx, regex in enumerate(regexs):
				if re.search(regex, line):	
					searched = re.search(regexs[3], line)
					if searched:
						service = searched.group(1)
					
						results[3].append(service)
					res = line.split()[0]				
					index = res.rfind("-")					
					res = res[:index]
					index = res.rfind(":")
					res = res[:index + 1] + str(round(float(res[index + 1:]), 6))
					results[idx].append(res)
					break
	return results
for txt in os.listdir(DATA_PATH):
	print(txt)
	print("++++++++++++++++++++++++++++++++++++++++++++++++")
	path = os.path.join(DATA_PATH, txt)
	results = get_times(PATH, regexs)
	if DEBUG:

		print(results[0])
		print("************************************************")
		print(results[1])
		print("************************************************")
		print(results[2])
		print(len(results[0]))
		print(len(results[1]))
		print(len(results[2]))
	else:
		result = list(zip(*results))
		result = list(map(calc_times, result))		
		output_file = txt.split('.')[0] + "-times" + ".csv"
		with open(output_file, "w") as f:
			writer = csv.writer(f)
			writer.writerows(result)



