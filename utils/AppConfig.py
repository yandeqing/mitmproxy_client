import os
import codecs
import configparser

# configPath = FilePathUtil.get_full_dir('config', "test_config.ini")
from utils import FilePathUtil

configPath = FilePathUtil.get_or_create_full_dir('config', "config.ini")


class ShareConfig:
    def __init__(self):
        fd = open(configPath, encoding="utf-8")
        data = fd.read()
        #  remove BOM
        if data[:3] == codecs.BOM_UTF8:
            data = data[3:]
            file = codecs.open(configPath, "w", encoding="utf-8")
            file.write(data)
            file.close()
        fd.close()
        self.cf = configparser.ConfigParser()
        self.cf.read(configPath, encoding="utf-8")

    def get_value(self, section, name):
        if not self.cf.has_section(section):
            return None
        if not self.cf.has_option(section, name):
            return None
        value = self.cf.get(section, name)
        return value

    def set_value(self, section, name, value):
        if not self.cf.has_section(section):
            self.cf.add_section(section)
        self.cf.set(section, name, value)
        with open(configPath, 'w+') as f:
            self.cf.write(f)
            f.close()

    def get_setting(self, name):
        return self.get_value("SETTING", name)

    def set_setting(self, name, value):
        self.set_value("SETTING", name, value)


if __name__ == '__main__':
    # FilePathUtil.get_or_create_full_dir('config', "config.ini")
    monitor_config = ShareConfig()
    # monitor_config.set_setting("phone","232323")
    # monitor_config.set_setting("username","232323")
    # monitor_config.set_setting("id","232323")
    setting = monitor_config.get_setting("phone1")
    print(setting == None)
