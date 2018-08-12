"""
Written by Ari Bornstein 
Wrapper for setting up NeurboParser env with python
"""

import argparse
import os

default_nerbo =  "/opt/dynet/NeurboParser/"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--neurbo_path", default=default_nerbo,
                        help = "Path of cloned Neurbo Repo")
    parser.add_argument("--train_dir", help="Directory for SDP train data")
    parser.add_argument("--test_dir", help="Directory for SDP test data")
    parser.add_argument("--embedding", help="Glove file")

    args = parser.parse_args()

    # prepare sdp splits
    semeval2015_data = os.path.join(args.neurbo_path, 'semeval2015_data')
    os.symlink(args.train_dir, os.path.join(semeval2015_data, 'train'))
    os.symlink(args.test_dir, os.path.join(semeval2015_data, 'test'))
    os.chdir(os.path.join(semeval2015_data, 'scripts'))    
    os.system('./generate_all_splits.sh')

    # prune embeddings
    os.chdir(os.path.join(args.neurbo_path, 'embedding'))    
    os.symlink(args.embedding, os.path.join(os.getcwd(), 'glove.6B.100d.txt'))
    os.system('python prune_embedding.py')
