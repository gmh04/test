from edina.admin import Fabric
from fabric.api import cd, env, hosts, run

from fabric.contrib.project import rsync_project

import os

def install_dev():
    """Set up DEV environment"""
    Fabric('news').install('newssrv')

@hosts('ghamilt2@devel.edina.ac.uk')
def install_beta():
    """Set up BETA environment"""
    Fabric('news').install('newssrv')

@hosts('gmh04@ec2-176-34-202-77.eu-west-1.compute.amazonaws.com')
def install_live():
    """Set up LIVE environment"""
    env.key_filename = '/home/george/.ssh/gmh04.pem'
    Fabric('news').install('newssrv')

@hosts('ghamilt2@devel.edina.ac.uk')
def deploy_beta():
    """Deploy BETA server"""
    Fabric('news').deploy('newssrv')

@hosts('gmh04@ec2-46-137-0-34.eu-west-1.compute.amazonaws.com')
def deploy_live():
    """Release LIVE server"""
    env.key_filename = os.sep.join((os.environ['HOME'], '.ssh', 'gmh04.pem'))
    Fabric('news', apache_dir='/etc/init.d/apache2').deploy('newssrv')

@hosts('gmh04@ec2-176-34-202-77.eu-west-1.compute.amazonaws.com')
def restore():
    Fabric('news').restore('newssrv')

@hosts('gmh04@ec2-46-137-0-34.eu-west-1.compute.amazonaws.com')
def upgrade_database():
    fab = Fabric('news')
    appdir = os.sep.join((fab.proj_dir, 'newssrv'))
    with cd(appdir):
        # save current data
        tmp = os.sep.join((run('echo $HOME'), 'tmp/'))
        fab.venvremote('%s/manage.py newssavesources' % appdir)
        run('cp %s %s' % (os.sep.join((appdir, 'initial_data.json')) , tmp))

        # drop tables
        fab.venvremote('./manage.py sqlclear feeds | ./manage.py dbshell')

        # deploy latest
        deploy_live()

        # restore database
        run('cp %s .' % os.sep.join((tmp, 'initial_data.json')))
        fab.venvremote('./manage.py syncdb')
        fab.venvremote('./manage.py newsfetchfeeds')
