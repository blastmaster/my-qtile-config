#! /bin/bash

Xephyr :2 -screen 960x740 &
DISPLAY=:2 qtile
