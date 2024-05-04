import logging
import os
import sys
import argparse


def parse_arguments():
    """
    Parse command line arguments.

    Returns:
        bool: True if debug mode is enabled, False otherwise.
    """
    parser = argparse.ArgumentParser(description='My Application')
    parser.add_argument('--debug', action='store_true',
                        help='Enable debug mode')
    args = parser.parse_args()
    return args.debug


def setup_logging(debug_mode):
    """
    Set up logging configuration based on the debug mode.

    Parameters:
        debug_mode (bool): True if debug mode is enabled, False otherwise.

    The function sets up the logging configuration based on the debug mode. If debug mode is enabled, the logging level is set to DEBUG and the log messages will be displayed on the terminal. If debug mode is disabled, the log messages will be written to a log file named 'app_debug.log'.

    If debug mode is disabled, the function also creates a log directory based on the operating system. On Windows, the log directory is named 'logs', and on other operating systems, it is named '.logs'. The log directory is created if it does not exist.

    The function redirects the standard output and standard error to separate log files named 'my_stdout.log' and 'my_stderr.log' respectively, located in the log directory.

    Example usage:
        debug_mode = parse_arguments()
        setup_logging(debug_mode)
    """
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
