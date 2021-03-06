import base64, secrets

from django.core.files.base import ContentFile
from wordfreq import *
from googletrans import Translator


def get_file_from_data_url(data_url):
    _format, _dataurl = data_url.split(';base64,')
    _filename, _extension = secrets.token_hex(20), _format.split('/')[-1]

    file = ContentFile(base64.b64decode(_dataurl), name=f"{_filename}.{_extension}")

    return file, (_filename, _extension)


def process_sub(text, file_type, score):
    important_words = {}
    words_difficulty = {}
    score = (1-score) * max_zipf()
    if file_type in '.srt' or file_type in '.ass' or file_type in 'x-ssa':
        text = text.decode('iso-8859-1')
        text = text.split('\r\n\r\n')
        for i, segment in enumerate(text):
            segment = segment.split('\r\n')[2:]
            for line in segment:
                line = tokenize(line, 'en')
                for word in line:
                    _freq = zipf_frequency(word, 'en')
                    if score / 1.05 < _freq < score * 1.1 and word not in important_words:
                        important_words[word] = i
                        words_difficulty[word] = _freq
        translator = Translator()
        ready_words = list(important_words.keys())
        result = translator.translate(ready_words, src='en', dest='fa')
        modified_segments = {}
        for res in result:
            seg_num = important_words[res.origin]
            if seg_num in modified_segments:
                modified_segments[seg_num].append([res.origin, res.text])
            else:
                modified_segments[seg_num] = [[res.origin, res.text]]
        new_text = ""
        for i, segment in enumerate(text):
            if i in modified_segments:
                to_add = []
                for word, trans in modified_segments[i]:
                    segment = segment.replace(word, '<font color="yellow">{0}</font>'.format(word), 1)
                    to_add.append("{0}:{1}".format('<font color="yellow">{0}</font>'.format(word), trans))
                to_add = "({0})".format(" ".join(to_add))
                new_text += segment
                new_text += "\r\n"
                new_text += to_add
                new_text += "\r\n\r\n"
            else:
                new_text += segment
                new_text += "\r\n\r\n"
        answer = [[res.origin, res.text, words_difficulty[res.origin]] for res in result]
        return answer, new_text


def max_zipf():
    return zipf_frequency('the', 'en')


def exam_list(num_words=50):
    boundaries = [0, 3, 4, 5, float('Inf')]
    samples_cnt = [0, min(25, num_words//4), min(25, num_words//4), min(15, num_words//4)]
    samples_cnt[0] = num_words - sum(samples_cnt)
    zipf_dict = {x:freq_to_zipf(y) for x, y in get_frequency_dict('en').items()}
    words_by_section = [[x for x, y in zipf_dict.items() if boundaries[i] < y <= boundaries[i+1]] for i in range(len(boundaries)-1)]

    exam_words = []
    secure_random = secrets.SystemRandom()
    for i in range(len(words_by_section)):
        exam_words.extend(secure_random.sample(words_by_section[i], samples_cnt[i]))

    return exam_words


def score_by_exam(words, answered):
    # answered[i]:boolean shows that user knows the i-th word
    out_of_score = 0.0
    scored = 0.0
    for i, word in enumerate(words):
        out_of_score += zipf_frequency(word, 'en')
        scored += zipf_frequency(word, 'en') if answered[i] else 0
    
    return scored / out_of_score

"""
def next_score(cur_score):
    checkpoints = [0.2, 0.4, 0.6, 0.8, 1.0]
    for sc in checkpoints:
        if cur_score < sc:
            return sc
"""
