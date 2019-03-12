import re

with open('课堂笔记.sql', 'rb') as source:
    with open('01-practice.sql', 'w') as target:
        line = source.readline().decode('utf-8')
        while line:
            if re.match(r'.*--.*', line):
                target.write(line)
            line = source.readline().decode('utf-8')


