# Nexss Programmer package: Audio/Split
# Uses great spleeter (MIT License) https://github.com/deezer/spleeter

import platform
import json
import sys
import io
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # 0,1,2,3

import pip
pip.main(["install", "spleeter"])

sys.path.append(os.path.join(os.getenv(
    "NEXSS_PACKAGES_PATH"), "Nexss", "Lib"))

from NexssLog import nxsInfo, nxsOk, nxsWarn, nxsError

# STDIN
NexssStdin = sys.stdin.read()

parsedJson = json.loads(NexssStdin)

if "nxsIn" in parsedJson.keys():
    parsedJson['_file'] = parsedJson['nxsIn'][0]

# print(parsedJson['_file'])
# sys.exit(1)

# parsedJson['_file'] = "squidGame-test.wav"
if "_file" in parsedJson.keys():
    _file_to_separate = os.path.abspath(os.path.join(
        parsedJson["cwd"], parsedJson["_file"]))

    if not os.path.exists(_file_to_separate):
        nxsError('File does not exist: ' + _file_to_separate)
        sys.exit(1)

    _folder = parsedJson["cwd"]
    if "_folder" in parsedJson.keys():
        _folder = parsedJson["_folder"]

    _option = 2
    if "_option" in parsedJson.keys():
        _option = parsedJson["_option"]

    SEPARATION_OPTIONS = {
        2: 'spleeter:2stems',
        4: 'spleeter:4stems',
        5: 'spleeter:5stems',
    }

    if not _option in SEPARATION_OPTIONS:
        nxsError('option: ' + str(_option) + 'is not valid')
        nxsInfo('Available options for number of tracks:\n' +
                ', '.join(map(str, SEPARATION_OPTIONS)))
        sys.exit(1)
    else:
        _selected_option = SEPARATION_OPTIONS[_option]

        nxsInfo('Selected option: ' + _selected_option)

        import tensorflow as tf

        from spleeter import SpleeterError
        from spleeter.audio.adapter import AudioAdapter
        from spleeter.separator import Separator
    # MODEL_TO_INST = {
    #     'spleeter:2stems': ('vocals', 'accompaniment'),
    #     'spleeter:4stems': ('vocals', 'drums', 'bass', 'other'),
    #     'spleeter:5stems': ('vocals', 'drums', 'bass', 'piano', 'other'),
    # }

    # print("RUNNING TESTS WITH TF VERSION {}".format(tf.__version__))

        adapter = AudioAdapter.default()
        waveform, _ = adapter.load(_file_to_separate)

        if 1:
            separator_lib = Separator(
                _selected_option, stft_backend="librosa", multiprocess=False)
            out_lib = separator_lib._separate_librosa(
                waveform, _file_to_separate)
        else:
            separator_tf = Separator(
                _selected_option, stft_backend="tensorflow", multiprocess=False)

        prediction = separator_lib.separate(waveform, _file_to_separate)

        separator_lib.separate_to_file(
            _file_to_separate,
            _folder)

        # Attach created files as output

        name = os.path.splitext(os.path.basename(_file_to_separate))[0]
        output = []
        for instrument in out_lib.keys():
            output.append(os.path.join(name, instrument + ".wav"))
        parsedJson['nxsOut'] = output

        del parsedJson['nxsIn']
else:
    nxsError('No file selected.')
    sys.exit(1)

NexssStdout = json.dumps(parsedJson, ensure_ascii=False).encode(
    'utf8', 'surrogateescape')
# STDOUT
print(NexssStdout.decode('utf8', 'surrogateescape'))
