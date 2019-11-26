# Cross-Lingual-Document-Translator
A Cross Lingual Document Translator is implemented using Statistical Machine Translation model. Statistical Machine Translation is an empirical machine translation technique using which translations are generated on the basis of statistical models trained on bilingual text corpora.

### IBM MODEL I

![image](https://user-images.githubusercontent.com/27685757/68961093-85b88380-07f7-11ea-83a8-ed1c764b1a41.png)

#### Flow of Algorithm
`train` method is called initially which internally calls `train_iter_helper`. In `train_iter_helper` the count dictionary is made which is used to update the translation model. The translation model gets updated using E-M Method. Model generates Translation table which ultimately is improvised with given number of iterations.

Then translation method `translate_sentence` is called for given trained model which ultimately gives us translated document. It tokenizes the source sentence and gets the corresponding translated word (assuming they map continuously with no distortion) and returns final sentence.

### INNOVATION USED
1. A major issue of IBM model 1 is due to its hypothesis of only 1 NULL word per sentence. The issue which occurs due to this is that Model 1 seems to align too few target words to the NULL source word. There is also another non-structural problem associated with Model 1 according to which rare words get aligned to too many words in the target language.
In the innovation part of our assignment we have tackled the above stated issues using a 2 step approach. In the first step we use a function which smoothes the translation probability estimates by adding virtual counts according to a uniform probability distribution over all target words. This helps in tackling the issue of rare words. For carrying out this task we define a parameter n and set its value to 0.005 (in our case) and then we obtain the smoothed probability by
 ![image](https://user-images.githubusercontent.com/27685757/68961464-771e9c00-07f8-11ea-8481-c6308d535277.png)
 where |V| is the size of the target vocabulary.
For handling the NULL words we have added a fixed number of extra null words (q0 = 2 in our case) to address the lack of sufficient alignments of target words to the NULL source word.

2. Another innovation which we have carried out is **Ensemble Learning** which generally improves the result by combining several models and thereby improves the result as compared to the result of a single model.
From the same corpus, we obtained m different samples and trained the IBM Model 1 on each of the samples. Hence, we obtained m different models and their corresponding translation probability matrices.
To obtain the resultant translation probabilities, we considered two approaches:    
**First Approach:**  
Get the word translations from the translation probability matrix for each model, by taking the word corresponding to the maximum translation probability.
So, we have m or less word translations for each source language word in the original corpus.
Finally, take the majority voting of all the potential translation options for each source word and hence generate the resultant word translations.  
Limitations – Since this approach considers the word translations of each model for obtaining the resultant word translations and leaves out the probabilities of translations altogether, so we may not always get the correct result.
It was observed that for cases where highly confident word translations are overshadowed due to greater number of considerably lower confident word translations. For example, if 15 models are trained on a corpus, and 6 of them are giving ‘huis’ as the translation of ‘house’ with a probability of around 0.8 each while 8 of them are giving ‘weg’ as the translation of ‘house’ with a probability of around 0.3 each and 1 of them gives some random translation. In this particular case, we can see that the translation of ‘house’ should be ‘huis’ but the above approach would result in ‘weg’ as the translation.  
**Second Approach:**    
In addition to the first approach, we incorporated each and every word translation probability to get the resultant word translation, in contrast to the first approach where we just considered the word translations from the models to get the resultant translations.
After obtaining the translation probability matrices from the models, take the average of probabilities of translation from the source word into a particular target word.
Now, get the word translations from the average probabilities as we obtain in the IBM Model 1.
Considering the above stated example, this approach would give the translation probability of ‘house’ to ‘huis’ to be around 0.8 in contrast to 0.3 for translation from ‘house’ to ‘weg’.

### RESULT ON A SAMPLE DATASET

Sample of **Europal English-Dutuch Dataset** is used and results are noted.
#### Result:
![Performance](https://user-images.githubusercontent.com/27685757/68962399-7f77d680-07fa-11ea-8e35-bfda24614f8a.png)

