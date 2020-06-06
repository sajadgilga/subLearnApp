import base64, secrets

from django.core.files.base import ContentFile
from wordfreq import zipf_frequency, tokenize
from googletrans import Translator


def get_file_from_data_url(data_url):
    _format, _dataurl = data_url.split(';base64,')
    _filename, _extension = secrets.token_hex(20), _format.split('/')[-1]

    file = ContentFile(base64.b64decode(_dataurl), name=f"{_filename}.{_extension}")

    return file, (_filename, _extension)


def process_sub(text, file_type, score):
    important_words = {}
    if file_type in '.srt' or file_type in '.ass' or file_type in 'x-ssa':
        text = text.decode('iso-8859-1')
        text = text.split('\r\n\r\n')
        for i, segment in enumerate(text):
            segment = segment.split('\r\n')[2:]
            for line in segment:
                line = tokenize(line, 'en')
                for word in line:
                    _freq = zipf_frequency(word, 'en')
                    if score / 1.05 < _freq < score * 1.2 and word not in important_words:
                        important_words[word] = i
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
        answer = [[res.origin, res.text] for res in result]
        return answer, new_text
