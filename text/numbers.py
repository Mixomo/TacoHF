""" from https://github.com/keithito/tacotron """

import re
import num2words

_inflect = num2words
_comma_number_re = re.compile(r'([0-9][0-9\,]+[0-9])')
_decimal_number_re = re.compile(r'([0-9]+\,[0-9]+)')
_euros_re = re.compile(r'€([0-9\,]*[0-9]+)')
_dollars_re = re.compile(r'\$([0-9\.\,]*[0-9]+)')
_ordinal_re = re.compile(r'[0-9]+(\º|\ª|er|do|os|as)')
_number_re = re.compile(r'[0-9]+')


def _remove_commas(m):
  return m.group(1).replace('.', '')


def _expand_decimal_point(m):
  return m.group(1).replace(',', ' coma ')


def _expand_dollars(m):
  match = m.group(1)
  parts = match.split('.')
  if len(parts) > 2:
    return match + ' dólares'  # Unexpected format
  dollars = int(parts[0]) if parts[0] else 0
  cents = int(parts[1]) if len(parts) > 1 and parts[1] else 0
  if dollars and cents:
    dollar_unit = 'dólares' if dollars == 1 else 'dólares'
    cent_unit = 'centavo' if cents == 1 else 'centavos'
    return '%s %s, %s %s' % (dollars, dollar_unit, cents, cent_unit)
  elif dollars:
    dollar_unit = 'dólares' if dollars == 1 else 'dólares'
    return '%s %s' % (dollars, dollar_unit)
  elif cents:
    cent_unit = 'centavo' if cents == 1 else 'centavos'
    return '%s %s' % (cents, cent_unit)
  else:
    return 'cero dólares'


def _expand_ordinal(m):
  return _inflect.num2words(m.group(0), to='ordinal',lang="es")

def _expand_number(m):
  num = int(m.group(0))
  return _inflect.num2words(num,lang="es")

def normalize_numbers(text):
  text = re.sub(_comma_number_re, _remove_commas, text)
  text = re.sub(_euros_re, r'\1 euros', text)
  text = re.sub(_dollars_re, _expand_dollars, text)
  text = re.sub(_decimal_number_re, _expand_decimal_point, text)
  text = re.sub(_ordinal_re, _expand_ordinal, text)
  text = re.sub(_number_re, _expand_number, text)
  return text
