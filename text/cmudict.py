""" from https://github.com/keithito/tacotron """

import re
from phonemizer.backend import EspeakBackend
from phonemizer.separator import Separator

# https://en.wikipedia.org/wiki/ARPABET
valid_symbols = [
    'AA', 'AA0', 'AA1', 'AA2', 'AE', 'AE0', 'AE1', 'AE2', 'AH', 'AH0', 'AH1', 'AH2',
    'AO', 'AO0', 'AO1', 'AO2', 'AW', 'AW0', 'AW1', 'AW2', 'AY', 'AY0', 'AY1', 'AY2',
    'B', 'CH', 'D', 'DH', 'EH', 'EH0', 'EH1', 'EH2', 'ER', 'ER0', 'ER1', 'ER2', 'EY',
    'EY0', 'EY1', 'EY2', 'F', 'G', 'HH', 'IH', 'IH0', 'IH1', 'IH2', 'IY', 'IY0', 'IY1',
    'IY2', 'JH', 'K', 'L', 'M', 'N', 'NG', 'OW', 'OW0', 'OW1', 'OW2', 'OY', 'OY0',
    'OY1', 'OY2', 'P', 'R', 'S', 'SH', 'T', 'TH', 'UH', 'UH0', 'UH1', 'UH2', 'UW',
    'UW0', 'UW1', 'UW2', 'V', 'W', 'Y', "RR", "NI"
]


# IPA to ARPABET

replacements = {
    'aɪ': 'AA0 Y',
    'aʊ': 'AA0 W',
    'b': 'B',
    'd': 'D',
    'dʒ': 'JH',
    'eɪ': 'EY0',
    'f': 'F',
    'h': 'HH',
    'i': 'IY0',
    'j': 'Y',
    'k': 'K',
    'l': 'L',
    'l̩': 'EL',
    'm': 'M',
    'm̩': 'EM',
    'n': 'N',
    'n̩': 'EN',
    'oʊ': 'OW',
    'p': 'P',
    's': 'S',
    't': 'T',
    'tʃ': 'CH',
    'u': 'UW0',
    'v': 'V',
    'w': 'W',
    'z': 'Z',
    'æ': 'AE0',
    'ð': 'DH',
    'ŋ': 'NG',
    'ɑ': 'AA0',
    'ɔ': 'AO0',
    'ɔɪ': 'OY0',
    'ə': 'AX',
    'ɚ': 'AXR',
    'ɛ': 'EH0',
    'ɝ': 'ER',
    'ɡ': 'G',
    'ɨ': 'IX',
    'ɪ': 'IH0',
    'ɹ': 'R',
    'ɾ': 'R',
    'ɾ̃': 'NX',
    'ʃ': 'SH',
    'ʉ': 'UX',
    'ʊ': 'UH0',
    'ʌ': 'AH0',
    'ʍ': 'WH',
    'ʒ': 'ZH',
    'ʔ': 'Q',
    'θ': 'TH'
}

spanish_replacements = {
    "a": "AA0",
    "o": "OW0",
    "β": "V",
    "e": "EY0",
    "ɲ": "NI",
    "r": "RR",
    "ɣ": "G",
    "ʎ": "SH",
    "x": "HH",
    "ts": "TH",  # jacuzzi / pizza
    "oɪ": "OW0 Y",  # acoitar
    "eʊ": "EY0 W",  # adeuda
    "ʝ": "SH"  # ya
}

replacements = {**replacements, **spanish_replacements}

_valid_symbol_set = set(valid_symbols)


class CMUDict:
    '''Thin wrapper around CMUDict data. http://www.speech.cs.cmu.edu/cgi-bin/cmudict'''

    def __init__(self, lang="es"):
        self.separator = Separator(phone='|', word=None)
        self.backend = EspeakBackend(
            lang, with_stress=True, preserve_punctuation=False)

    def grapheme2ipa(self, word):
        return self.backend.phonemize([word], separator=self.separator)[0].strip().strip("|")

    def ipa2arpabet(self, ipa_word):
        # print(ipa_word)
        ipa_word = ipa_word.replace("ɾ|ɾ", "r")
        if ipa_word.endswith("j|j"):
            ipa_word = ipa_word.replace("j|j", "i")
        else:
            ipa_word = ipa_word.replace("j|j", "ʎ")
        # Remove secondary accents, they are not important in spanish
        ipa_word = ipa_word.replace("ˌ", "")
        # Remove long consonant indication
        ipa_word = ipa_word.replace("ː", "")
        arpabet_word = ""
        for c in ipa_word.split("|"):
            accent = False
            if c.startswith("ˈ"):
                c = c[1:]
                accent = True
            if c in replacements:
                replacement = replacements[c]
                if accent:
                    replacement = replacement.replace("0", "1")
                arpabet_word += replacement + " "
            else:
                print(ipa_word)
                print(f"'{c}' no esta en la lista de replacements")
                raise Exception()
        return "{" + arpabet_word.strip() + "}"

    def word2phonemes(self, word):
        return self.ipa2arpabet(self.grapheme2ipa(word))

    def __len__(self):
        return len(self._entries)

    def lookup(self, word):
        '''Converts word to spainsh adapted ARPAbet'''

        # Apply it only on words, keep punctuation unchanged
        for match in re.findall(r"[A-Za-zÀ-ÿ]+", word):
            word = word.replace(match, self.word2phonemes(match), 1)

        return word
