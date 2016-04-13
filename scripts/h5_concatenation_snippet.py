import h5py
import numpy as np
import os

def hdf5_cancate(hdf5_files, output, verbose=False):
    # the file list
    filenamelist = hdf5_files

    # get data from exisitng files
    statesdata=[]
    actionsdata=[]
    meta=[]
    for filename in filenamelist:
        fileread  = h5py.File(filename, 'r')   # 'r' means that hdf5 file is open in read-only mode
        status=fileread['states']
        statesdata.append(status)
        actionsdata.append(fileread['actions'])
        meta.append(fileread['file_offsets'])

    # get the dimensions of the new file
    print(statesdata)
    statelen=0
    actionlen=0
    metalen=0
    for i in range(0, len(statesdata)):
        statelen = statelen+statesdata[i].shape[0]
        actionlen = actionlen+actionsdata[i].shape[0]
        metalen = metalen+len(meta[i])

    # initialise the output
    tmp_file = os.path.join(os.path.dirname(output), ".tmp." + os.path.basename(output))
    combined = h5py.File(tmp_file, 'w')   
    states = combined.create_dataset(
                    'states',
                    dtype=np.uint8,
                    shape=(statelen, statesdata[0].shape[1], statesdata[0].shape[2], statesdata[0].shape[3]),
                    chunks=(64, statesdata[0].shape[1], statesdata[0].shape[2], statesdata[0].shape[3]),      # approximately 1MB chunks
                    compression="lzf")
    actions = combined.create_dataset(
                    'actions',
                    dtype=np.uint8,
                    shape=(actionlen, 2),
                    chunks=(64, 2),
                    compression="lzf")
    offsets = combined.create_group('offsets')

    # putting the data from separate file to the inialisation
    start = 0
    summation = 0
    for i in range(0, len(statesdata)):
        # put the states and actions to the inialisation
        end = start + statesdata[i].shape[0]
        metadata = meta[i]

        states[start:end] = statesdata[i]
        actions[start:end] = actionsdata[i]

        start += statesdata[i].shape[0]

        # put the file_offsets to the inialisation, with the total off_sets calculated
        for keyitem,valueitem in metadata.iteritems():
            offsets[keyitem] = [summation, valueitem.value[1]]
            summation=summation+valueitem.value[1]
    combined.close()
    os.rename(tmp_file, output)

def run_cancat(cmd_line_args=None):
    """Run cancatenations. command-line args may be passed in as a list
    """
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description='Cancatenate the generated hdf5 files',
        epilog="A directory containing the hdf5 files is needed")
    parser.add_argument("--outfile", "-o", help="Destination to write data (hdf5 file)", required=True)
    parser.add_argument("--recurse", "-R", help="Set to recurse through directories searching for SGF files", default=False, action="store_true")
    parser.add_argument("--directory", "-d", help="Directory containing SGF files to process. if not present, expects files from stdin", default=None)
    parser.add_argument("--verbose", "-v", help="Turn on verbose mode", default=False, action="store_true")

    if cmd_line_args is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(cmd_line_args)

    if args.verbose:
        print "directory", args.directory

    def _is_hdf5(fname):
        return fname.strip()[-5:] == ".hdf5"

    def _walk_all_hdf5s(root):
        """a helper function/generator to get all hdf5 files in subdirectories of root
        """
        for (dirpath, dirname, files) in os.walk(root):
            for filename in files:
                if _is_hdf5(filename):
                    # yield the full (relative) path to the file
                    yield os.path.join(dirpath, filename)

    def _list_hdf5s(path):
        """helper function to get all hdf5 files in a directory (does not recurse)
        """
        files = os.listdir(path)
        return (os.path.join(path, f) for f in files if _is_hdf5(f))

    if args.directory:
        if args.recurse:
            files = list(_walk_all_hdf5s(args.directory))
        else:
            files = list(_list_hdf5s(args.directory))
    else:
        files = list((f.strip() for f in sys.stdin if _is_hdf5(f))) 

    if args.verbose:
        print "files", files

    hdf5_cancate(files, args.outfile, verbose=args.verbose)

if __name__ == '__main__':
    run_cancat()
