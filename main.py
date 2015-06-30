__author__ = 'qqibrow'
import re

pid2cwd = {};
includesList = [];

def doAnalysis(f):
    for line in f:
        # add pwd to pid -> pwd table.
        pid = re.search("^\d+", line);
        cwd = re.search("getcwd\(\"(.*?)\"", line);
        if pid and cwd:
            pid2cwd[pid.group(0)] = cwd.group(1);

        includes = re.findall(r"(-I.*?)\"\,", line);
        if(includes):
            pid = re.search("^\d+", line).group(0);
            includesList.append((pid, includes));

filename = './test';
with open(filename, 'r') as f:
    doAnalysis(f);


regex = re.compile("^-I\.\.");
finalList = [];
for pid,includes in includesList:
    if pid in pid2cwd:
        cwd = pid2cwd[pid];
        for include in includes:
            finalList.append(regex.sub("-I" + cwd + "/..", include));


myset = set(finalList);
for i in myset:
    print i;
