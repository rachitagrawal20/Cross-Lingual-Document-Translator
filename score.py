
#computes jaccard coefficient
def jaccard_similarity(docA, docB):
  list1 = docA.split()
  list2 = docB.split()
  intersection = len(list(set(list1).intersection(list2)))
  union = (len(list1) + len(list2)) - intersection
  return float(intersection) / union

#returns a dictionary of cosine similarity and jaccard coefficient
def similarity(idf, docA, docB):
  return {
      "cosine" : cosine_similariy(idf, docA, docB),
      "jaccard" : jaccard_similarity(docA, docB)
  }

def print_average_similarity(p_corpus, model):
	cos_sim = 0
	jac_sim = 0
	for i in range(len(p_corpus)):
	  docA = p_corpus[i][lang_b]
	  docB = translate_sentence(model, p_corpus[i][lang_a])
	  sim = similarity(idfs[lang_b], docA, docB)
	  jac_sim += sim["jaccard"]
	  cos_sim += sim["cosine"]
	jac_sim /= len(p_corpus)
	cos_sim /= len(p_corpus)
	print("Jaccard: " + str(jac_sim) + " Cosine: " + str(cos_sim))
