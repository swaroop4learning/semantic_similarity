from nltk.tokenize import word_tokenize
import pandas as pd
import shap

from sts_models.sbert_model import SBertModel, SBertModel_Custom


class STSWrapper():
    def __init__(self, sts_model, tokenizer='nltk'):
        self.sts_model = sts_model
        if tokenizer == 'nltk':
            self.tokenizer = word_tokenize
        elif tokenizer == 'split':
            self.tokenizer = self._split_tokenizer

    def _split_tokenizer(self, sent):
        return sent.split()

    def __call__(self, sent_pair_list):
        batch = []
        for pair in sent_pair_list:
            s1, s2 = pair[0].split('[SEP]')
            batch.append((s1, s2))

        scores = self.sts_model(batch)
        return scores

    def _tokenize_sent(self, sentence):
        if isinstance(sentence, str):
            # token_ids = self.sts_model.tokenizer.encode(sentence)
            # tokens = self.sts_model.tokenizer.convert_ids_to_tokens(token_ids)[1:-1]
            tokens = self.tokenizer(sentence)
        elif isinstance(sentence, list):
            tokens = sentence

        return tokens

    def build_feature(self, sent1, sent2):
        tokens1 = self._tokenize_sent(sent1)
        tokens2 = self._tokenize_sent(sent2)
        self.s1len = len(tokens1)
        self.s2len = len(tokens2)

        tdict = {}
        for i in range(len(tokens1)):
            tdict['s1_{}'.format(i)] = tokens1[i]
        for i in range(len(tokens2)):
            tdict['s2_{}'.format(i)] = tokens2[i]

        return pd.DataFrame(tdict, index=[0])

    def mask_model(self, mask, x):
        #input from shap:  mask  is [False False False False False  True] for x  ['He' 'hates' 'apples' 'He' 'likes' 'apples']
        tokens = []
        for mm, tt in zip(mask, x):
            if mm:
                tokens.append(tt)
            else:
                tokens.append('[MASK]')
        s1 = ' '.join(tokens[:self.s1len])
        s2 = ' '.join(tokens[self.s1len:])
        sentence_pair = pd.DataFrame([s1 + '[SEP]' + s2])
        return sentence_pair


class ExplainableSTS():
    def __init__(self, wanted_sts_model):
        if wanted_sts_model == 'sbert':
            #sts_model = SBertModel()
            sts_model = SBertModel_Custom()

        self.wrapper = STSWrapper(sts_model)

    def __call__(self, sent1, sent2):
        s1 = ' '.join(self.wrapper.tokenizer(sent1))
        s2 = ' '.join(self.wrapper.tokenizer(sent2))
        return self.wrapper.sts_model([(s1, s2)])[0]

    def explain(self, sent1, sent2, plot=False):
        explainer = shap.Explainer(self.wrapper, self.wrapper.mask_model)
        value = explainer(self.wrapper.build_feature(sent1, sent2))
        if plot: shap.waterfall_plot(value[0])
        all_tokens = []
        all_tokens += ['s1_' + t for t in self.wrapper.tokenizer(sent1)]
        all_tokens += ['s2_' + t for t in self.wrapper.tokenizer(sent2)]

        return [(token, sv) for token, sv in zip(all_tokens, value[0].values)]
