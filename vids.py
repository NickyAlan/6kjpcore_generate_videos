from utils import *
import pandas as pd
from random import randint
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.editor import AudioFileClip, ImageClip, CompositeVideoClip, concatenate_videoclips

if __name__ == '__main__' :
    # read jp6kcore.csv
    start_vocab_idx = 169
    num_vocabs = 10
    vocabs = pd.read_csv('./jp6kcore.csv', encoding='utf-8-sig')
    print(f'\n   generating: {num_vocabs} vocabs\n   from: {start_vocab_idx} to {start_vocab_idx + num_vocabs - 1}')

    for vocab_idx in range(start_vocab_idx, start_vocab_idx + num_vocabs) :
        
        vocab_detail = vocabs.iloc[vocab_idx]
        vocab = vocab_detail['kanji']

        # download sounds
        print(f'\n\t[{vocab_idx}] vocab: {vocab_detail["romaji"]}')
        print(f'\t: {vocab_detail["translate"]}')
        download_from_url(vocab_detail['sound_url'], 'sounds/sound.mp3')
        download_from_url(vocab_detail['sentence_sound_url'], 'sounds/sentence_sound.mp3')
        
        # timeline: sound/1 sec/sound/0.5 sec
        sound = AudioFileClip('sounds/sound.mp3')
        st_sound = AudioFileClip('sounds/sentence_sound.mp3')
        frame1_sec = (0, (sound.duration*2) + 1.5)
        frame2_sec = (frame1_sec[-1], frame1_sec[-1] + (st_sound.duration*2) + 1.5)
        
        # background image
        bg_images = ['media/bg_v1.jpg', 'media/bg_v2.jpg', 'media/bg_v3.jpg']
        bg_random = bg_images[randint(0, len(bg_images) - 1)]
        # bg_random = bg_images[2]
        bg_image = ImageClip(img = bg_random, duration=frame2_sec[-1])
        bg_image = bg_image.resize((576, 576))
        color_dict = {'media/bg_v1.jpg': ['yellow', 'white', '#36332d'], 
                      'media/bg_v2.jpg': ['yellow', 'white', '#36332d'],
                      'media/bg_v3.jpg': ['purple', 'white', '#36332d'],}
        color_c = color_dict[bg_random]

        # 1st frame/scence
        frame1 = ['kanji', 'hira', 'romaji', 'translate']
        vocab_length = vocab_detail[frame1[:-1]].str.len().max()
        translate_length = len(vocab_detail[frame1[-1]])
        max_, top = get_max_top(vocab_length)
        
        captions = [bg_image]
        fontsize_tup = ('l', 'm', 'm', 's')
        fontsize_dict1 = create_fontsize(vocab_length, translate_length, max_ = max_)
        ypos1 = get_ypos(fontsize_dict1, top=top)

        for pos_idx, (key, f) in enumerate(zip(frame1, fontsize_tup), start=1) :
            text = vocab_detail[key]
            bg_color = 'transparent'
            color = color_c[0] if key == 'kanji' else color_c[1]
            fontsize = fontsize_dict1[f]
            y = ypos1[f'{pos_idx}']
            
            if key == 'translate' :
                if len(text) >= 34:
                    texts = text.split(',')
                    fontsize += (fontsize * .3)
                    y += (fontsize * 2.2)
                    if len(texts) > 1 :
                        text = '\n/'.join(texts)
                    else :
                        n = len(texts)
                        text = ' '.join(texts[:n//2]) + '\n' + ' '.join(texts[n//2: ])

                font = 'fonts/Cubano.ttf'
                bg_color = color_c[2]
            else : 
                font = 'fonts/wqy-microhei.ttc'
                bg_color = 'transparent'
            
            sub = [(frame1_sec, text)]
            caption = SubtitlesClip(sub, create_generator(fontsize, font, color, bg_color))\
                .set_position(('center', y))
            
            captions.append(caption)

        # 2nd frame/scence
        frame2 = ['sentence', 'sentence_hira', 'sentence_translate']
        sentence_length = vocab_detail[frame2[:-1]].str.len().max()
        st_translate_length = len(vocab_detail[frame2[-1]])
        sentence_length, st_translate_length
        max_ = get_max_st(sentence_length)

        fontsize_tup = ('m', 'm', 's')
        fontsize_dict2 = create_fontsize(sentence_length, st_translate_length, max_ = max_)
        ypos2 = get_ypos(fontsize_dict2, top = 144)
        
        for pos_idx, (key, f) in enumerate(zip(frame2, fontsize_tup), start=2) :
            text = vocab_detail[key]
            bg_color = 'transparent' 
            color = color_c[0] if key == 'sentence' else color_c[1]
            fontsize = fontsize_dict2[f]
            y = ypos2[f'{pos_idx}']

            if key == 'sentence_translate' :
                text = text[:-1] 
                if len(text) > 36 :
                    fontsize *= 1.8
                    y += (fontsize * 5)
                    texts = text.split(',')
                    if len(texts) > 1 :
                        text = '\n'.join(texts)
                    else :
                        texts = text.split(' ')
                        n = len(texts)
                        text = ' '.join(texts[:n//2]) + '\n' + ' '.join(texts[n//2: ])

                font = 'fonts/Cubano.ttf'
                bg_color = color_c[2]
            else :
                text = text.replace(' ','').replace('<b>', ' ').replace('</b>', ' ').replace('。', '')
                if len(text) > 36 :
                    texts = text.split('、')
                    if len(texts) > 1 :
                        fontsize += (fontsize*.3)
                        if key == 'sentence_hira' :
                            y += (fontsize * 2) 

                    text = '\n'.join(texts)
                
                font = 'fonts/wqy-microhei.ttc'
                bg_color = 'transparent'
                
            sub = [(frame2_sec, text)]
            caption = SubtitlesClip(sub, create_generator(fontsize, font, color, bg_color))\
            .set_position(('center', y))
            
            captions.append(caption)

        # combined video and audio
        audio1_sec = sound.duration
        audio2_sec = st_sound.duration
        seconds1 = frame1_sec
        seconds2 = frame2_sec

        seperate_sec1 = [(0, audio1_sec), (audio1_sec, audio1_sec+1), (audio1_sec+1, seconds1[-1])]
        seperate_sec2 = [(seconds2[0], seconds2[0] + audio2_sec),\
                         (seconds2[0] + audio2_sec, seconds2[0] + audio2_sec + 1), \
                         (seconds2[0] + audio2_sec + 1, seconds2[-1])]
        seperate_sec = seperate_sec1 + seperate_sec2 

        clips = []
        video = CompositeVideoClip(captions)
        for idx, (s1, s2) in enumerate(seperate_sec) :
            clip = video.subclip(s1, s2)
            if idx == 0 or idx == 2 :
                clip = clip.set_audio(sound)
            elif idx == 3 or idx == 5 :
                clip = clip.set_audio(st_sound)
            clips.append(clip)

        # render complete video
        result = concatenate_videoclips(clips)
        save_name = f'videos/{vocab} - {vocab_detail["romaji"]} - {vocab_detail["translate"]}.mp4'
        result.write_videofile(save_name, fps=24, verbose=False, logger=None)
        print(f'\tsaved: {vocab_detail["romaji"]}')
