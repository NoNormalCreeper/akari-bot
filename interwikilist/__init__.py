from configparser import ConfigParser
import sys
def iwlist():
    cp = ConfigParser()
    cp.read("interwikilist\list.cfg")
    section = cp.sections()[0]
    return(cp.options(section))

def iwlink(iw):
    cp = ConfigParser()
    cp.read("interwikilist\list.cfg")
    section = cp.sections()[0]
    return(cp.get(section,iw))