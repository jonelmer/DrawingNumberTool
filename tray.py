from infi.systray import SysTrayIcon
import pyperclip
import easygui
import pickle

try:
    (count, prefix) = pickle.load(open('save.p', 'rb'))
except FileNotFoundError:
    count = 3000
    prefix = "JE-"

def hello(systray):
    print("Hello")

def increment(systray):
    global count
    count = count +1
    systray.update(hover_text=c_to_s(count))
    save(systray)

def copy(systray):
    global count
    pyperclip.copy(c_to_s(count)+'\tA')

def copy_inc(systray):
    copy(systray)
    increment(systray)

def range_box(systray):
    number = c_to_s(count)
    items = [number+'\tA',]
    for i in range(100):
        items.append("{0}_{1:02d}\tA".format(number, i))
    easygui.textbox('\n'.join(items))

def c_to_s(count):
    return "{0}{1:06d}".format(prefix, count)

def update_count(systray):
    global count, prefix
    s = easygui.enterbox('Current available number')
    split = -s[::-1].find('-')

    prefix = s[:split].upper()
    count = int(s[split:])

    systray.update(hover_text=c_to_s(count))
    save(systray)

def save(systray):
    global count, prefix
    pickle.dump((count, prefix), open('save.p', 'wb'))


def on_quit(systray):
    save(systray)

    
    
menu_options = (
                ("Copy + Next", None, copy_inc),
                ("Next", None, increment),
                ("Copy", None, copy),
                ("Update", None, update_count),
                ("Range", None, range_box),
                #("Freia", None, (("TOP - SI-7650", None, print),
                #                 ("Shutter & Insert - SI-7651", None, print)
                #                 )),
                )



systray = SysTrayIcon(".\icon.ico", c_to_s(count), menu_options,
                      default_menu_index=0, on_quit=on_quit)
systray.start()
