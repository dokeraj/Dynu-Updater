from dataclasses import dataclass
import sys
from environs import Env

@dataclass
class EnvVars:
    username: str
    password: str
    hostnames: str
    dynuUpdateUrl: str
    ipSource: str
    refreshTime: float


# READ THE ENV VARS:
def read_envs():
    try:
        env = Env()
        USERNAME = env('USERNAME')
        PASSWORD = env('PASSWORD')
        HOSTNAMES = env('HOSTNAMES')
        DYNU_UPDATE_URL = env('DYNU_UPDATE_URL', "https://api.dynu.com/nic/update")
        IP_SOURCES = env('IP_SOURCES', "https://api.ipify.org?format=json")
        REFRESH_TIME = env.float('REFRESH_TIME', 300)

        print(f"The following env vars have been set:\n- USERNAME: {USERNAME}\n- PASSWORD: {PASSWORD}\n- HOSTNAMES: {HOSTNAMES}\n- DYNU_UPDATE_URL: {DYNU_UPDATE_URL}\n- IP_SOURCES: {IP_SOURCES}\n- REFRESH_TIME: {REFRESH_TIME}\n\n")
        return EnvVars(USERNAME, PASSWORD, HOSTNAMES, DYNU_UPDATE_URL, IP_SOURCES, REFRESH_TIME)
    except Exception as e:
        print(f"ERROR: one or more env vars were not properly set: {e}")
        sys.exit(1)
