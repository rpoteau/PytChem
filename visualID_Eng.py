import os,sys,platform
from datetime import datetime
import datetime, time
#from IPython.core.display import display,Image,Markdown,HTML
from IPython.display import display,Image,Markdown,HTML
from urllib.request import urlopen

__author__ = "Romuald POTEAU"
__maintainer__ =  "Romuald POTEAU"
__email__ = "romuald.poteau@univ-tlse3.fr"
__status__ = "Development"

_start_time   = None
_end_time     = None
_chrono_start = None
_chrono_stop  = None

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   OFF = '\033[0m'

def css_styling():
    styles = open("./css/visualID.css", "r").read()
    display(HTML(styles))
#def css_styling():
#    html = urlopen("file:./css/visualID.css")
#    styles = HTML(html.read().decode('utf-8'))
#    display(HTML(styles))

def display_md(text):
    display(Markdown(text))
    
def hdelay(sec):
    return str(datetime.timedelta(seconds=int(sec)))    
    
# Return human delay like 01:14:28 543ms
# delay can be timedelta or seconds
def hdelay_ms(delay):
    if type(delay) is not datetime.timedelta:
        delay=datetime.timedelta(seconds=delay)
    sec = delay.total_seconds()
    hh = sec // 3600
    mm = (sec // 60) - (hh * 60)
    ss = sec - hh*3600 - mm*60
    ms = (sec - int(sec))*1000
    return f'{hh:02.0f}:{mm:02.0f}:{ss:02.0f} {ms:03.0f}ms'

def chrono_start():
    global _chrono_start, _chrono_stop
    _chrono_start=time.time()

# return delay in seconds or in humain format
def chrono_stop(hdelay=False):
    global _chrono_start, _chrono_stop
    _chrono_stop = time.time()
    sec = _chrono_stop - _chrono_start
    if hdelay : return hdelay_ms(sec)
    return sec

def chrono_show():
    print('\nDuration : ', hdelay_ms(time.time() - _chrono_start))

def init():
    global _start_time
    # Styling notebook
    #
    css_styling()
    # Today, now and hostname
    #
    _start_time = datetime.datetime.now()
    start_time = _start_time.strftime("%A %d %B %Y, %H:%M:%S")
    _h = platform.uname()
    h = _h[1]+" ("+_h[0]+")"
    md = f'**Start at:** {start_time}  \n'
    md+= f'**Hostname:** {h}'
    display_md(md)
    #print('Run time             :', _start_time.strftime("%A %d %B %Y, %H:%M:%S"))
    #print('Hostname             :', f'{h[1]} ({h[0]})')
    md = '<p style="text-align: center"><img width="800px" src="./svg/logoPytChem.svg" style="margin-left:auto; margin-right:auto"/></p>'
    display_md(md)
    
def end():
    global _end_time
    _end_time = datetime.datetime.now()
    end_time = time.strftime("%A %d %B %Y, %H:%M:%S")
    duration = hdelay_ms(_end_time - _start_time)
    md = f'**End at:** {end_time}  \n'
    md+= f'**Duration:** {duration}'
    display_md(md)
    md = '<p style="text-align: center"><img width="800px" src="./svg/logoEnd.svg" style="margin-left:auto; margin-right:auto"/></p>'
    display_md(md)

def y2c(mc2i,y):
    import tensorflow as tf
    from tensorflow import keras
    from keras.utils import np_utils
    from keras.utils import to_categorical
    y_array = y.copy()
    y_array = y_array.to_numpy() # transformation au format numpy
    # transformation des valeurs de y1 & y2 en entiers
    for x in range(len(y_array)):
        #print(x, y_array[x], mapc2i[y_array[x]])
        y_array[x] = mc2i[y_array[x]]
    yohe = to_categorical(y_array)
    del y_array
    return yohe

def categorizeY_2ohe(Ctot, y1, y2):
# one-hot-encodes a pandas column of categorical data
# Ctot is the reference pandas column, necessary to find all unique categories in this column
# y1 and y2 are the actual pandas column that will be categorized. y1 and y2 are supposed to be
# the ytest and ytrain subsets of Ctot 
# y1ohe and y2ohe are the numpy arrays returned by this routine
    uv = Ctot.unique()
    print(f"Cat??gories uniques : {uv}") 
    mapc2i = {}
    for x in range(len(uv)):
        mapc2i[uv[x]] = x
    print(f"Correspondance entre chaque cat??gorie unique et un entier : {mapc2i}")
    y1ohe = y2c(mapc2i,y1)
    y2ohe = y2c(mapc2i,y2)
    print(f"Structure (shape) des tableaux renvoy??s par categorize1C_2ohe. y1 : {y1ohe.shape}, y2 : {y2ohe.shape}")
    del mapc2i, uv
    return y1ohe, y2ohe
