import logging
import os
import sys
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description='My Application')
    parser.add_argument('--debug', action='store_true',
                        help='Enable debug mode')
    args = parser.parse_args()
    return args.debug


def setup_logging(debug_mode):
    if debug_mode:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(filename='app_debug.log', level=logging.DEBUG)

    logging.debug('This message will go to the debug log file or terminal')

    if not debug_mode:
        if os.name == 'nt':
            logs_folder = 'logs'
        else:
            logs_folder = '.logs'

        application_path = os.path.dirname(
            sys.executable if getattr(sys, 'frozen', False) else __file__)
        log_dir = os.path.join(application_path, logs_folder)

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        stdout_log_path = os.path.join(log_dir, 'my_stdout.log')
        stderr_log_path = os.path.join(log_dir, 'my_stderr.log')

        sys.stdout = open(stdout_log_path, 'w')
        sys.stderr = open(stderr_log_path, 'w')
