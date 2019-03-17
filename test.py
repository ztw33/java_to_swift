import os,json,re,copy
#def mak_dic_word():
import string
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

def del_stopwords(sen):
    stopworddic = set(stopwords.words('english'))
    stopworddic.add("return")
    result = [i for i in sen.split(" ") if i not in stopworddic]
    return " ".join(result)


def preprocess_sen_new(sen, if_stop_words=False):
    sentences = re.sub("CF|NS|AU|CAF|QC|CG|UI|CA|AV|\\)|\\(", "", sen)
    result = re.split(" |_|-|—|:", sentences)
    print("result: ", result)
    result = map(split_Uppercase, result)  # 将词以大写字母开始后加小写字母直至遇到大写字母,全是大写则不分开

    result = map(delete_num, result)
    input_str_old = copy.deepcopy(list(result))
    result = " ".join(input_str_old)

    sentences = result.lower()
    table = str.maketrans("", "", string.punctuation)
    result = sentences.translate(table)
    print("result: ",result)
    if if_stop_words:
        result = del_stopwords(result)
    return result


def split_Uppercase(x):
    # 这里假设以小写开始，之后全是大写开始拆分  stringAbdBcd
    x = x.replace(".", "")
    upp = re.findall('[A-Z][^A-Z]+', x)

    if len(upp) == 0:
        return x.lower()
    #    print("split_Uppercase: ",x.replace("".join(upp),"")+" "+" ".join(upp))
    return (x.replace("".join(upp), "") + " " + " ".join(upp)).strip().lower()


# 将字符串按大小写拆分为若干字符
def split_words(json_str):
    sentence = re.sub("CF|NS|AU|CAF|QC|CG|UI|CA|AV|\\)|\\(", "", json_str)
    result_list = copy.deepcopy(split_Uppercase(sentence).split(" "))
    return result_list


def delete_num(x):
    if re.search("\d", x) == None:
        return x
    else:
        return ""

print(preprocess_sen_new("NSHashtable"))