"""
Written by Ari Bornstein
Wrapper for evaluating NeurboParser models with python
Run in the context of the contained Dockerfile
"""
import argparse
import spacy
import os
import json
from conllu import parse
import subprocess

nlp = spacy.load('en', vectors=False)


def parse_cmd(parser_file, pruner_model, data_file, model_file, prediction):
    return "%s --test \
                --file_test=%s \
                --srl_file_pruner_model=%s \
                --srl_file_format=sdp \
                --logtostderr \
                --file_model=%s \
                --file_prediction=%s" % (
                    parser_file,
                    data_file,
                    pruner_model,
                    model_file,
                    prediction
                )


def semantic_parse(text, parser_file, pruner_model,
                   data_file, model_file, prediction):
    """
    Parses semantic dependency graph from a string of sentences
    Requires a pruner and parser file
    """
    doc = nlp(text)

    f = open(data_file, "w+")
    for sent in doc.sents:
        for i, word in enumerate(sent):
            f.write("%d\t%s\t%s\t%s\n" % (
                i+1,  # There's a word.i attr that's position in *doc*
                word,
                word.lemma_,  # Lemma
                word.tag_,))
        f.write("\n")
    f.write("\n")
    f.close()

    process = subprocess.Popen(parse_cmd(parser_file, pruner_model,
                                         data_file, model_file, prediction),
                               shell=True, stderr=subprocess.PIPE)
    process.wait()

    # update this with direct pipe from output
    with open(prediction, 'r') as myfile:
        data = myfile.read()
    sentences = parse(data)
    return json.dumps({"original text": text,
                       "parse": [ob.__dict__ for ob in sentences]})

if __name__ == "__main__":

    default_neurbo = "/opt/dynet/NeurboParser/"
    parser = argparse.ArgumentParser()
    parser.add_argument("--neurbo_path", default=default_neurbo,
                        help="Path of cloned Neurbo Repo")
    parser.add_argument("--pruner", help="Path to pruner model")
    parser.add_argument("--model", help="Path to SDP model")
    parser.add_argument("--pred", help="Path to prediction output")
    parser.add_argument("--text", help="Text to be parsed")

    args = parser.parse_args()

    parser_file = os.path.join(args.neurbo_path,
                               'NeurboParser/build/neurboparser')
    data_file = os.path.join(os.getcwd(), 'data.sdp')
    print(semantic_parse(unicode(args.text, "utf-8"), parser_file,
          args.pruner, data_file, args.model, args.pred))
