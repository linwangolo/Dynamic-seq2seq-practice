import jieba
import re


class preprocessing():
    __PAD__ = 0
    __GO__ = 1
    __EOS__ = 2
    __UNK__ = 3
    vocab = ['__PAD__', '__GO__', '__EOS__', '__UNK__']
    def __init__(self):
        self.encoderFile = "./question.txt"
        self.decoderFile = './answer.txt'
        self.dictFile = 'word_dict.txt'
        jieba.load_userdict(self.dictFile)
        self.stopwordsFile = "./preprocessing/stopwords.dat"     #?
        
    def wordToVocabulary(self, originFile, vocabFile, segementFile):
        # stopwords = [i.strip() for i in open(self.stopwordsFile).readlines()]
        # print(stopwords)
        # exit()
        vocabulary = []
        sege = open(segementFile, "w")
        with open(originFile, 'r') as en:
            for sent in en.readlines():
                # 去标点
                if "enc" in segementFile:      # enc???
                    #sentence = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。“”’‘？?、~@#￥%……&*（）]+", "", sent.strip())
                    sentence = sent.strip()
                    words = jieba.lcut(sentence)
                    print(words)
                else:
                    words = jieba.lcut(sent.strip())
                vocabulary.extend(words)    
                for word in words:
                    sege.write(word+" ")
                sege.write("\n")               # 將空白加入每句的字詞之間?
        sege.close()

        # 去重并存入词典
        vocab_file = open(vocabFile, "w")
        _vocabulary = list(set(vocabulary))
        _vocabulary.sort(key=vocabulary.index)
        _vocabulary = self.vocab + _vocabulary     # self.vocab define?
        for index, word in enumerate(_vocabulary):
            vocab_file.write(word+"\n")
        vocab_file.close()

    def toVec(self, segementFile, vocabFile, doneFile):
        word_dicts = {}
        vec = []
        with open(vocabFile, "r") as dict_f:
            for index, word in enumerate(dict_f.readlines()):
                word_dicts[word.strip()] = index                # build a dictionary of vocabularies

        f = open(doneFile, "w")
        with open(segementFile, "r") as sege_f:
            for sent in sege_f.readlines():
                sents = [i.strip() for i in sent.split(" ")[:-1]]
                vec.extend(sents)                                # vec FOR WHAT?
                for word in sents:
                    f.write(str(word_dicts.get(word))+" ")     # write a file for the corresponding values of the key words(str(value) transfer the number into string)
                f.write("\n")
        f.close()
            

    def main(self):
        # 获得字典
        self.wordToVocabulary(self.encoderFile, './preprocessing/enc.vocab', './preprocessing/enc.segement')    #
        self.wordToVocabulary(self.decoderFile, './preprocessing/dec.vocab', './preprocessing/dec.segement')    # ??
        # 转向量
        self.toVec("./preprocessing/enc.segement", 
                   "./preprocessing/enc.vocab", 
                   "./preprocessing/enc.vec")
        self.toVec("./preprocessing/dec.segement", 
                   "./preprocessing/dec.vocab", 
                   "./preprocessing/dec.vec")

pre = preprocessing()
pre.main()
