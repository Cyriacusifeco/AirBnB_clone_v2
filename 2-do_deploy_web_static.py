#!/usr/bin/python3

from fabric.api import env, put, run, sudo
import os

env.use_ssh_config = True
env.user = 'ubuntu'
env.hosts = ['54.237.124.196', '34.207.83.120']


def do_deploy(archive_path):
    """Distribute an archive to web servers"""
    if not os.path.exists(archive_path):
        print("Archive not found")
        return False
    try:
        archive_name = os.path.basename(archive_path)
        archive_base = os.path.splitext(archive_name)[0]
        remote_path = "/tmp/{}".format(archive_name)
        # Upload archive to /tmp/ directory of web server
        put(archive_path, remote_path)
        # Create the directory /data/web_static/releases/<archive
        # filename without extension>
        remote_release_dir =\
            "/data/web_static/releases/{}".format(archive_base)
        sudo("mkdir -p {}".format(remote_release_dir))
        # Uncompress archive to the created directory
        sudo(
            "tar -xzf {} -C {} --strip-components 1"
            .format(remote_path, remote_release_dir))
        # Delete the archive from the web server
        sudo("rm {}".format(remote_path))
        # Remove old symbolic link
        sudo("rm -f /data/web_static/current")
        # Create new symbolic link
        sudo("ln -s {} /data/web_static/current".format(remote_release_dir))
        print("New version deployed!")
        return True
    except Exception as e:
        print("Deployment failed: {}".format(e))
        return False
