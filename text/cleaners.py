""" from https://github.com/keithito/tacotron """

'''
Cleaners are transformations that run over the input text at both training and eval time.

Cleaners can be selected by passing a comma-delimited list of cleaner names as the "cleaners"
hyperparameter. Some cleaners are English-specific. You'll typically want to use:
  1. "english_cleaners" for English text
  2. "transliteration_cleaners" for non-English text that can be transliterated to ASCII using
     the Unidecode library (https://pypi.python.org/pypi/Unidecode)
  3. "basic_cleaners" if you do not want to transliterate (in this case, you should also update
     the symbols in symbols.py to match your data).
'''

import re
import random
from unidecode import unidecode
from .numbers import normalize_numbers
from .cmudict import CMUDict

_cmudict = CMUDict()

_arpabet_split_re = re.compile(r'[^\s]*{.*?}[^\s]*|[^\s]+', re.UNICODE)
# Regular expression matching whitespace:
_whitespace_re = re.compile(r'\s+')

# List of (regular expression, replacement) pairs for abbreviations:
_abbreviations = [(re.compile('\\b%s\\.' % x[0], re.IGNORECASE), x[1]) for x in [
  ('srs', 'señores'),
  ('sr', 'señor'),
  ('dr', 'doctor'),
  ('drs', 'doctores'),
  ('jr', 'yunior'),
]]


def expand_abbreviations(text):
  for regex, replacement in _abbreviations:
    text = re.sub(regex, replacement, text)
  return text


def expand_numbers(text):
  return normalize_numbers(text)


def lowercase(text):
  return text.lower()


def collapse_whitespace(text):
  return re.sub(_whitespace_re, ' ', text)


def convert_to_ascii(text):
  return unidecode(text)

def maybe_get_arpabet(word): # https://github.com/keithito/tacotron/blob/master/datasets/datafeeder.py
  arpabet = _cmudict.lookup(word)
  return arpabet

def basic_cleaners(text):
  '''Basic pipeline that lowercases and collapses whitespace without transliteration.'''
  text = expand_numbers(text)
  text = expand_abbreviations(text)
  text = collapse_whitespace(text)
  return text

def transliteration_cleaners(text):
  '''Pipeline for non-English text that transliterates to ASCII.'''
  text = convert_to_ascii(text)
  text = lowercase(text)
  text = collapse_whitespace(text)
  return text

def cmudict_cleaners(text):
  text = basic_cleaners(text)
  text = ' '.join([maybe_get_arpabet(word) for word in _arpabet_split_re.findall(text)])
  return text