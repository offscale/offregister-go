from fabric.contrib.files import append
from fabric.operations import run, sudo

from offregister_fab_utils.fs import append_path, cmd_avail


def install0(arch='amd64', *args, **kwargs):
    version = kwargs.get('GOVERSION', '1.11.1')

    if cmd_avail('go'):
        current_version = run('go version', quiet=True).rpartition(' ')[0].rpartition(' ')[2][2:]
        if current_version == version:
            return 'Go {current_version} already installed'.format(current_version=current_version)

    go_path = kwargs.get('GOPATH', run('echo $HOME/go', quiet=True))
    install_loc = '/usr/local'
    go_tar = 'go{version}.{os}-{arch}.tar.gz'.format(version=version, os='linux', arch=arch)

    run('curl -O https://storage.googleapis.com/golang/{go_tar}'.format(go_tar=go_tar))
    sudo('tar -C {install_loc} -xzf {go_tar}'.format(install_loc=install_loc, go_tar=go_tar))
    append_path('{install_loc}/go/bin:{go_path}/bin'.format(install_loc=install_loc, go_path=go_path))
    sudo("sed -i '0,/can/{//d}' /etc/environment")
    append('/etc/environment', 'GOPATH={go_path}'.format(go_path=go_path), use_sudo=True)
    run('rm {go_tar}'.format(go_tar=go_tar))
    # run('rm -rf go*')
    run('mkdir -p {go_path}{subdirs}'.format(go_path=go_path, subdirs='/{bin,src}'))
    return 'Installed:{}'.format(run('go version', quiet=True))
