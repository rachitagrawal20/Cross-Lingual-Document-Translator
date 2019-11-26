#Importing necessary libraries
import math
from collections import defaultdict

#constants
MIN_PROB = 1.0e-12

'''
  EM maximization step - updates probabilities with maximum likelihood estimate
'''

#initialises the vocabulary sets for src and trg language
def init_vocab(corpus, src_vocab, trg_vocab, lang_a, lang_b):
        for sentence in corpus:
            trg_vocab.update(sentence[lang_a].split())
            src_vocab.update(sentence[lang_b].split())
        # Add the NULL token
        src_vocab.add(None)
        src_vocab.add(None)

#initialises the translation table probabilties and sets it to 1/(no. of unique words in trg language vocabulary)
def set_initial_probabilities(corpus, translation_table, lang_a, lang_b):
        src_vocab = set()
        trg_vocab = set()
        init_vocab(corpus, src_vocab, trg_vocab, lang_a, lang_b)
        initial_prob = 1 / len(trg_vocab)

        for t in trg_vocab:
            translation_table[t] = defaultdict(lambda: initial_prob)

#returns probability of src language word 's' being translated to trg language word 't'
def prob_alignment_point(source, target, translation_table):
        return translation_table[target][source]

#computes the sum of probability of all possible alignments, for the translation of src sentence into trg sentence
def get_total_count(src_sentence, trg_sentence, translation_table):
        
        alignment_prob_for_t = defaultdict(lambda: 0.0)
        for target in trg_sentence:
            for source in src_sentence:
                alignment_prob_for_t[target] += prob_alignment_point(source, target, translation_table)
        return alignment_prob_for_t

def max_lex_transl_probab(counts, translation_table):
      for t, src_words in counts["t_given_s"].items():
          for s in src_words:
              estimate = counts["t_given_s"][t][s] / counts["any_t_given_s"][s]
              translation_table[t][s] = max(estimate, MIN_PROB)          

#recomputes translation probababilites i.e. probability of translation of a word in src vocabulary into every word in trg vocabulary 
def train_iter_helper(corpus, translation_table, lang_a, lang_b):
        counts = {}
        counts["t_given_s"] = defaultdict(lambda: defaultdict(lambda: 0.0))
        counts["any_t_given_s"] = defaultdict(lambda: 0.0)
        for aligned_sentence in corpus:
            trg_sentence = (aligned_sentence[lang_a]).split()
            src_sentence = (aligned_sentence[lang_b]).split()

            # E step - compute normalization factors to weigh counts
            total_count = get_total_count(src_sentence, trg_sentence, translation_table)
            # E step - compute counts
            for t in trg_sentence:
                for s in src_sentence:
                    count = prob_alignment_point(s, t, translation_table)
                    normalized_count = count / total_count[t]
                    counts["t_given_s"][t][s] += normalized_count
                    counts["any_t_given_s"][s] += normalized_count

        # M step: Update probabilities with maximum likelihood estimate
        max_lex_transl_probab(counts, translation_table)

#trains the model on the given training corpus for the given number of iterations
def train(corpus, iterations, lang_a, lang_b, dump_filename = None):
  translation_table = {}
  set_initial_probabilities(corpus, translation_table, lang_a, lang_b)
  for i in range(iterations):
    train_iter_helper(corpus, translation_table, lang_a, lang_b)
    print(str(i) + " iterations completed")
    if (i % 10 and dump_filename is not None):
      dump_model(translation_table, filename = dump_filename + str(i) + ".json")
  return translation_table
