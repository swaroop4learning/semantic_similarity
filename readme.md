# Project: Semantic Textual Similarity (STS) 

## About
This repository consists of STS score generation and various experiments conducted to support mono-lingual and cross-lingual embeddings.
The quality of the sentence embeddings is validated against validation data by assessing the MSE score and detailed report is present in report.pdf

## Project files
<li>run_similarity_score_en.py consists of main driver code to generate STS scores for mono lingual sentences </li>
<li>run_similarity_score_en_es.py consists of main driver code to generate STS scores for cross lingual sentences </li>
<li>Data folder has the raw data, cleaned data and pretrained model files</li>
<li>Experiments folder have reproducible training source code for various approaches experimented:
<ul>
    <li>Word2Vec-STS.ipynb: Generate Word2vec embeddings for given corpus and average the embeddings to create sentence embeddings and apply following approaches for STS scores generation</li>
    <li>BILSTM_Sentence_Encoder.ipynb: Sentence Embeddings with BiLSTM-The cleaned sentences are padded and applied through encoder decoder model to generate sentence embeddings of equal size. The embeddings are optimized to fit MLP based regression model</li>
    <li>Do2Vec.ipynb: Doc2Vec model is trained to generate representative embeddings of sentences</li>
    <li>BERT.ipynb: SOTA The pretrained SBERT embeddings which are fine tuned on STS dataset are used for generating sentence embeddings</li>
    <li>Siamese_BiLSTM_w2v.ipynb: The pretrained word2vec embeddings are fed as input layers to bi-directional lstm to generate similarity scores</li>
    <li>Cross_Lingual_Training.ipynb: This notebook consists of code to preprocess non english text and run through various model architectures to generate cross lingual semantic similarity scores</li>
</ul>
</li>
<li>sts_explainability.ipynb: This module helps in explaining which words or set of words are playing major role in the STS score for a given sentence pair through SHAP values</li>

## Execution
When the `run_similarity_score_en.py` file is run, it uses the command-line arguments . It prints a prompt asking for two sentences and then prints the predicted STS score for the sentence pair.

Make sure you are in the src directory after unzipping
```
> python run_similarity_score_en.py
Enter your first sentence:      Where is Swaroop going
Enter your second sentence:     Swaroop is leaving to college now
Generating the similarity score......
The semantic similarity score is 4.338752180337906
The explainability can be generated through sts_explainability module 
```

```
> python run_similarity_score_en_es.py
Enter your english sentence:	A man is playing a flute.
Enter your spanish sentence:	Un hombre está tocando una flauta de bambú.
Generating the cross lingual similarity score......
The predicted semantic similarity score is  2.534799337387085
```

## Dependencies
create virtual environment of Python 3.9 version and install dependencies from requirements.txt to reproduce

## Contact
Contact author for any queries to reproduce the results

## References:
<li>Hugging face datasets</li>
<li>Efficient Estimation of Word Representation in vector space</li>
<li>https://github.com/yg211/explainable-metrics</li>



