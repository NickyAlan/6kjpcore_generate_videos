import urllib
import subprocess
from moviepy.editor import TextClip

def create_generator(fontsize: float, font = 'wqy-microhei.ttc', color='white', bg_color = 'transparent') :
    '''
    create generator TextClip
    '''
    generator = lambda text: TextClip(text, font=font, fontsize=fontsize, color=color, bg_color=bg_color)
    return generator

def create_fontsize(str_length1: int, str_length2: int, max_ = 330) :
    '''
    create appropriate fontsie
    '''
    lsize = max_ / str_length1
    msize = max_ / (str_length1 + 3)
    
    if str_length2 <= 4 :
        ssize = max_ / (str_length2 + 4)
    elif str_length2 >= 34 :
        ssize = max_ / (str_length2)
    elif str_length2 >= 21 :
        ssize = max_ / (str_length2 - 5)
    else :
        ssize = max_ / (str_length2 + 1)
    
    fonsize_dict = {'l': lsize,'m': msize,'s': ssize}

    if str_length1 == 1 :
        fonsize_dict['m'] = max_ / (str_length1 + 1)
        fonsize_dict['s'] = ( max_ * 4 ) / str_length2
    elif str_length1 == 2 :
        fonsize_dict['m'] = max_ / (str_length1 + 2)
        if str_length2 <= 4 :
            fonsize_dict['s'] = ( max_ * 2 ) / (str_length2 + 4)
        else :
            fonsize_dict['s'] = ( max_ * 2 ) / str_length2

    return fonsize_dict

def get_ypos(fontsize_dict: dict, top = 72) :
    '''
    adjust y-position from fonsize_dict
    '''
    ypos = {
        '1': top,
        '2': top + fontsize_dict['l'] + 10,
        '3': top + fontsize_dict['l'] + fontsize_dict['m'] + 15,
        '4': top + fontsize_dict['l'] + (2 * fontsize_dict['m']) + 1.7 * fontsize_dict['s'],
    }
    return ypos

def get_max_top(vocab_length: int) :
    convert = {1: (120, 50), 2: (270, 60), 3: (390, 72), 4: (440, 72), 5: (480, 73), 6: (520, 75), 7: (600, 120), 8: (600, 120), 9: (620, 120) ,14: (680, 120)}
    try :
        max_, top = convert[vocab_length]
    # if not exist in dict
    except :
        if vocab_length < 14 :
            max_, top = convert[14]
        else :
            max_, top = (750, 160)

    return max_, top

def get_max_st(sentence_length: int) :
    if sentence_length <= 18 :
        max_ = 840
    elif sentence_length <= 26 :
        max_ = 800
    elif sentence_length <= 41 :
        max_ = 720
    else :
        max_ = 690

    return max_

def download_from_url(url: str, filepath: str) :
    urllib.request.urlretrieve(url, filepath)

def copy2clip(text: str) :
    cmd = f'echo {text}|clip'
    return subprocess.check_call(cmd, shell=True)