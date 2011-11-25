from edina.admin import Fabric
from fabric.api import hosts

def install_dev():
    """Set up DEV environment"""
    Fabric('news').install('newssrv')

@hosts('ghamilt2@devel.edina.ac.uk')
def install_beta():
    """Set up BETA environment"""
    Fabric('news').install('newssrv')

@hosts('ghamilt2@devel.edina.ac.uk')
def deploy_server_live():
    """Release LIVE server"""
    Fabric('news').release('newssrv', do_django_tests=True)
