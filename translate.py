
#returns dictionary which contains word translations from src language to trg language
def get_translations(translation_table):
  translations = {}
  for t in translation_table.keys():
    translations[t] = max(translation_table[t].items(), key=lambda a: a[1])[0]
  return translations
 
#accepts a sentence and returns its translation into trg language
def translate_sentence(model, sentence):
    
    def tokenize(sentence):
      return sentence.split()

    def translate(tokens, translations):
        return [translations[word] if word in translations else word for word in tokens]

    translations = get_translations(model)
    tokens = tokenize(sentence)
    translated_tokens = translate(tokens, translations)

    return " ".join(translated_tokens)
