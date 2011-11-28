from edina.admin import Fabric
from fabric.api import hosts, env

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

@hosts('gmh04@ec2-46-137-118-145.eu-west-1.compute.amazonaws.com')
def deploy_live():
    """Release LIVE server"""
    env.key_filename = '/home/george/.ssh/gmh04.pem'
    #Fabric('news', apache_dir='/etc/init.d/apache2').release('newssrv', do_django_tests=True)
    Fabric('news', apache_dir='/etc/init.d/apache2').deploy('newssrv')

@hosts('gmh04@ec2-46-137-118-145.eu-west-1.compute.amazonaws.com')
def deploy_site_live():
    Fabric('news').deploy_site()

    #htdocs = os.sep.join((self.target_dir, 'www', 'htdocs'))
    #with cd(htdocs):
      #      rsync_project(htdocs, 'site/')

@hosts('gmh04@ec2-176-34-202-77.eu-west-1.compute.amazonaws.com')
def restore():
    Fabric('news').restore('newssrv')
