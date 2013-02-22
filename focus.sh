#!/bin/bash
#
# Focus
#
# A simple script to add hostnames in $HOME/.focus to your /etc/hosts file
# under the host name 127.0.0.1 so you can't visit them....so you focus :)
#

focus() {
    backup_hosts_file && add_hosts_line && echo "Focusing...go be productive!"
}

unfocus() {
    backup_hosts_file && delete_hosts_line && echo "Unfocusing..were you productive?"
}

backup_hosts_file() {
    sudo cp /etc/hosts /etc/hosts.bak
}

add_hosts_line() {
    sudo -s "echo $(hosts_line) >> /etc/hosts"
}

delete_hosts_line() {
    sudo -s "sed '/focus_activation_host/d' /etc/hosts.bak > /etc/hosts"
}

hosts_line() {
    echo "127.0.0.1 $(focus_hosts) focus_activation_host"
}

focus_hosts() {
    cat $HOME/.focus | while read host; do
        echo -n " $host www.$host";
    done
}