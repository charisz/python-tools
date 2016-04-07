import os
import abc

class ConfigLoaderException(Exception):
    pass

class ConfigFormatter(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def encode(self, data):
        """
            Args:
                data: any serializable python type

            Returns:
                The encoded string data
        """
        pass

    @abc.abstractmethod
    def decode(self, data):
        """
            Args:
                data (str): the raw data from the file

            Returns:
                Dict, list or any serializable python type
        """
        pass

class ConfigLoader(object):
    """
        Args:
            formatter (ConfigFormatter): config encode/decode interface instance
            base_path (str): a custom path which may be contains the config
    """
    def __init__(self, formatter, base_path):
        self.sources = [
            os.path.dirname(os.getcwd()),
            os.path.dirname(os.path.abspath(base_path)),
            os.path.expanduser('~'),
            '/etc',
        ]
        self.__loaded_config_file = None
        self.__formatter = formatter

    @property
    def filename(self):
        return self.__loaded_config_file

    def load(self, filename, create = None, default_conf = {}):
        """Load the config file

        Args:
            filename (str): the filename of the config, without any path
            create (Optional[str]): if the config file not found, and this parameter is not None, a config file will be create with content of default_conf
            default_conf (Optional[dict]): content of the default config data

        Returns:
            Return value of the ConfigFormatter.decode or the default_conf value

        Raises:
            ConfigLoaderException: if the config file not found

        """
        tries = []
        for source in self.sources:
            file_path = os.path.join(source, filename)
            tries.append(file_path)
            if not os.path.exists(file_path):
                continue
            self.__loaded_config_file = file_path
            with open(file_path) as f:
                return self.__formatter.decode(f.read())

        if create is not None:
            self.__loaded_config_file = os.path.join(create, filename)
            self.save(default_conf)
            return default_conf

        raise ConfigLoaderException("Config file not found in: %s" % tries)

    def save(self, data):
        """Save the config data

        Args:
            data: any serializable config data

        Raises:
            ConfigLoaderException: if the ConfigLoader.load not called, so there is no config file name, or the data is not serializable

        """
        if self.__loaded_config_file is None:
            raise ConfigLoaderException("Load not called yet!")

        try:
            with open(self.__loaded_config_file, 'w') as f:
                f.write(self.__formatter.encode(data))
        except Exception as e:
            raise ConfigLoaderException("Config data is not serializable: %s" % e)