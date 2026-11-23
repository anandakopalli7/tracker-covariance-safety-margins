"""LOCAL STAND-IN for `omegaconf` (not installed on this laptop). Import-only: canmot.config_resolvers registers two
resolvers at import time; the tracker path never reads an OmegaConf object (the tracker config is a plain dict)."""


class OmegaConf:
    _resolvers = {}

    @classmethod
    def has_resolver(cls, name):
        return name in cls._resolvers

    @classmethod
    def register_new_resolver(cls, name, resolver, **kwargs):
        cls._resolvers[name] = resolver


class DictConfig(dict):
    pass
