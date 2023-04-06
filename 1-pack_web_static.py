#!/usr/bin/python3
from fabric.api import local, env
from datetime import datetime
import os

env.user = 'ubuntu'
env.hosts = ['<your-server-ip-address>']


def do_pack():
    """Archive the contents of the web_static folder"""
    try:
        if not os.path.exists("./versions"):
            local("mkdir versions")
        now = datetime.now()
        time = now.strftime("%Y%m%d%H%M%S")
        file_name = "web_static_{}.tgz".format(time)
        local("tar -czvf versions/{} web_static".format(file_name))
        return os.path.abspath("versions/{}".format(file_name))
    except Exception as e:
        print("An error occured while packing the archive: {}".format(e))
        return None
