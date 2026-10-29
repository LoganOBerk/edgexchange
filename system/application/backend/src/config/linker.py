from .environment import Environment as env
from procurement import LiveCache
from integration import SessionCache
from persistence import AccountRepository

from functools import cached_property

class Cache:
    @cached_property
    def lc(self): return LiveCache(env.lc_src())

    @cached_property
    def sc(self): return SessionCache(env.sc_src())

class Database:
    @cached_property
    def acc(self): return AccountRepository(env.db_src())

class Config:
    @cached_property
    def ao(self): return env.ao_cfg()
