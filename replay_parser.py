'''
------------------------------------------------------------------------------------------------
Author: @Demorf

Based on the work of @Isaac at https://forum.c1games.com/
https://github.com/idraper/terminal_flip_replay

Copyright: CC0 - completely open to edit, share, etc
------------------------------------------------------------------------------------------------
'''

import argparse
import json


def parse_args():
    ap = argparse.ArgumentParser(add_help=False, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument('-h', '--help', action='help', help='show this help message and exit\n\n')
    ap.add_argument('-f', '--flip', action='store_true', default=False, help='flip P1 and P2 turnss\n\n')
    ap.add_argument('-t', '--turns', action='append', type=int, help='filter only specific turn(can be used multiple times)\n\n')
    ap.add_argument('-n', '--no_frames', action='store_true', help='filter frames info')
    ap.add_argument('-s', '--suffix', default='_', help='suffix for the output file)\n\n')
    ap.add_argument(
        'files',
        nargs='+',
        default=[],
        help="specify a replay file (or multiple) you'd like to analyze\n\n")
    return vars(ap.parse_args())


def flip_vert(point):
    return [27 - point[0], 27 - point[1]]


def process_line(i, original, flip=False, turns=None, frames=True, sort=True):
    data = json.loads(original)

    if 'turnInfo' in data.keys():
        # skip frame rows
        if frames is False and data['turnInfo'][0] == 1:
            return ''

        if turns and data['turnInfo'][1] not in turns:
            return ''

    result = original
    if flip:
        result = flip_line(i, original)

    if sort:
        result = sort_data(result)

    return result + '\n'


def sort_data(original):
    data = json.loads(original)
    keys = ['turnInfo', 'p1Stats', 'p1Units', 'player1', 'p2Stats', 'p2Units', 'player2', 'events', 'endStats']

    sorted_data = {}
    for key in keys:
        if key in data:
            sorted_data[key] = data[key]

    sorted_data.update(data)
    return json.dumps(sorted_data, separators=(',', ':'))


def flip_line(i, original):
    keywords = ['p1Units', 'p1Stats', 'player1']

    for p1key in keywords:
        p2key = p1key.replace('1', '2')

        p1index = original.find(p1key)
        p2index = original.find(p2key)

        if (p1index != -1):
            original = original[:p1index] + p2key + original[p1index + len(p2key):]
        if (p2index != -1):
            original = original[:p2index] + p1key + original[p2index + len(p1key):]

    data = json.loads(original)

    if 'events' in data.keys():
        for event_type in data['events']:
            for unit in data['events'][event_type]:
                uPos = -1 if event_type != 'death' else -2
                unit[uPos] = 1 if unit[uPos] == 2 else 2
                unit[0] = flip_vert(unit[0])
                if event_type == 'selfDestruct':
                    for u in unit[1]:
                        u = flip_vert(u)
                elif event_type == 'shield' or \
                        event_type == 'move' or \
                        event_type == 'attack':
                    unit[1] = flip_vert(unit[1])

    if 'p1Units' in data.keys():
        for units in data['p1Units']:
            for unit in units:
                unit[0], unit[1] = flip_vert(unit[:2])
        for units in data['p2Units']:
            for unit in units:
                unit[0], unit[1] = flip_vert(unit[:2])

    if 'endStats' in data.keys():
        data['endStats']['winner'] = 1 if data['endStats']['winner'] == 2 else 2

    return json.dumps(data, separators=(',', ':'))


def process_file(file, flipped_file, flip=False, turns=None, frames=True):
    for i, line in enumerate(file):
        flipped_file.write(process_line(i, line, flip, turns, frames))


def make_suffix(args):
    if args["suffix"] != "_":
        return "_"+args["suffix"]

    suffix = ""
    if args["turns"]:
        suffix += "_" + "_".join([str(t) for t in args["turns"]])

    if args["flip"]:
        suffix += "_flipped"

    if args["no_frames"]:
        suffix += "_clean"

    if suffix == "":
        suffix = "_"

    return suffix


def main(args):
    for file in args['files']:
        suffix = make_suffix(args)
        with open(file, 'r') as f:
            with open(file[:file.find('.')] + suffix + file[file.find('.'):], 'w') as new_file:
                process_file(f, new_file, args['flip'], args['turns'], not args['no_frames'])


if __name__ == "__main__":
    args = parse_args()
    main(args)