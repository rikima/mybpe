import re, collections
from collections import defaultdict 

class BPE(object):

  def __init__(self):
    self.vocab = defaultdict(int)
    self.EOW = "</w>"


  def get_stats(self):
    pairs = collections.defaultdict(int) 
    for word, freq in self.vocab.items():
      symbols = word.split()
      for i in range(len(symbols)-1):
        pairs[symbols[i],symbols[i+1]] += freq 
  
    return pairs
  

  def merge_vocab(self, pair):
    v_out = {}
    bigram = re.escape(' '.join(pair))
    p = re.compile(r'(?<!\S)' + bigram + r'(?!\S)') 
    for word in self.vocab:
      w_out = p.sub(''.join(pair), word)
      v_out[w_out] = self.vocab[word] 
    return v_out


  def build_vocab(self, sentences):
    for i, sentence in enumerate(sentences):
      for word in sentence.split():
        word = " ".join(list(word)) + " " + self.EOW
        self.vocab[word] += 1
    

  def train(self, sentences, num_merges=10):
    self.build_vocab(sentences)
    for i in range(num_merges):
      pairs = self.get_stats()
      best = max(pairs, key=pairs.get) 
      self.vocab = self.merge_vocab(best) 
    
    return self.vocab


if __name__ == '__main__':
    sentences = [
        "low low low low low",
        "lower lower",
        "newest newest newest newest newest newest",
        "widest widest widest"
    ]
    
    bpe = BPE()
    vocab = bpe.train(sentences)
    
    print(vocab)
