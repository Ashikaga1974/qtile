#!/bin/bash
xrandr --output DisplayPort-0 --mode 1920x1080 --pos 1920x0 --rotate normal --output DisplayPort-1 --off --output DisplayPort-2 --off --output HDMI-A-0 --off --output DVI-D-0 --primary --mode 1920x1080 --pos 0x0 --rotate normal
feh --bg-scale ~/Bilder/kdeplasma-win11/wallpaper/Windows\ 11\ Wallpaper\ 2\ \(1\).jpg --bg-scale ~/Bilder/kdeplasma-win11/wallpaper/Windows\ 11\ Wallpaper\ 2\ \(1\).jpg
picom &
