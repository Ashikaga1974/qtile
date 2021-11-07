
import os
import re
import socket
import subprocess
from libqtile import qtile
from libqtile.config import Click, Drag, Group, KeyChord, Key, Match, Screen
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from typing import List  # noqa: F401from typing import List  # noqa: F401
from libqtile import extension

from Xlib import X, display
from Xlib.ext import randr
from pprint import pprint

from libqtile.log_utils import logger

### Autostart - Script
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])

#@hook.subscribe.client_new
#def client_new(client):
#    if client.name == 'Mozilla Firefox':
#       client.togroup('2_WEB')
#    if client.name == 'Unbenannt - Kate':
#       client.togroup('3_DEV')
#    if client.name == 'Sascha-KDE — Konsole':
#       client.togroup('4_TERM')

### Globale Variablen
mod = "mod4"
alt = "mod1"
terminal = "konsole" #guess_terminal()

### Keymapping
keys = [
    ### APPLICATIONS
    # Dmenu

    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),


    Key([mod], 't', lazy.run_extension(extension.DmenuRun(
                    dmenu_prompt = ">",
                    dmenu_font = "Source Code Pro 12",
                    dmenu_height = 20,
    ))),

    # FireFox
    Key([mod],      "b",                                    lazy.spawn("firefox"), desc = "Launch Firefox"),

    # Switch between windows
    Key([mod],      "h",                                    lazy.layout.left(), desc = "Move focus to left"),
    Key([mod],      "l",                                    lazy.layout.right(), desc = "Move focus to right"),
    Key([mod],      "j",                                    lazy.layout.down(), desc = "Move focus down"),
    Key([mod],      "k",                                    lazy.layout.up(), desc = "Move focus up"),

    # In Vollbild schalten
    Key([mod],      "space",                                lazy.window.toggle_fullscreen(), desc = "Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod,       "shift"],           "h",                lazy.layout.shuffle_left(), desc = "Move window to the left"),
    Key([mod,       "shift"],           "l",                lazy.layout.shuffle_right(), desc = "Move window to the right"),
    Key([mod,       "shift"],           "j",                lazy.layout.shuffle_down(), desc = "Move window down"),
    Key([mod,       "shift"],           "k",                lazy.layout.shuffle_up(), desc = "Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod,       "control"],          "h",               lazy.layout.grow_left(), desc = "Grow window to the left"),
    Key([mod,       "control"],          "l",               lazy.layout.grow_right(), desc = "Grow window to the right"),
    Key([mod,       "control"],          "j",               lazy.layout.grow_down(), desc = "Grow window down"),
    Key([mod,       "control"],          "k",               lazy.layout.grow_up(), desc = "Grow window up"),
    Key([mod],      "n",                                    lazy.layout.normalize(), desc = "Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod,       "shift"],           "Return",           lazy.layout.toggle_split(), desc = "Toggle between split and unsplit sides of stack"),
    Key([mod],      "Return",                               lazy.spawn(terminal), desc = "Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod],      "Tab",                                  lazy.next_layout(), desc = "Toggle between layouts"),
    Key([mod],      "w",                                    lazy.window.kill(), desc = "Kill focused window"),

    Key([mod,       "control"],         "r",                lazy.restart(), desc = "Restart Qtile"),
    Key([mod,       "control"],         "q",                lazy.shutdown(), desc = "Shutdown Qtile"),
]

###########Gruppen zuweisen ###########
group_names = [     ("1_ALL", {'layout': 'columns'}),
                    ("2_WEB", {'layout': 'columns'}),
                    ("3_DEV", {'layout': 'columns'}),
                    ("4_TERM", {'layout': 'columns'}),
                    ("5_SONS", {'layout': 'columns'})
]

groups = [Group(name, **kwargs) for name, kwargs in group_names]

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))
    # Switch to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name)))
    # Send current window to another group

###########Farben zuweisen ###########
colors = [
                    ["#282c34", "#282c34"], # 0 panel background
                    ["#3d3f4b", "#434758"], # 1 background for current screen tab
                    ["#ffffff", "#ffffff"], # 2 font color for group names
                    ["#ff5555", "#ff5555"], # 3 border line color for current tab
                    ["#74438f", "#74438f"], # 4 border line color for 'other tabs' and color for 'odd widgets'
                    ["#4f76c7", "#4f76c7"], # 5 color for the 'even widgets'
                    ["#e1acff", "#e1acff"], # 6 window name
                    ["#ecbbfb", "#ecbbfb"],  # 7 backbround for inactive screens
                    ["#fefe22", "#fefe22"]  # 8 yellow
]

########### Gruppen initialisieren und Tasten zuweisen (CTRL+ALT) ###########
layout_theme = {
                    "border_width": 4,
                    "margin": 5,
                    "border_focus": colors[5],
                    "border_normal": colors[1]
}

########### Layouts zuweisen ###########
layouts = [

    layout.Floating(fullscreen_border_width = 4),

    layout.Columns(
                    **layout_theme,
                    icon = "",
    ),

    layout.Max(),

    layout.TreeTab( **layout_theme,
                    active_bg = "#4f76c7",
                    active_fg = "#000000",
                    bg_color = "#141414",
                    font = "sans",
                    fontsize = 10,
                    inactive_bg = "#384323",
                    inactive_fg = "#a0a0a0",
                    sections = ["Apps"],
                    section_fontsize = 10,
                    section_top = 10,
                    panel_width = 200,
                    padding_x = 2
    ),

    layout.MonadTall(
                    **layout_theme
    ),


    # Try more layouts by unleashing below layouts.
    # layout.Stack(margin = 5, num_stacks = 2),p
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.VerticalTile(),
    # layout.Zoomy(),

]

PaddingSeperator = 5
LineWidthSeperator = 0

##### DEFAULT WIDGET SETTINGS #####
widget_defaults = dict(
                    font = "Source Code Pro Bold",
                    fontsize = 12,
                    padding = 2,
)

##### WIDGETS INITIALISIEREN #####
def init_widgets_list():
    widgets_list = [

                    #1
                    widget.CurrentLayoutIcon(scale = .80),

                    #2
                    widget.Image(
                        filename = "~/.config/qtile/icons/start-menu-win11.png", scale = "false", mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' -e dolphin')}
                        ),

                    widget.Image(
                        filename = "~/.config/qtile/icons/start-menu-win11.png", scale = "false", mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn("/home/sascha/xmenu/xmenu.sh")}
                        ),

                    #3
                    widget.GroupBox(hide_unused = False, highlight_method = 'border', font = 'Source Code Pro Bold'),

                    #4
                    widget.WindowCount(text_format = '[{num}]', foreground = colors[8]),

                    #5
                    widget.Prompt(),

                    #6
                    widget.WindowName(foreground = colors[5]),

                    #widget.TaskList(highlight_method = "block", rounded = False),

                    #widget.WindowTabs(),

                    #7
                    widget.Chord(chords_colors={'launch': ("#ff0000", "#ffffff")}, name_transform=lambda name: name.upper()),

                    #8
                    ### Abstand
                    widget.Sep(linewidth = LineWidthSeperator, padding = PaddingSeperator, foreground = colors[2], background = colors[0], mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn('firefox -private')}),

                    ### FireFox
                    #9
                    widget.TextBox(text = "  Firefox", foreground = colors[2], background = colors[4], padding = 5, mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn('firefox')}),

                    #10
                    ### Abstand
                    widget.Sep(linewidth = LineWidthSeperator, padding = PaddingSeperator, foreground = colors[2], background = colors[0]),

                    #11
                    ### Ranger
                    widget.TextBox(text = "  Ranger", foreground=colors[2], background = colors[5], padding = 5, mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' -e ranger')}),

                    #12
                    ### Abstand
                    widget.Sep(linewidth = LineWidthSeperator, padding = PaddingSeperator, foreground = colors[2], background = colors[0]),

                    ### Terminal
                    #13
                    widget.TextBox(text = "  Terminal" , foreground = colors[2], background = colors[4], padding = 2, mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal)}),

                    #14
                    ### Abstand
                    widget.Sep(linewidth = LineWidthSeperator, padding = PaddingSeperator, foreground = colors[2], background = colors[0]),

                    #15
                    ### Settings
                    widget.TextBox(text = "  Settings" , foreground = colors[2], background = colors[5], padding = 5, mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn("systemsettings5")}),

                    #16
                    ### Abstand
                    widget.Sep(linewidth = LineWidthSeperator, padding = PaddingSeperator, foreground = colors[2], background = colors[0]),

                    #17
                    widget.TextBox(text = "  Config.py", foreground = colors[2], background = colors[4], mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn('kate /home/sascha/.config/qtile/config.py')}),

                    #18
                    ### Abstand
                    widget.Sep(linewidth = LineWidthSeperator, padding = PaddingSeperator, foreground = colors[2], background = colors[0], mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn('kate /home/sascha/.local/share/qtile/qtile.log')}),

                    #19
                    ### Volume
                    widget.TextBox(text = " ♫", padding = 2, foreground = colors[2], background = colors[4]),
                    #20
                    widget.Volume(foreground = colors[2], background = colors[4]),

                    #21
                    ### Abstand
                    widget.Sep(linewidth = LineWidthSeperator, padding = PaddingSeperator, foreground = colors[2], background = colors[0]),

                    #22
                    ### Updates
                    widget.TextBox(text = " ⟳", padding = 2, foreground = colors[2], background = colors[5], fontsize = 11),
                    #23
                    widget.CheckUpdates(update_interval = 60, distro = "Arch", display_format = "{updates} Updates", no_update_string = 'Keine Updates', foreground = colors[2], mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' -e sudo pacman -Syu')}, background = colors[5]),

                    #24
                    ### Abstand
                    widget.Sep(linewidth = LineWidthSeperator, padding = PaddingSeperator, foreground = colors[2], background = colors[0]),

                    #25
                    ### Uhr
                    widget.Clock(format=' %d.%m.%Y %a %H:%M:%S', background = colors[4]),

                    #26
                    ### Abstand
                    widget.Sep(linewidth = LineWidthSeperator, padding = PaddingSeperator, foreground = colors[2], background = colors[0]),

                    #27
                    ### Logout
                    widget.QuickExit(default_text = "", background = colors[5]),

                    #28
                    ### Abstand
                    widget.Sep(linewidth = LineWidthSeperator, padding = PaddingSeperator, foreground = colors[2], background = colors[0]),

                    #29
                    ### Tray
                    widget.Systray(),

                    #30
                    widget.KeyboardLayout(configured_keyboards = ['de', 'us']),

                    #31
                    ### Abstand
                    widget.Sep(linewidth = LineWidthSeperator, padding = PaddingSeperator, foreground = colors[2], background = colors[0]),

                    #32
                    ### CPU Widget (2ter Monitor)
                    widget.CPU(update_interval = 5),

                    #33
                    ### Abstand
                    widget.Sep(linewidth = LineWidthSeperator, padding = PaddingSeperator, foreground = colors[2], background = colors[0]),

                    #34 CPU Widget (2ter Monitor)
                    widget.CPUGraph(border_width = 1, line_width = 1, core = "all", type = "box"),

                    #35
                    ### Abstand
                    widget.Sep(linewidth = LineWidthSeperator, padding = PaddingSeperator, foreground = colors[2], background = colors[0]),

                    #36 Net Widget (2ter Monitor)
                    widget.NetGraph(interface = "enp5s0", border_width = 1, line_width = 1),

                    #37
                    ### Abstand
                    widget.Sep(linewidth = LineWidthSeperator, padding = PaddingSeperator, foreground = colors[2], background = colors[0]),

                    #38
                    ### Temperatur (2ter Monitor)
                    widget.TextBox(text = " 🌡", padding = 2, foreground = colors[2], background = colors[5], fontsize = 10),
                    #39
                    widget.ThermalSensor(foreground = colors[2], background = colors[5], fontsize = 10, threshold = 90, padding = 5),

                    #40
                    ### Abstand
                    widget.Sep(linewidth = LineWidthSeperator, padding = PaddingSeperator, foreground = colors[2], background = colors[0]),

                    #41
                    ### Speicher (2ter Monitor)
                    widget.TextBox(text = " 🖬", foreground = colors[2], background = colors[4], padding = 0, fontsize = 10),
                    #42
                    widget.Memory(foreground = colors[2], background = colors[4], fontsize = 10, mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' -e htop')}, padding = 5),

                    #43
                    ### Abstand
                    widget.Sep(linewidth = LineWidthSeperator, padding = PaddingSeperator, foreground = colors[2], background = colors[0]),

            ]
    return widgets_list

##### Widgets für den ersten Monitor einstellen #####
def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    del widgets_screen1[29:43]
    return widgets_screen1

##### Widgets für den 2 Monitor einstellen #####
def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    del widgets_screen2[6:29]
    return widgets_screen2

##### MAUS EVENTS BEIM UMGANG MIT FENSTERN #####
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

##### MONITORE INITIALISIEREN #####
def init_screens():
    return [Screen(top = bar.Bar(widgets = init_widgets_screen1(), opacity = 1.0, size = 20)),
            Screen(top = bar.Bar(widgets = init_widgets_screen2(), opacity = 1.0, size = 20)),
]

##### EINSTIEGSPUNKT ZUM AUFBAU DER MONITORE #####
if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()
    widgets_screen2 = init_widgets_screen2()

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules = [
                # Run the utility of `xprop` to see the wm class and name of an X client.
                *layout.Floating.default_float_rules,
                Match(wm_class = 'confirmreset'),  # gitk
                Match(wm_class = 'makebranch'),  # gitk
                Match(wm_class = 'maketag'),  # gitk
                Match(wm_class = 'ssh-askpass'),  # ssh-askpass
                Match(title = 'branchdialog'),  # gitk
                Match(title = 'pinentry'),  # GPG key password entry
])

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
