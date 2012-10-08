import re
from os.path import join, realpath, dirname
from fabric.api import cd, env, local, run, sudo, require, settings, abort
from fabric.decorators import task, roles
from fabric.contrib.console import confirm
from fabric.contrib.files import exists
from fabric.operations import _prefix_commands, _prefix_env_vars

env.proj_repo = 'git@github.com:katemsu/kate3.git'
env.proj_name = 'smizell'
env.config_root = join(realpath(dirname(__file__)), 'config')

# Placeholder roles so that using the -R option works
env.roledefs = {'app': [],
                'db': []}

ENVIRONMENTS = {
    'production': {
        'user': 'smizell',
        'roledefs': {
            'app': ['coekate.murraystate.edu'],
        },
    },
    'dev': {
        'roledefs': {
            'app': ['olivia.lincolnloop.com:9027'],
            'db': ['olivia.lincolnloop.com:9027'],
        },
        'root': '/opt/webapps/ginger.dev.lincolnloop.com',
        'proj_rev': 'origin/develop',
    },
}

DEFAULTS = {
    'root': '/web/projects/kate3base',
    'git_root': '/web/gitprojects/kate3',
    'proj_rev': 'origin/master',
}

# Default to all roles if no specific roles or hosts were specified
if not env.get('roles') and not env.get('hosts'):
    env.roles = env.roledefs.keys()


@task
def environment(name):
    """Environment selector"""
    env.update(dict(DEFAULTS, **ENVIRONMENTS[name]))
    env.name = name

    # Set dependent attributes
    env.proj_root = env.root + '/src/kate3'
    env.pip_file = env.git_root + '/requirements.pip'

    # Create a reverse map for roledefs
    env.role_for_host = {}
    if env.name == "test":
        # If this is the testserver, get the ip and generate roledefs
        ip = testserver.get_ip_address()
        env.roledefs = {'app': [ip], 'db': [ip]}
        env.role_for_host[ip] = 'test'
    elif env.name == "sentry":
        # Handle sentry config
        env.roles = ['sentry']
        env.role_for_host[env.roledefs['sentry'][0]] = 'sentry'
    else:
        for role, hosts in env.roledefs.items():
            for host in hosts:
                env.role_for_host[host] = role


@task
def dev():
    """Shortcut for environment:dev"""
    return environment("dev")


@task
def production():
    """Shortcut for environment:production"""
    return environment("production")


@task
def test():
    """Shortcut for environment:test"""
    return environment("test")

@task
@roles('app')
def deploy(branch=None):
    """
    Update source, update pip requirements, collect static media, syncdb,
    restart server.

    Branches and individual commits can be deployed with::

        $ fab envname deploy:refname
    """
    update_code(branch)
    #update_reqs()
    syncdb()
    restart()


@task
@roles('app')
def update():
    """Update source and collect static media"""
    update_code()
    collectstatic()


@task
@roles('app')
def version():
    """Show last commit to repo on server"""
    with cd(env.git_root):
        sshagent_run('git log -1')


@task
@roles('app')
def restart():
    """Restart Apache or Gunicorn process"""
    if env.name == 'dev':
        run('touch %s/etc/apache/django.wsgi' % env.root)
    else:
        sudo('/etc/init.d/kate3 restart')


@task
@roles('app')
def update_reqs():
    """Update pip requirements"""
    if env.name == 'dev':
        run('sudo chmod -R g+w {env.root}'.format(env=env))
    ve_run('yes w | pip install -r %s' % env.pip_file)

@task
@roles('app')
def update_code(branch=None):
    """Updates project source"""
    if not branch:
        branch = env.proj_rev
    #with cd(env.proj_root):
    #    # Clean .pyc files
    #    run('find . -name *.pyc -delete')
    with cd(env.git_root):
        sshagent_run('git pull')
        #sshagent_run('git checkout %s' % branch)


@task
@roles('app')
def syncdb():
    """Run syncdb (along with any pending south migrations)"""
    ve_run('{env.proj_root}/manage.py syncdb --migrate --noinput'.format(env=env))

@task
@roles('app')
def collectstatic():
    with cd("%s/kate3" % env.proj_root):
        ve_run("compass compile")
        ve_run("{env.proj_root}/manage.py collectstatic --noinput".format(env=env))

@task
@roles('app')
def gunicorn_log(lines=30):
    """Tail the Django Log"""
    log_file = "/var/log/gunicorn/kate3.log"
    sudo("tail -n{lines} {file}".format(lines=lines, file=log_file))

@task
@roles('app')
def access_log(lines=30):
    """Tail the Django Log"""
    log_file = "/var/log/httpd/access_log"
    sudo("tail -n{lines} {file}".format(lines=lines, file=log_file))

@task
@roles('app')
def error_log(lines=30):
    """Tail the Django Log"""
    log_file = "/var/log/httpd/error_log"
    sudo("tail -n{lines} {file}".format(lines=lines, file=log_file))


@task
@roles('app')
def backup(options='-u'):
    """
    Backup the database.  Pass options for the backup like this::

        $ fab backup:"-u -f /tmp/mybackup.dump.gz.gpg -k"

    If no options are provided, it defaults to -u to upload the backup to
    Cloud Files.
    """
    ve_run("manage.py backup %s" % options)


@task
@roles('app')
def list_backups(options=''):
    """List backups"""
    ve_run("manage.py list_backups %s" % options)


@task
@roles('app')
def restore(options=''):
    """
    Restore the latest db backup, or provide specific restore options like
    this::

        $ fab restore:"-d secondary-db my-db-name.2011-12-06.1005.dump.gz.gpg"
    """
    if 'production' in env.roles:
        abort("This command cannot be used with the production environment.")

    # Restart postgres to eject any other users accessing the database
    if not env.name == 'dev':
        sudo('/etc/init.d/postgresql restart')

    with settings(warn_only=True):
        ve_run("manage.py restore %s" % options)


@task
@roles('app')
def ve_run(cmd):
    """
    Helper function.
    Runs a command using the virtualenv environment
    """
    require('root')
    return sshagent_run('source %s/bin/activate; %s' % (env.root, cmd))

def sshagent_run(cmd):
    """
    Helper function.
    Runs a command with SSH agent forwarding enabled.

    Note:: Fabric (and paramiko) can't forward your SSH agent.
    This helper uses your system's ssh to do so.
    """
    # Handle context manager modifications
    wrapped_cmd = _prefix_commands(_prefix_env_vars(cmd), 'remote')
    try:
        host, port = env.host_string.split(':')
        return local(
            "ssh -p %s -A %s@%s '%s'" % (port, env.user, host, wrapped_cmd)
        )
    except ValueError:
        return local(
            "ssh -A %s@%s '%s'" % (env.user, env.host_string, wrapped_cmd)
        )