# pyNeurboParser
A python wrapper for the [NeurboParser](https://github.com/Noahs-ARK/NeurboParser) lib 

## Prerequites
    - Docker

## Setup
        1. Clone the pyNeurboParser Repo
        2. Run the pyNeurboParser container
        ```
        docker run -it -v path_to_repo:/data/ -p 5000:5000 abornst/py-neurbo-parser
        ```

## Usage 
    - Command Line

        In the container run the following command to evaluate the model
        ```
        python /data/src/SDP_eval.py  --pruner "Path to pruner model" --model "Path to SDP model --pred Path to prediction output --text "Text to be parsed"
        ```

    - Programatic

        ```python
            sys.path.append("/data/src/")
            from SDP_eval import semantic_parse

            json_parse = semantic_parse(text, parser_path, pruner_path, data_file, model_path, prediction_path)
        ```

### Training    
    1. Run setup (note you only have to do this once)
    ```
    python /data/src/SDP_setup.py --train_dir "Directory for SDP train data" --test_dir "Directory for SDP test data" --embedding "Glove file"
    ```

    2. Run train script 
    ```
    python /data/src/SDP_train.py --model "Path to write models" --pred "Path to write predictions" --log "Path to write logs"
	--language "Parser Language" --form "Desired SDP formalism"
    ```

## Demo
An example usage of this wrapper in a flask application can be found in the demo app

## References
	
[1] Hao Peng, Sam Thomson, and Noah A. Smith. 2017. 
Deep Multitask Learning for Semantic Dependency Parsing
In Proceedings of the Annual Meeting of the Association for Computational Linguistics (ACL).
	
[2] André F. T. Martins, Miguel B. Almeida, Noah A. Smith. 2013. 
Turning on the Turbo: Fast Third-Order Non-Projective Turbo Parsers. 
In Proceedings of the Annual Meeting of the Association for Computational Linguistics (ACL).
	
[3] Jeffrey Pennington, Richard Socher, and Christopher D. Manning. 2014. 
GloVe: Global Vectors for Word Representation. 
In Proceedings of the Empirical Methods in Natural Language Processing (EMNLP).

[4] André F. T. Martins and Mariana S. C. Almeida. 2014.
Priberam: A Turbo Semantic Parser with Second Order Features.
In Proceedubgs of the International Workshop on Semantic Evaluation (SemEval), task 8: Broad-Coverage Semantic Dependency Parsing.

[5] Mariana S. C. Almeida and André F. T. Martins. 2015.
Lisbon: Evaluating TurboSemanticParser on Multiple Languages and Out-of-Domain Data.
In Proceedings of International Workshop on Semantic Evaluation (SemEval'15), task 18: Broad Coverage Semantic Dependency Parsing.
