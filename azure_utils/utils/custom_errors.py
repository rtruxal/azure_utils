class ArgumentException(BaseException):
    pass

class ServicePrincipalGenericException(BaseException):
    pass

class ServicePrincipalParsingException(BaseException):
    pass

class ServicePrincipalAuthException(BaseException):
    pass

class JSONInfileConfigException(BaseException):
    pass

class JSONInfileParsingException(BaseException):
    pass

class READ_THE_DAMN_WARNING_FILE(BaseException):
    pass

class RTDWFITDD_messages:
    from os import linesep
    read_warning_is_false = \
        'Please be so kind as to read WARNING.txt. It can be located at `/path/to/python/env/Lib/<OS-SPECIFIC-PATH>/azure_utils/config/WARNING.txt.' \
        + linesep + \
        'If you are on *NIX, try running `find /path/to/python/env -type f -name "WARNING.txt'

    read_warning_is_true = \
        'Ok so you have found the credentials_config.json file. Congrats.' \
        + linesep + \
        "You've won....drumrollll......the right to read the WARNING.txt EXTREMELY CAREFULLY!!!" \
        + linesep + \
        'Wherever you found credentials_config.json, go back a dir (`cd ../`, hopefully a command you know) and you will find it.'
    @classmethod
    def read_warning_false(cls):
        return cls.read_warning_is_false

    @classmethod
    def read_warning_true(cls):
        return cls.read_warning_is_true