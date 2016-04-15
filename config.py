from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget
import libqtile

# Some constants

mod = 'mod4'
alt = 'mod1'
terminal = 'roxterm'
group_names = [str(i) for i in range(1, 10)]


keys = [
    # navigate through application
    Key([mod], 'k', lazy.layout.up()),
    Key([mod], 'j', lazy.layout.down()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),

    # shuffle applications
    Key([mod, 'shift'], 'k', lazy.layout.shuffle_up()),
    Key([mod, 'shift'], 'j', lazy.layout.shuffle_down()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), lazy.layout.swap_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), lazy.layout.swap_right()),

    # manipulate size of application windows
    Key([mod, 'control'], 'j', lazy.layout.grow(), lazy.layout.grow_down()),
    Key([mod, 'control'], 'k', lazy.layout.shrink(), lazy.layout.grow_up()),
    Key([mod, "control"], "h", lazy.layout.grow_left()),
    Key([mod, "control"], "l", lazy.layout.grow_right()),

    Key([mod], 'f', lazy.window.toggle_fullscreen()),
    Key([mod, 'control'], 'space', lazy.window.toggle_floating()),

    Key([mod], 'm', lazy.layout.maximize()),
    Key([mod], 'n', lazy.layout.normalize()),

    Key([mod, 'shift'], 'Return', lazy.layout.toggle_split()),
    Key([mod, 'control'], 'Return', lazy.layout.rotate()),

    # control
    Key([mod], 'r', lazy.spawncmd()),
    Key([mod], 'space', lazy.next_layout()),
    Key([mod, 'shift'], 'space', lazy.prev_layout()),

    Key([mod, 'shift'], 'c', lazy.window.kill()),
    Key([mod, 'control'], 'r', lazy.restart()),
    Key([mod, 'control'], 'q', lazy.shutdown()),
    Key([mod], 'Return', lazy.spawn(terminal)),

    # Group bindings
    Key([mod], 'Left', lazy.group.prevgroup()),
    Key([mod], 'Right', lazy.group.nextgroup()),
    Key([mod], 'Escape', lazy.screen.togglegroup())

]

# Groups

groups = [Group(g) for g in group_names]

for gr in groups:
    # keybinding to move to group
    keys.append(Key([mod], gr.name, lazy.group[gr.name].toscreen()))
    # keybinding to move window to certain group
    keys.append(Key([mod, 'shift'], gr.name, lazy.window.togroup(gr.name)))


# Layouts

layouts = [
    layout.MonadTall(),
    layout.Columns(),
    layout.Wmii(),
    layout.Stack(num_stack=2),
    layout.Floating(),
    layout.Max(),
]

# Widgets

widget_defaults = dict(
    font='Arial',
    fontsize=11,
    padding=3,
)

# Battery widget

# '⏦', 'AC CURRENT'
# '⚠', 'WARNING SIGN'
# ⚡ U+26A1 'HIGH VOLTAGE'

battery = dict(
    battery_name='BAT0',
    energy_now_file='energy_now',
    energy_full_file='energy_full',
    power_now_file='power_now',
    charge_char='⚡',
    discharge_char='⏦',
    update_delay=5,
    foreground='7070ff',
    low_forgeground='ff0000'
)

battery_widget = widget.Battery(**battery)
bat_icon = battery.copy()
#TODO
#path = '/home/blastmaster/.config/qtile/theme/'
#myicons = {
        #'battery-missing': 'battery-caution.png',
        #'battery-caution': 'battery-caution.png',
        #'battery-low': 'battery-low.png',
        #'battery-good': 'battery-good.png',
        #'battery-full': 'battery-full.png',
        #'battery-caution-charging': 'battery-caution-charging.png',
        #'battery-low-charging': 'battery-low-charging.png',
        #'battery-good-charging': 'battery-good-charging.png',
        #'battery-full-charging': 'battery-full-charging.png',
        #'battery-full-charged': 'battery-full-charged.png',
#}

#bat_icon.update({'theme_path': path,
                 #'custom_icons': myicons})

#battery_icon = widget.BatteryIcon(**bat_icon)

# CPU-Graph widget

cpu_graph = widget.CPUGraph(
    samples=50,
    line_width=1,
    width=42,
    height=14,
    margin_x=1,
    margin_y=1,
    border_width=1,
    graph_color='ff2020',
    fill_color='c01010'
)

# Memory widget

memory_widget = widget.Memory(foreground='7070ff')

# Memory-Graph widget

memory_graph = widget.MemoryGraph(
    samples=50,
    line_width=2,
    width=42,
    height=14,
    margin_x=1,
    margin_y=1,
    type='box',
    border_width=1,
    graph_color='ff2020',
)

# Net-Graph widget

net_graph = widget.NetGraph(
    samples=50,
    line_width=1,
    margin_x=1,
    margin_y=1,
    width=42,
    height=14,
    border_width=1,
    interface='wlan0',
    graph_color='22ff44',
    fill_color='11aa11',
)


def separator(sep='|'):
    return libqtile.widget.TextBox(sep, foreground='7070ff')


top_widgets = [
    widget.GroupBox(rounded=False, borderwidth=2),
    widget.Prompt(),
    widget.TaskList(fontsize=11, rounded=False),
    widget.Systray(),
    separator(sep='Net: '),
    net_graph,
    # TODO: install dependencies for Wlan
    #widget.Wlan(interface='wlan0'),
    separator(sep='Cpu: '),
    cpu_graph,
    separator('Mem: '),
    memory_graph,
    battery_widget,
    # TODO: too big, scale down!
    #battery_icon,
    widget.Notify(),
]

bottom_widgets = [
    widget.Spacer(),
    memory_widget,
    widget.Sep(foreground='7070ff'),
    widget.CurrentLayout(foreground='7070ff'),
    widget.Sep(foreground='7070ff'),
    widget.Clock(foreground='7070ff',
        format='%Y-%m-%d %a %I:%M %p'),
]

# Screens

screens = [
    Screen(
        top=bar.Bar(top_widgets, 24),
        bottom=bar.Bar(bottom_widgets, 24)
    ),
]

# Drag floating layouts.

mouse = [
    Drag([mod], 'Button1', lazy.window.set_position_floating(),
        start=lazy.window.get_position()),
    Drag([mod], 'Button3', lazy.window.set_size_floating(),
        start=lazy.window.get_size()),
    Click([mod], 'Button2', lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_wrap = False
floating_layout = layout.Floating()
auto_fullscreen = True
