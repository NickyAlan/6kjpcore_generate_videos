import urllib
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
    ssize = max_ / (str_length2 + 2)
    fonsize_dict = {'l': lsize,'m': msize,'s': ssize}

    if str_length1 == 1 :
        fonsize_dict['m'] = max_ / (str_length1 + 1)
        fonsize_dict['s'] = ( max_ * 4 ) / str_length2

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
    if vocab_length == 1 :
        max_ = 120
        top = 50
    elif vocab_length ==2 :
        max_ = 250
        top = 60
    elif vocab_length <= 4 :
        max_ = 440
        top = 72
    elif vocab_length <= 7 :
        max_ = 600
        top = 90
    elif vocab_length <= 14 :
        max_ = 680
        top = 120
    else :
        max_ = 750
        top = 160
    
    return max_, top

def get_max_st(sentence_length: int) :
    if sentence_length <= 18 :
        max_ = 840
    elif sentence_length <= 26 :
        max_ = 800
    elif sentence_length <= 41 :
        max_ = 750
    else :
        max_ = 700

    return max_

def download_from_url(url: str, filepath: str) :
    urllib.request.urlretrieve(url, filepath)