#!/usr/bin/env python

# Simple feature extractor for CRFsuite. Based on example/ner.py in the
# CRFsuite distribution (https://github.com/chokkan/crfsuite).

import crfutils

import sys
from os import path, getcwd
from collections import OrderedDict

if len(sys.argv) < 4:
    raise RuntimeError("Need to supply paths to train, devel, and test CSVs.")

train_csv = open(path.abspath(path.expanduser(sys.argv[1])), 'r')
devel_csv = open(path.abspath(path.expanduser(sys.argv[2])), 'r')
test_csv = open(path.abspath(path.expanduser(sys.argv[3])), 'r')
trigram_path = path.join(path.dirname(path.dirname(path.realpath(__file__))), 'trigrams')

MODE_TRIGRAMS = {
    1: ["lemma"],
    2: ["lemma", "pos"],
    3: ["lemma", "pos", "soundex"]
}

feature_set = [
    ('word', [[['word', 0]], [['word', -1]], [['word', 1]]]),
    ('lemma', [[['lemma', 0]]]),
    ('soundex', [[['soundex', 0]]]),
    ('pos', [[['pos', 0]]]),
]

for mode, trigrams in MODE_TRIGRAMS.items():

    features = OrderedDict()
    for i in feature_set:
        features[i[0]] = i[1]

    for w, _ in features.items():
        if w in trigrams:
            features[w] = [[[w, -1]], [[w, 0]], [[w, 1]]]

    feature_keys = features.keys()
    feature_items = features.values()
    input_columns = ' '.join(feature_keys) + ' chunk y'

    attribute_templates = []
    for i in feature_items:
        attribute_templates += i

    print("Using features: {}.".format(str(attribute_templates)))

    feature_extractor = lambda x: crfutils.apply_templates(x, attribute_templates)

    for fi, txt in [(train_csv, "train"), (devel_csv, "devel"), (test_csv, "test")]:
        write_to = path.join(trigram_path, txt + "_trigrams_" + str(mode) + ".crfsuite")
        fo = open(write_to, "w+")
        print("Writing to {}...".format(write_to))
        crfutils.main(feature_extractor, fi, fo, fields=input_columns, sep='\t')
        fo.close()

train_csv.close()
devel_csv.close()
test_csv.close()