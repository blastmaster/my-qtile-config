from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget
from libqtile.dgroups import simple_key_binder
import libqtile

# Some constants

MOD = 'mod4'
TERMINAL = 'roxterm'
GROUP_NAMES = [str(i) for i in range(1, 10)]


keys = [

    # navigate through windows
    Key([MOD], 'k', lazy.layout.up(),
        dict(desc='set focus on window above')),
    Key([MOD], 'j', lazy.layout.down(),
        dict(desc='set focus on window below')),
    Key([MOD], "h", lazy.layout.left(),
        dict(desc='set focus on window left')),
    Key([MOD], "l", lazy.layout.right(),
        dict(desc='set focus on window right')),

    # shuffle windows
    Key([MOD, 'shift'], 'k', lazy.layout.shuffle_up(),
        dict(desc='shuffle window up')),
    Key([MOD, 'shift'], 'j', lazy.layout.shuffle_down(),
        dict(desc='shuffle window down')),
    Key([MOD, "shift"], "h", lazy.layout.shuffle_left(), lazy.layout.swap_left(),
        dict(desc='shuffle window left')),
    Key([MOD, "shift"], "l", lazy.layout.shuffle_right(), lazy.layout.swap_right(),
        dict(desc='shuffle window right')),

    # manipulate size of windows
    Key([MOD, 'control'], 'j', lazy.layout.grow(), lazy.layout.grow_down(),
        dict(desc='increase size of current window')),
    Key([MOD, 'control'], 'k', lazy.layout.shrink(), lazy.layout.grow_up(),
        dict(desc='decrease size of current window')),
    Key([MOD, "control"], "h", lazy.layout.grow_left(),
        dict(desc='increase window size to left')),
    Key([MOD, "control"], "l", lazy.layout.grow_right(),
        dict(desc='increase window size to right')),

    # misc layout modifications
    Key([MOD], 'f', lazy.window.toggle_fullscreen(),
        dict(desc='toggle fullscreen')),
    Key([MOD, 'control'], 'space', lazy.window.toggle_floating(),
        dict(desc='toggle floating')),
    Key([MOD], 'm', lazy.layout.maximize(),
        dict(desc='maximize current window')),
    Key([MOD], 'n', lazy.layout.normalize(),
        dict(desc='normalize current window')),
    Key([MOD, 'shift'], 'Return', lazy.layout.toggle_split(),
        dict(desc='toggle split')),
    Key([MOD, 'control'], 'Return', lazy.layout.rotate(),
        dict(desc='rotate layout')),

    # control
    Key([MOD], 'r', lazy.spawncmd(),
        dict(desc='run an application')),
    Key([MOD], 'space', lazy.next_layout(),
        dict(desc='switch to next layout')),
    Key([MOD, 'shift'], 'space', lazy.prev_layout(),
        dict(desc='switch to previous layout')),
    Key([MOD, 'shift'], 'c', lazy.window.kill(),
        dict(desc='kill window')),
    Key([MOD, 'control'], 'r', lazy.restart(),
        dict(desc='restart qtile')),
    Key([MOD, 'control'], 'q', lazy.shutdown(),
        dict(desc='quit qtile')),
    Key([MOD], 'Return', lazy.spawn(TERMINAL),
        dict(desc='start a terminal')),

    # group bindings
    Key([MOD], 'Left', lazy.screen.prev_group(),
        dict(desc='switch to group left')),
    Key([MOD], 'Right', lazy.screen.next_group(),
        dict(desc='switch to group right')),
    Key([MOD], 'Escape', lazy.screen.togglegroup(),
        dict(desc='toggle group'))

]

# Groups

groups = [Group(g) for g in GROUP_NAMES]

for gr in groups:
    # keybinding to move to group
    keys.append(Key([MOD], gr.name, lazy.group[gr.name].toscreen()))
    # keybinding to move window to certain group
    keys.append(Key([MOD, 'shift'], gr.name, lazy.window.togroup(gr.name)))


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
    low_forgeground='ff0000',
    **widget_defaults,
)

battery_widget = widget.Battery(**battery)
#bat_icon = battery.copy()
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
    fill_color='c01010',
    **widget_defaults,
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
    **widget_defaults,
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
    **widget_defaults,
)


def separator(sep='|'):
    return libqtile.widget.TextBox(sep, foreground='7070ff', **widget_defaults)


top_widgets = [
    widget.GroupBox(rounded=False, borderwidth=2, **widget_defaults),
    widget.Prompt(),
    widget.TaskList(rounded=False, **widget_defaults),
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
        format='%Y-%m-%d %a %I:%M %p',
        **widget_defaults),
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
    Drag([MOD], 'Button1', lazy.window.set_position_floating(),
        start=lazy.window.get_position()),
    Drag([MOD], 'Button3', lazy.window.set_size_floating(),
        start=lazy.window.get_size()),
    Click([MOD], 'Button2', lazy.window.bring_to_front())
]

dgroups_key_binder = simple_key_binder(MOD)
dgroups_app_rules = []
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_wrap = False
floating_layout = layout.Floating()
auto_fullscreen = True
