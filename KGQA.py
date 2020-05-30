from neo import NeoDB
import jieba
import jieba.posseg as pseg

import logging
logging.basicConfig(level=logging.ERROR)
jieba.setLogLevel(logging.INFO)

class KGQA(object):
    def __init__(self):
        super().__init__()
        # self.taggings = ['n', 'PER']  # n: 名词(如：儿子)、PER: 人名(如：贾宝玉)
        self.neo = NeoDB()
        jieba.enable_paddle()

    def cut_words(self, sentence):
        """
        句子分词并标注词性
        :param sentence:str 用户输入的问句，如"贾宝玉的爸爸是谁"
        :return person: str 问题的主要人物
        :return words: 如['爸爸', '妈妈']
        """
        words_flags = pseg.cut(sentence, use_paddle=True)  # paddle模式

        person = ''
        words = []
        for word, flag in words_flags:
            if flag == 'PER':
                person = word
            if flag == 'n':
                words.append(self.neo.similar_words[word])
        logging.debug(str(words))
        return person, words

    def answer(self, sentence):
        """
        搜索回答
        :param sentence:str 用户输入的问句，如"贾宝玉的爸爸是谁"
        :return result: str 如：""
        """
        try:
            person, words = self.cut_words(sentence)

            words_ = [0 for i in range(len(words))]
            for i in range(len(words)):
                words_[i] = '-[r'+str(i) + ':'+words[len(words)-i-1]+']'
                if i != len(words)-1:
                    words_[i] += '->(n'+str(i)+':Person)'
            quary = "match(p)" + ''.join(words_) + \
                "->(n:Person{Name:'"+person+"'}) return  p.Name,n.Name,p.cate,n.cate"
            logging.debug(str(quary))
        except Exception as e:
            return '问题有误'

        try:
            data = self.neo.graph.run(quary)
            data = list(data)[0]
            logging.debug(str(data))

            result = data['n.cate']+'的'+data['n.Name']
            for item in words:
                result += '的'
                result += item
            result += '是'
            result += data['p.cate']+'的'+data['p.Name']
            return result
        except Exception as e:
            return '没有答案'

    def test(self, sentence):
        answer = self.answer(sentence)
        print(answer)
