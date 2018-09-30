"""
Written by Ari Bornstein
Wrapper for training NeurboParser models with python
Run in the context of the contained Dockerfile or equivlent enviorment
"""

import os
import argparse
import subprocess


def train(parser_file, train_epochs, pruner_epochs, file_train,
          file_dev, file_pruner_model, use_pretrained_embedding,
          file_pretrained_embedding, lemma_dim, word_dim, pos_dim,
          lstm_dim, mlp_dim, num_lstm_layers, use_word_dropout,
          word_dropout_rate, trainer, srl_train_cost_false_positives,
          srl_train_cost_false_negatives, file_model, file_prediction,
          log_file):

    train_cmd = "%s --train --evaluate \
                    --dynet_mem 512 \
                    --dynet_seed 823632965 \
                    --dynet_weight_decay 1e-6 \
                    --train_epochs=%s  \
                    --pruner_epochs=%s \
                    --file_train=%s \
                    --file_test=%s \
                    --srl_labeled=true \
                    --srl_deterministic_labels=true \
                    --srl_use_dependency_syntactic_features=false \
                    --srl_prune_labels_with_senses=false \
                    --srl_prune_labels=true \
                    --srl_prune_distances=true \
                    --srl_prune_basic=true \
                    --srl_train_pruner=true \
                    --srl_file_pruner_model=%s \
                    --srl_pruner_posterior_threshold=0.0001 \
                    --srl_pruner_max_arguments=20 \
                    --form_case_sensitive=false \
                    --srl_model_type=af \
                    --srl_allow_self_loops=false \
                    --srl_allow_root_predicate=true \
                    --srl_allow_unseen_predicates=false \
                    --srl_use_predicate_senses=false \
                    --srl_file_format=sdp \
                    --use_pretrained_embedding=%s \
                    --file_pretrained_embedding=%s \
                    --lemma_dim=%s \
                    --word_dim=%s \
                    --pos_dim=%s \
                    --lstm_dim=%s \
                    --mlp_dim=%s \
                    --num_lstm_layers=%s \
                    --use_word_dropout=%s \
                    --word_dropout_rate=%s \
                    --trainer=%s \
                    --srl_train_cost_false_positives=%s \
                    --srl_train_cost_false_negatives=%s \
                    --logtostderr \
                    --file_model=%s \
                    --file_prediction=%s \
                    2>&1 | tee %s \
                    " % (
                        parser_file,
                        train_epochs,
                        pruner_epochs,
                        file_train,
                        file_dev,
                        file_pruner_model,
                        use_pretrained_embedding,
                        file_pretrained_embedding,
                        lemma_dim,
                        word_dim,
                        pos_dim,
                        lstm_dim,
                        mlp_dim,
                        num_lstm_layers,
                        use_word_dropout,
                        word_dropout_rate,
                        trainer,
                        srl_train_cost_false_positives,
                        srl_train_cost_false_negatives,
                        file_model,
                        file_prediction,
                        log_file)
    process = subprocess.Popen(train_cmd, shell=True, stderr=subprocess.PIPE)
    process.wait()


if __name__ == "__main__":

    default_neurbo = "/opt/dynet/NeurboParser/"

    parser = argparse.ArgumentParser()
    parser.add_argument("--neurbo_path", default=default_neurbo,
                        help="Path of cloned Neurbo Repo")
    parser.add_argument("--model", help="Path to write models")
    parser.add_argument("--pred", help="Path to write predictions")
    parser.add_argument("--log", help="Path to write logs")
    parser.add_argument("--language", help="Parser Language")
    parser.add_argument("--form", help="Desired SDP formalism", required=True)
    args = parser.parse_args()

    trainer = "adadelta"
    train_epochs = 100
    pruner_epochs = 1
    lemma_dim = 25
    word_dim = 100
    pos_dim = 25
    mlp_dim = 100
    lstm_dim = 200
    num_lstm_layers = 2
    use_pretrained_embedding = 'true'
    use_word_dropout = 'true'
    word_dropout_rate = 0.25
    srl_train_cost_false_positives = 0.4
    srl_train_cost_false_negatives = 0.6

    parser_file = os.path.join(args.neurbo_path,
                               'NeurboParser/build/neurboparser')
    file_pretrained_embedding = os.path.join(args.neurbo_path,
                                             'embedding/glove.100.pruned')
    form_path = os.path.join(args.neurbo_path,
                             'semeval2015_data/%s/data' % args.form)
    file_train = os.path.join(form_path,
                              'english/english_%s_augmented_train.sdp'
                              % args.form)
    file_dev = os.path.join(form_path,
                            'english/english_%s_augmented_dev.sdp'
                            % args.form)
    file_test = os.path.join(form_path,
                             'english/english_id_%s_augmented_test.sdp'
                             % args.form)
    file_model = os.path.join(args.model,
                              '%s.%s.lstm%s.layer%s.h%s.drop%s.model' % (
                                args.form,
                                trainer,
                                lstm_dim,
                                num_lstm_layers,
                                mlp_dim,
                                word_dropout_rate))

    file_pruner_model = os.path.join(args.model, '%s_%s.pruner.model' % (
        args.language,
        args.form
    ))
    file_prediction = os.path.join(args.pred,
                                   '/%s.%s.lstm%s.layer%s.h%s.drop%s.pred' % (
                                    args.form,
                                    trainer,
                                    lstm_dim,
                                    num_lstm_layers,
                                    mlp_dim,
                                    word_dropout_rate))

    log_file = os.path.join(args.log, '%s.%s.lstm%s.layer%s.h%s.drop%s.log' % (
        args.form,
        trainer,
        lstm_dim,
        num_lstm_layers,
        mlp_dim,
        word_dropout_rate))

    train(parser_file, train_epochs, pruner_epochs, file_train,
          file_dev, file_pruner_model, use_pretrained_embedding,
          file_pretrained_embedding, lemma_dim, word_dim, pos_dim,
          lstm_dim, mlp_dim, num_lstm_layers, use_word_dropout,
          word_dropout_rate, trainer, srl_train_cost_false_positives,
          srl_train_cost_false_negatives, file_model, file_prediction,
          log_file)
