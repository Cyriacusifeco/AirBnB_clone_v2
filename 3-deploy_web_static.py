#!/usr/bin/python3
"""Fabric script that creates and distributes an archive to web servers."""
import os
from fabric.api import env, put, run, local
from datetime import datetime

env.hosts = ['54.237.124.196', '34.207.83.120']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


def do_pack():
    """Creates an archive of the web_static folder."""
    now = datetime.now().strftime('%Y%m%d%H%M%S')
    local('mkdir -p versions')
    filename = 'versions/web_static_{}.tgz'.format(now)
    result = local('tar -cvzf {} web_static'.format(filename))
    if result.succeeded:
        return filename
    else:
        return None


def do_deploy(archive_path):
    """Distributes an archive to web servers."""
    if not os.path.exists(archive_path):
        return False
    filename = archive_path.split("/")[-1]
    path_no_ext = "/data/web_static/releases/" + filename.split(".")[0]
    put(archive_path, "/tmp/")
    run("sudo mkdir -p {}".format(path_no_ext))
    run("sudo tar -xzf /tmp/{} -C {}".format(filename, path_no_ext))
    run("sudo rm /tmp/{}".format(filename))
    run("sudo mv {}/web_static/* {}/".format(path_no_ext, path_no_ext))
    run("sudo rm -rf {}/web_static".format(path_no_ext))
    run("sudo rm -rf /data/web_static/current")
    run("sudo ln -s {} /data/web_static/current".format(path_no_ext))


def deploy():
    """Creates and distributes an archive to web servers."""
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
