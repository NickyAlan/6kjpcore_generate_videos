import pandas as pd
import math, datetime, os
from utils import download_from_url
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.editor import AudioFileClip, ImageClip, CompositeVideoClip, concatenate_videoclips, TextClip

def create_generator(fontsize: float, font = 'fonts/wqy-microhei.ttc', color='white', bg_color = 'transparent', opacity = 1.0) :
    '''
    create generator TextClip
    '''
    generator = lambda text: TextClip(text, font=font, fontsize=fontsize, color=color, bg_color=bg_color)\
                .set_opacity(opacity)
    return generator

def seconds2timestamp(seconds: float) :
    '''
    convert seconds to timestamp format
    '''
    base = str(seconds).split('.')
    msec = base[-1].ljust(3, '0') # add to back 1 -> 001
    sec = base[0].rjust(2, '0') # add to font 2 -> 02
    if int(sec) >= 60 :
        minute = str(int(sec)//60).rjust(2, '0')
        sec = str(int(sec) - (60*int(minute))).rjust(2, '0')
    else :
        minute = '00'
    timestamp = f'00:{minute}:{sec},{msec}'
    return timestamp

def get_srtfile(save_path: str, keeps_sec_subtitle: list) :
    ''' 
    save to .srt file
    '''
    if not save_path.endswith('.srt'): save_path += '.srt'
    with open(f'{save_path}', 'w') as file :
        # seconds -> minutes sub | 66.967 -> 01:06,967
        for order, (start_sec, stop_sec, text) in enumerate(keeps_sec_subtitle, start=1) :
            start_stamp = seconds2timestamp(start_sec)
            stop_stamp = seconds2timestamp(stop_sec)
            caption = f'{order}\n{start_stamp} --> {stop_stamp}\n{text}\n\n'
            file.write(caption)

def get_vocabtxt(save_path: str, keeps_vocabs: list) :
    '''
    save to .txt file
    '''
    if not save_path.endswith('.txt'): save_path += '.txt'
    with open(f'{save_path}', 'w', encoding='utf-8') as file :
        for vocab, hiragana, romaji, translate in keeps_vocabs : 
            file.write(f'{vocab} ({hiragana} - {romaji}) : {translate}\n')

if __name__ == "__main__" :
    VIDEO_PATH = "videos/trainstation"
    NUM_VOCABS = 100
    START_VOCAB = 200
    W, H = 1280, 720
    CHENGE_BG_EVERY = 20
    SMOOTH_TIME = 0.2
    opacity_time = 0.1
    END_OPACITY_TIME = 1.2
    INTERVAL_TIME = 3
    start2speech = 0 # for initial text 2 speech capcut
    BG_IMAGES = ["media/a4.jpg", "media/a2.jpg", "media/a1.jpg", "media/a3.jpg", "media/a5.jpg"]
    clips = [] 
    keeps_vocabs = [] # for get txt file
    keeps_sec_subtitle = [] # for text to speech in capcut

    assert len(BG_IMAGES) > (NUM_VOCABS-1)//CHENGE_BG_EVERY, f"total background images must >= {NUM_VOCABS//CHENGE_BG_EVERY}"
    vocabs = pd.read_csv('./jp6kcore.csv', encoding='utf-8-sig')
    hour, minute = datetime.datetime.now().strftime("%H:%M").split(":")
    print(f"\nCreating : {NUM_VOCABS} vocabs ~ {hour}:{int(minute)+math.ceil((36*NUM_VOCABS)/60)}")
    for vocab_idx in range(START_VOCAB, NUM_VOCABS + START_VOCAB) :
        detail = vocabs.iloc[vocab_idx]
        vocab = detail["kanji"]
        hiragana = detail["hira"]
        romaji = detail["romaji"]
        translate = detail["translate"].replace("(colloquial)", "").strip()
        sound = detail["sound_url"]
        keeps_vocabs.append((vocab, hiragana, romaji, translate))
        print(f"[{vocab_idx+1}] : {hiragana} - {translate}")

        download_from_url(sound, f"sounds/{romaji}.mp3")
        sound = AudioFileClip(f"sounds/{romaji}.mp3")

        BG_IMAGE = BG_IMAGES[(vocab_idx-START_VOCAB)//CHENGE_BG_EVERY] # change bg every x vocabs
        ENG_TIME = round(sound.duration, 3) + 1
        VOCAB_TIME = round(sound.duration, 3)
        
        END_TIME = max(ENG_TIME, END_OPACITY_TIME) + (3*INTERVAL_TIME) + (2*max(VOCAB_TIME, END_OPACITY_TIME) + 0.5)
        DURATION = round(END_TIME + 1.2, 3)
        bg_image = ImageClip(img = BG_IMAGE, duration = DURATION).resize((W, H))

        # time for capcut text to speech
        keeps_sec_subtitle.append((round(start2speech, 3), round(start2speech, 3) + 1.0, translate))
        start2speech += END_TIME

        scenes = [bg_image]
        texts = [("translate", translate, 0, END_TIME, 0.15, 75), 
                ("kanji", vocab, max(ENG_TIME, END_OPACITY_TIME) + INTERVAL_TIME, END_TIME, 0.35, 120), 
                ("hiragana", hiragana, max(ENG_TIME, END_OPACITY_TIME) + (2*INTERVAL_TIME) + max(VOCAB_TIME, END_OPACITY_TIME), END_TIME, 0.6, 90), 
                ("romaji", romaji, max(ENG_TIME, END_OPACITY_TIME) + (2*INTERVAL_TIME) + max(VOCAB_TIME, END_OPACITY_TIME), END_TIME, 0.7, 80)]
        opacities = [float(f'0.{ms}') for ms in range(0, 11)]

        for text_type, text, start_time, end_time, y_pos, font_size in texts :
            if text_type == "translate": font = "fonts/Cubano.ttf"
            else : font = "fonts/wqy-microhei.ttc"

            # fade in
            start, end = start_time, opacity_time + start_time
            for opacity in opacities :
                sub = [((start, end), text)]
                caption = SubtitlesClip(sub, create_generator(fontsize=font_size, font=font, opacity=opacity))\
                        .set_position(("center", y_pos), relative=True)

                start += opacity_time
                end += opacity_time
                scenes.append(caption)

            # stay text
            sub = [((end-SMOOTH_TIME, end_time-END_OPACITY_TIME+SMOOTH_TIME), text)]
            caption = SubtitlesClip(sub, create_generator(fontsize=font_size, font=font))\
                    .set_position(("center", y_pos), relative=True)

            scenes.append(caption)
            
            # for color in ("black", "white") :
            #     if color == "black" : y_pos += 0.003
            #     caption = SubtitlesClip(sub, create_generator(fontsize=font_size, font=font, color=color))\
            #             .set_position(("center", y_pos), relative=True)

            #     scenes.append(caption)
            #     y_pos -= 0.003

        # add audio
        seperate_time = [text[2] for text in texts[:3]]
        video = CompositeVideoClip(scenes)
        for idx, start_time in enumerate(seperate_time) :
            if idx < 2 : clip = video.subclip(start_time, seperate_time[idx+1])
            else : clip = video.subclip(start_time, END_TIME)
            
            if idx > 0 : clip = clip.set_audio(sound)
            clips.append(clip)
    
    # concatenation
    print("[INFO] : Concatenating ...")
    result = concatenate_videoclips(clips)
    result.write_videofile(f"{VIDEO_PATH}.mp4", fps=14, verbose=False, logger=None)
    get_srtfile(f"{VIDEO_PATH}.srt", keeps_sec_subtitle)
    get_vocabtxt(f"{VIDEO_PATH}.txt", keeps_vocabs)

    # remove temp audio files
    files_path = [os.path.join("sounds", name) for name in os.listdir("sounds")]
    [os.remove(path) for path in files_path]
    