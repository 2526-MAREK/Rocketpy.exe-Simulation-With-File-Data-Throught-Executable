import configparser    

class dataFromParser(configparser.ConfigParser):
    Config  = configparser.ConfigParser()

    def configSectionMap(self, section):
        dict1 = {}
        options = self.Config.options(section)
        for option in options:
            try:
                dict1[option] = self.Config.get(section, option)
                if dict1[option] == -1:
                    print("skip: %s" % option)
            except:
                    print("exception on %s!" % option)
                    dict1[option] = None
            return dict1

    def openFileParser(self, fileini):
    #Config<configparser.ConfigParser instance at 0x00BA9B20>
        self.Config.read(fileini)
        self.Config.sections()       