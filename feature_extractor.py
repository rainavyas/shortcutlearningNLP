from collections import defaultdict
from utilities.perplexity import perplexity_all
from utilities.unigram import unigram_all

from framework.src.utils.data_utils import load_data

class FeatureExtractor():
    '''
        Defines set of methods for extracting features
    '''
    def __init__(self, sentences):
        self.sentences = sentences
    
    def get_feat(self, feat_name='num_words'):
        if feat_name == 'num_words':
            return self.num_words()
        if feat_name == 'num_chars':
            return self.num_chars()
        if feat_name == 'perplexity':
            return self.perplexity()
        if feat_name == 'unigram':
            return self.unigram()

    def num_words(self):
        return [len(s.split()) for s in self.sentences]
    
    def num_chars(self):
        return [len(s) for s in self.sentences]
    
    def perplexity(self):
        return perplexity_all(self.sentences)

    def unigram(self, train_data_name='imdb'):
        train, dev, test = load_data(train_data_name)
        return unigram_all(self.sentences, train)



class RetentionGenerator(FeatureExtractor):
    '''
        Funtionality:
            - Extract desired feature per sentence
            - Generate retention plot ordered by feature for fraction of class in pred/label
    '''
    def __init__(self, sentences, ys):
        super().__init__(sentences)
        self.ys = ys
    
    def retention_plot(self, features, cum=True, print_feat=False):

        fracs = [(i+1)/len(features) for i,_ in enumerate(features)]
        if print_feat:
            print(features[:100])
            print(sum(self.ys), sum(self.ys[:12500]))

        items = [(f, y) for f,y in zip(features, self.ys)]
        ordered_items = sorted(items, key=lambda x: x[0])
        ordered_ys = [o[1] for o in ordered_items]
        if print_feat:
            # print([o[0] for i,o in enumerate(ordered_items) if i == int(len(ordered_items)/2)])
            # print([o[0] for o in ordered_items[:100]])
            # print(ordered_ys[:100])
            print(sum(ordered_ys), sum(ordered_ys[:12500]))
        


        # retention plot per class
        num_classes = len(set(self.ys))
        pos_class_fracs = defaultdict(list) # key refers to class index
        cum_count = defaultdict(lambda: [0])

        for i, y in enumerate(ordered_ys):
            for c in range(num_classes):
                if y==c:
                    cum_count[c].append(cum_count[c][-1] + 1)
                else:
                    cum_count[c].append(cum_count[c][-1])
                pos_class_fracs[c].append(cum_count[c][-1]/(i+1))

        # temp
        if print_feat:
            print(cum_count[1][:100])

        if cum:
            cum_count_fracs = {}
            for c in range(num_classes):
                cum_count_fracs[c] = [val/cum_count[c][-1] for val in cum_count[c][1:]]
            return fracs, cum_count_fracs
        return fracs, pos_class_fracs

