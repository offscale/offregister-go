from fabric.operations import run
from offregister_fab_utils.fs import append_path, cmd_avail
from patchwork.files import append


def install0(arch="amd64", *args, **kwargs):
    version = kwargs.get("GOVERSION", "1.12.9")

    if cmd_avail(c, "go"):
        current_version = (
            c.run("go version", hide=True)
            .stdout.rpartition(" ")[0]
            .rpartition(" ")[2][2:]
        )
        if current_version == version:
            return "Go {current_version} already installed".format(
                current_version=current_version
            )

    go_path = kwargs.get("GOPATH", c.run("echo $HOME/go", hide=True).stdout.rstrip())
    install_loc = "/usr/local"
    go_tar = "go{version}.{os}-{arch}.tar.gz".format(
        version=version, os="linux", arch=arch
    )

    c.run(
        "curl -O https://storage.googleapis.com/golang/{go_tar}".format(go_tar=go_tar)
    )
    c.sudo(
        "tar -C {install_loc} -xzf {go_tar}".format(
            install_loc=install_loc, go_tar=go_tar
        )
    )
    append_path(
        c,
        "{install_loc}/go/bin:{go_path}/bin".format(
            install_loc=install_loc, go_path=go_path
        ),
    )
    append(
        "/etc/environment", "GOPATH={go_path}".format(go_path=go_path), use_sudo=True
    )
    c.run("rm {go_tar}".format(go_tar=go_tar))
    # c.run('rm -rf go*')
    c.run("mkdir -p {go_path}{subdirs}".format(go_path=go_path, subdirs="/{bin,src}"))
    return "Installed:{}".format(run("go version", hide=True).stdout)
