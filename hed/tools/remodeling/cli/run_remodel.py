import os
import json
import argparse
from hed.errors.exceptions import HedFileError
from hed.tools.util.io_util import get_file_list, parse_bids_filename
from hed.tools.bids.bids_dataset import BidsDataset
from hed.tools.remodeling.dispatcher import Dispatcher
from hed.tools.remodeling.backup_manager import BackupManager


# def check_commands(commands):
#     """ Verify that the remodeling file is correct.
#
#     Args:
#         args (object
#
#     """
#
#     command_list, errors = Dispatcher.parse_commands(commands)
#     if errors:
#         raise ValueError("UnableToFullyParseCommands",
#                          f"Fatal command errors, cannot continue:\n{Dispatcher.errors_to_str(errors)}")
#     return
#


def get_parser():
    parser = argparse.ArgumentParser(description="Converts event files based on a json file specifying operations.")
    parser.add_argument("data_dir", help="Full path of dataset root directory.")
    parser.add_argument("-m", "--model-path", dest="model_path",
                        help="Full path of the file with remodeling instructions.")
    parser.add_argument("-t", "--task-names", dest="task_names", nargs="*", default=[], help="The name of the task.")
    parser.add_argument("-e", "--extensions", nargs="*", default=['.tsv'], dest="extensions",
                        help="File extensions to allow in locating files.")
    parser.add_argument("-x", "--exclude-dirs", nargs="*", default=[], dest="exclude_dirs",
                        help="Directories names to exclude from search for files.")
    parser.add_argument("-f", "--file-suffix", dest="file_suffix", default='events',
                        help="Filename suffix excluding file type of items to be analyzed (events by default).")
    parser.add_argument("-s", "--save-formats", nargs="*", default=['.json', '.txt'], dest="save_formats",
                        help="Format for saving any summaries, if any. If empty, then no summaries are saved.")
    parser.add_argument("-b", "--bids-format", action='store_true', dest="use_bids",
                        help="If present, the dataset is in BIDS format with sidecars. HED analysis is available.")
    parser.add_argument("-n", "--backup_name", default=BackupManager.DEFAULT_BACKUP_NAME, dest="backup_name",
                        help="Name of the default backup for remodeling")
    parser.add_argument("-v", "--verbose", action='store_true',
                        help="If present, output informative messages as computation progresses.")
    return parser


def parse_commands(arg_list=None):
    parser = get_parser()
    args = parser.parse_args(arg_list)
    if '*' in args.file_suffix:
        args.file_suffix = None
    if '*' in args.extensions:
        args.extensions = None
    args.data_dir = os.path.realpath(args.data_dir)
    args.exclude_dirs = args.exclude_dirs + ['remodel']
    args.model_path = os.path.realpath(args.model_path)
    if args.verbose:
        print(f"Data directory: {args.data_dir}\nCommand path: {args.json_remodel_path}")
    with open(args.model_path, 'r') as fp:
        commands = json.load(fp)
    command_list, errors = Dispatcher.parse_commands(commands)
    if errors:
        raise ValueError("UnableToFullyParseCommands",
                         f"Fatal command errors, cannot continue:\n{Dispatcher.errors_to_str(errors)}")
    return args, commands


def run_bids_ops(dispatch, args):
    bids = BidsDataset(dispatch.data_root, tabular_types=['events'], exclude_dirs=args.exclude_dirs)
    dispatch.hed_schema = bids.schema
    if args.verbose:
        print(f"Successfully parsed BIDS dataset with HED schema {str(bids.get_schema_versions())}")
    events = bids.get_tabular_group(args.file_suffix)
    if args.verbose:
        print(f"Processing ")
    for events_obj in events.datafile_dict.values():
        if args.task_names and events_obj.get_entity('task') not in args.task_names:
            continue
        sidecar_list = events.get_sidecars_from_path(events_obj)
        if sidecar_list:
            sidecar = events.sidecar_dict[sidecar_list[-1]].contents
        else:
            sidecar = None
        if args.verbose:
            print(f"Events {events_obj.file_path}  sidecar {sidecar}")
        df = dispatch.run_operations(events_obj.file_path, sidecar=sidecar, verbose=args.verbose)
        df.to_csv(events_obj.file_path, sep='\t', index=False, header=True)
    return


def run_direct_ops(dispatch, args):
    tabular_files = get_file_list(dispatch.data_root, name_suffix=args.file_suffix, extensions=args.extensions,
                                  exclude_dirs=args.exclude_dirs)
    if args.verbose:
        print(f"Found {len(tabular_files)} files with suffix {args.file_suffix} and extensions {str(args.extensions)}")
    for file_path in tabular_files:
        if args.task_names:
            (suffix, ext, entity_dict) = parse_bids_filename(file_path)
            task = entity_dict.get('task', None)
            if not (task and task in args.task_names):
                continue
        df = dispatch.run_operations(file_path, verbose=args.verbose)
        df.to_csv(file_path, sep='\t', index=False, header=True)
    return


def main(arg_list=None):
    args, commands = parse_commands(arg_list)
    if not os.path.isdir(args.data_dir):
        raise ValueError("DataDirectoryDoesNotExist", f"The root data directory {args.data_dir} does not exist")
    backup_man = BackupManager(args.data_dir)
    if not backup_man.get_backup(args.backup_name):
        raise HedFileError("BackupDoesNotExist", f"Backup {args.backup_name} does not exist. "
                           f"Please run_remodel_backup first", "")
    backup_man.restore_backup(args.backup_name, verbose=args.verbose)
    dispatch = Dispatcher(commands, data_root=args.data_dir, backup_name=args.backup_name)
    if args.use_bids:
        run_bids_ops(dispatch, args)
    else:
        run_direct_ops(dispatch, args)
    dispatch.save_context(args.save_formats)


if __name__ == '__main__':
    main()
