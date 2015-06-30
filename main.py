__author__ = 'qqibrow'
import re
import sys
from pprint import pprint

def getPid2CmdTable(lines):
    pid2cwd = {};
    for line in lines:
        pid = re.search("^\d+", line);
        cwd = re.search("getcwd\(\"(.*?)\"", line);
        if pid and cwd:
            pid2cwd[pid.group(0)] = cwd.group(1);
    return pid2cwd;

# return [(pid, [include])]
def getPidWithIncludeList(lines):
    includesList = [];
    for line in lines:
        includes = re.findall(r"(-I.*?)\"\,", line);
        if(includes):
            pid = re.search("^\d+", line).group(0);
            includesList.append((pid, includes));
    return includesList;


def Init(filename):
    lines = sys.stdin.readlines();
    pid2cmd = getPid2CmdTable(lines);
    pidIncludeList = getPidWithIncludeList(lines);
    return pid2cmd, pidIncludeList;

filename = './test';

pid2cmd, pidIncludeList = Init(filename);
regex = re.compile("^-I\.\.");
includesWithAbsPath = set();
for pid,includes in pidIncludeList:
    if pid in pid2cmd:
        cwd = pid2cmd[pid];
        for include in includes:
            includesWithAbsPath.add(regex.sub("-I" + cwd + "/..", include));

for include in includesWithAbsPath:
    print include;
