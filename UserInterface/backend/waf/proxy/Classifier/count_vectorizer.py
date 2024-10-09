# Existing imports
from collections import Counter
import re
from scipy.sparse import csr_matrix

class SimpleCountVectorizer:
    def __init__(self):
        self.vocabulary = {}
        self.vocab_size = 0

    def fit(self, texts):
        word_count = Counter()
        for text in texts:
            words = self._tokenize(text)
            word_count.update(words)
        
        self.vocabulary = {word: idx for idx, (word, _) in enumerate(word_count.most_common())}
        self.vocab_size = len(self.vocabulary)

    def transform(self, texts):
        rows, cols, data = [], [], []
        for row, text in enumerate(texts):
            word_counts = Counter(self._tokenize(text))
            for word, count in word_counts.items():
                if word in self.vocabulary:
                    col = self.vocabulary[word]
                    rows.append(row)
                    cols.append(col)
                    data.append(count)
        return csr_matrix((data, (rows, cols)), shape=(len(texts), self.vocab_size))

    def fit_transform(self, texts):
        self.fit(texts)
        return self.transform(texts)

    def _tokenize(self, text):
        return re.findall(r'\b\w+\b', text.lower())