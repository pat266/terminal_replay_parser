Small script for parsing replays files for  https://terminal.c1games.com

Based on the work of   
@Isaac at https://forum.c1games.com/
https://github.com/idraper/terminal_flip_replay

#Usage

`python replay_parser.py --flip [file_names]`  
>switches player1 and player2 positions

`python replay_parser.py --no_frames [file_names]`
>extracts only turn_info, removing all the frame_info. 
The replay can not be viewed any more but is more convenient for testing and editing

`python replay_parser.py -t 6 -t 10 [file_names]`
>extracting only specific turn(s). This is great for debugging specific bad move. Does not work well if you relay on history data.


#Example

`python scripts/replay_parser.py -flip replays/flip_me.replay`

`python scripts/replay_parser.py -flip --no_frames -t 5 replays/check_turn_5_upsidedown.replay`

`python scripts/replay_parser.py --no_frames -t 8 -t 9 -t 10 replays/why_stacking_for_3_turns.replay`