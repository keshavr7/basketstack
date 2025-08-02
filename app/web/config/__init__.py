import ast
import os


class Config:
    ENV_PREFIX = "DJANGO_"
    CONFIG_DIRS = ["/var/run/configs", "/var/run/secrets", "."]  # Added . for local .env support
    BOOL_TRUE = ["1", "true", "yes", "y"]

    def __init__(self):
        self.config = self.get_config()

    def __call__(self, key, default=None):
        return self.config.get(key, default)

    def bool(self, key, default=False):
        if key not in self.config:
            return default
        else:
            return str(self.config[key]).lower() in self.BOOL_TRUE

    def int(self, key, default=0):
        return int(self(key, default))

    def float(self, key, default: float = 0.0):
        return float(self(key, default))

    def dict(self, key, default=None):
        if default is None:
            default = {}
        if key not in self.config:
            return default
        if isinstance(self.config[key], dict):
            return self.config[key]
        return ast.literal_eval(self.config[key])

    def list(self, key, default=None):
        if default is None:
            default = []
        if key not in self.config:
            return default
        if isinstance(self.config[key], list):
            return self.config[key]
        return ast.literal_eval(self.config[key])

    def get_config(self):
        config = {}
        for config_dir in self.CONFIG_DIRS:
            if os.path.isdir(config_dir):
                for file in sorted(os.listdir(config_dir)):
                    config.update(self.get_file_as_dictionary(os.path.join(config_dir, file)))
        config.update(self.get_env_vars_as_dictionary())
        config.update(self.get_non_django_env_vars_as_dictionary())
        return config

    def get_file_as_dictionary(self, file_path):
        if not os.path.isfile(file_path):
            return {}
        with open(file_path) as fp:
            return {
                item[0].strip().strip('"'): item[1].strip().strip('"')
                for item in [
                    line.split("=", 1)
                    for line in fp
                    if "=" in line and not line.strip().startswith("#")
                ]
            }

    def get_env_vars_as_dictionary(self):
        return {
            k.replace(self.ENV_PREFIX, ""): v
            for k, v in os.environ.items()
            if k.startswith(self.ENV_PREFIX)
        }

    def get_non_django_env_vars_as_dictionary(self):
        return {k: v for k, v in os.environ.items() if not k.startswith(self.ENV_PREFIX)}


# Config class - initialize in settings.py
