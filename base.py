import re
import logging
from shutil import copyfile

from utils import get_file_lines

class HostsFile(object):

    def __init__(self, path="/etc/hosts"):
        self.path = path

        self._lines = self.parse_hosts_file(self.path)

    @property
    def lines(self):
        return [self.join_hosts_line(line) for line in self._lines]

    def write(self, path, backup=None):
        "Write out the hosts file to a path"

        if backup:
            copyfile(path, backup)

        with open(path, "w") as file:
            for line in self.lines:
                file.write(line + "\n")

    def host_exists(self, host):
        "Check if a host exists within an array of /etc/hosts lines"

        for line in self._lines:
            
            if isinstance(line, list):
                if line[1] == host:
                    return True

        return False


    def add_host(self, host, ip_address):
        "Add new hosts to a list if it doesn't already exist"

        if self.host_exists(host):
            logging.warning("'%s' already exists in %s, skipping", host, self.path)
            return False

        self._lines.append([ip_address, host])
        return True


    @classmethod
    def parse_hosts_file(cls, path):
        "Parse a hosts file ``path`` and return a list of lines"
        return [cls.parse_hosts_line(line) for line in get_file_lines(path)]

    @classmethod
    def parse_hosts_line(cls, line):
        "Split an /etc/hosts line into manageable parts"
        if line.startswith("#"):
            return line

        return re.split("\s+", line)

    @classmethod
    def join_hosts_line(cls, line):
        "Combine an /etc/hosts line back into the proper format"

        if isinstance(line, basestring) and line.startswith("#"):
            return line

        return "\t".join(line)
