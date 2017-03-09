#!/bin/bash
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
echo ">>>>>>> STOP SENSOR"
cd $DIR/sensor/
python app.py stop
echo ">>>>>>> STOP VIDEO"
cd $DIR/video/
python app.py stop