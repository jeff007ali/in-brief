from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize


def _create_word_frequency_table(text_string):
    """
    we create a dictionary for the word frequency table.
    For this, we should only use the words that are not part of the stopWords array.

    Removing stop words and making frequency table
    Stemmer - an algorithm to bring words to its root word.

    :return: words dict 
    """
    stopWords = set(stopwords.words("english"))
    words = word_tokenize(text_string)

    ps = PorterStemmer()

    wordFrequencyTable = dict()
    for word in words:
        word = ps.stem(word)
        if word in stopWords:
            continue
        if word in wordFrequencyTable:
            wordFrequencyTable[word] += 1
        else:
            wordFrequencyTable[word] = 1

    return wordFrequencyTable

def _score_sentences(sentences, wordFrequencyTable):
    """
    score a sentence by its words
    Basic algorithm: adding the frequency of every non-stop word in a sentence divided by total no of words in a sentence.
    :rtype: dict
    """

    sentenceValueTable = dict()
    for sentence in sentences:
        word_count_in_sentence = len(word_tokenize(sentence))
        word_count_in_sentence_without_stop_words = 0

        for wordValue in wordFrequencyTable:
            if wordValue in sentence.lower():
                word_count_in_sentence_without_stop_words += 1
                if sentence[:10] in sentenceValueTable:
                    sentenceValueTable[sentence[:10]] += wordFrequencyTable[wordValue]
                else:
                    sentenceValueTable[sentence[:10]] = wordFrequencyTable[wordValue]

        '''
        we're dividing every sentence score by the number of words in the sentence. 
        Because there can be unfair advantage to long sentence over short sentence with our scoring function
        '''
        if sentence[:10] in sentenceValueTable:
            sentenceValueTable[sentence[:10]] = sentenceValueTable[sentence[:10]] / word_count_in_sentence_without_stop_words

    return sentenceValueTable


def run_summarization(text):
    # 1. create frequency table of words
    wordFrequencyTable = _create_word_frequency_table(text)

    # 2. tokenize the sentences
    sentences = sent_tokenize(text)

    # 3. Score the sentences
    sent_scores = _score_sentences(sentences, wordFrequencyTable)

if __name__ == '__main__':
    result = run_summarization(text_str)
    print(result)

