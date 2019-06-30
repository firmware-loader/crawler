import requests
import re

filename = "E:\\Dokumente\\seafile\\Seafile\\Seafile\\Main\\Dokumente\\FH\\Bachelor\\commands\\avr_asm_links.txt"
words = re.compile(r"Words:\s?([0-9]+)")
cycles = re.compile(r"Cycles:\s?([0-9]+)")
name = re.compile(
    r"<h2(?:.*?)class=\"title\"(?:.*?)>\s?(?:.*?)\s?<a(?:.*?)\/>(?:.*?)\s?(?:.*?)<a\s(?:.*?)\/>(.*?)<\/abbr>",
    re.DOTALL)

session = requests.Session()
session.trust_env = False
unused_elements = []

with open(filename, "r") as fp:
    line = fp.readline()
    while line:
        headers = {'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                 "Chrome/75.0.3770.100 Safari/537.36"}
        r = session.get(line.strip(), headers=headers)

        if r.status_code == 200:
            wordCount = words.search(r.text)
            cycleCount = cycles.search(r.text)
            inName = name.search(r.text)
            if wordCount and cycleCount and inName:
                print("{\"",  inName.groups()[0].strip(), "\", {", wordCount.groups()[0].strip(), ", [](){return "
                                                                                              "std::size_t{",
                      cycleCount.groups()[0].strip(), "};} }}")
            else:
                unused_elements.append(line)
        line = fp.readline()
    print(unused_elements)
