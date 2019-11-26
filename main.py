from util import *
from translate import *
from input import *

def main():
	#input
	# base = "data/"
	# lang_a = "en" 
	# infile_a = base + "en.txt"
	# lang_b = "du"
	# infile_b = base + "fr.txt"

	# corpus_original = get_corpus(lang_a, infile_a, lang_b, infile_b)
	# print(len(corpus_original))
	# corpus = get_sample(corpus_original, 2, 2)
	# print(len(corpus))
	# p_corpus = preprocess_corpus(corpus, lang_a, lang_b)

	# model = train(p_corpus, 2, lang_a, lang_b)
	# idfs = compute_IDFs(p_corpus[:1000])

	ip_file = input("Give name of input model: ")
	json_model = input_json_model(ip_file)
	print("Select from the given options: ")
	print("1: Show Model Summary")
	print("2: Translate Sentence")

	ip_option = int(input())
	if(ip_option == 1):
		show_results(json_model)
	elif(ip_option == 2):
		ip_sentence = input("Give a sentence to translate: ")
		ip_sentence = to_normalized_sentence(ip_sentence)
		print("translated sentence = " + str(translate_sentence(json_model["model"], ip_sentence)))
	else:
		print("Error! Please enter correct option")

if __name__ == "__main__":
	main()