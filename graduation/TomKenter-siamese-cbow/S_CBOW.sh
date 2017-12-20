#!/bin/sh

THEANO_FLAGS=floatX=float32 python siamese-cbow.py -v -share_weights \
  -vocab ./ppdbutils/ppdbVocabFile.txt -epochs 5 -neg 2 -embedding_size 100 \
  /ppdbutils/ppdb-2.0-tldr.gz output
