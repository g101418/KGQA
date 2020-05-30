from py2neo import Graph

class NeoDB(object):
    def __init__(self):
        super().__init__()
        self.graph = Graph("http://localhost:7474",
                           username="neo4j", password="123456")
        self.CA_LIST = {"贾家荣国府": 0, "贾家宁国府": 1,
                        "王家": 2, "史家": 3, "薛家": 4, "其他": 5, "林家": 6}
        self.similar_words = {
            "爸爸": "父亲", "妈妈": "母亲", "爸": "父亲", "妈": "母亲", "父亲": "父亲",
            "母亲": "母亲", "儿子": "儿子", "女儿": "女儿", "丫环": "丫环", "兄弟": "兄弟",
            "妻": "妻", "老婆": "妻", "哥哥": "哥哥", "表妹": "表兄妹", "弟弟": "弟弟",
            "妾": "妾", "养父": "养父", "姐姐": "姐姐", "娘": "母亲", "爹": "父亲",
            "father": "父亲", "mother": "母亲", "朋友": "朋友", "爷爷": "爷爷", "奶奶": "奶奶",
            "孙子": "孙子", "老公": "丈夫", '岳母': '岳母', "表兄妹": "表兄妹",
            "孙女": "孙女", "嫂子": "嫂子", "暧昧": "暧昧"
        }

    def create_graph(self, relation_filename="./data/relation.txt"):
        """
        构造图，将relation.txt文件数据写入neo4j数据库
        :param relation_filename:str relation.txt文件路径名
        :return:
        """
        with open(relation_filename) as f:
            for line in f.readlines():
                rela_array = line.strip("\n").split(",")
                print(rela_array)
                graph.run("MERGE(p: Person{cate:'%s',Name: '%s'})" % (
                    rela_array[3], rela_array[0]))
                graph.run("MERGE(p: Person{cate:'%s',Name: '%s'})" % (
                    rela_array[4], rela_array[1]))
                graph.run(
                    "MATCH(e: Person), (cc: Person) \
                    WHERE e.Name='%s' AND cc.Name='%s'\
                    CREATE(e)-[r:%s{relation: '%s'}]->(cc)\
                    RETURN r" % (rela_array[0], rela_array[1], rela_array[2], rela_array[2])
                )
        return
