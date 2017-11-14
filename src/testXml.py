import xml.etree.ElementTree
import re

_file=open(r'F:\\InterfaceTest\\build.xml',"r")

search_str="(<target name=\"report\">)([\s\S]*?)(</target>)"

search_reults=re.search(search_str,_file.read())

_file.close()

print search_reults.group(0)