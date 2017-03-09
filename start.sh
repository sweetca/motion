#!/bin/bash
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
echo ">>>>>>> START VIDEO"
cd $DIR/video/
python app.py start
echo ">>>>>>> START SENSOR"
cd $DIR/sensor/
python app.py start