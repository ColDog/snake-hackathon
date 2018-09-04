#!/bin/bash

game_id=$(bin/engine create -c snake-config.json | jq -r '.ID')
./bin/engine run -g $game_id
sleep 1
./bin/engine replay -g $game_id
