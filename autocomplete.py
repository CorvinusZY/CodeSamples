### Below is a code sample that simulates the auto complete searching system. It is a leetcode problem. Link to the problem is given below.
### https://leetcode.com/problems/design-search-autocomplete-system/

class SentenceNode:
    def __init__(self, hot, sentence):
        self.hot = hot
        self.sentence = sentence
    def __lt__(self, other):
        return self.hot < other.hot if self.hot != other.hot else self.sentence > other.sentence
    
class AutocompleteSystem:
    class trie:
        def __init__(self):
            self.hotsentences = []#min heap (sentencenode)
            self.dic = {}
            #self.system = system
        def addsentence(self, sentence, degree): 
            def contain_sentence():
                tmp = []
                contain = False
                while self.hotsentences:
                    hotsentence = heapq.heappop(self.hotsentences)
                    tmp.append(hotsentence)
                    if hotsentence.sentence == sentence: 
                        tmp[-1].hot = degree
                        contain = True
                        break
                while tmp:
                    heapq.heappush(self.hotsentences, tmp.pop())
                return contain
            if contain_sentence():
                return
            heapq.heappush(self.hotsentences, SentenceNode(degree, sentence))  
            if len(self.hotsentences) > 3:
                heapq.heappop(self.hotsentences)
            return  
    def __init__(self, sentences: List[str], times: List[int]):
        self.root = self.trie()
        self.sentences = sentences
        self.hot = {sentences[i]: time for i, time in enumerate(times)}
        self.build(sentences)
        self.cur_node = self.root
        self.cur_search = ""
        self.have_result = True
        #print(self.root.dic['i'].hotsentences)
    
    
    def sys_addsentence(self, sentence, degree):
        node = self.root
        for ch in sentence:
            if ch not in node.dic:
                node.dic[ch] = self.trie()
            node.addsentence(sentence, degree)
            node = node.dic[ch]
        node.addsentence(sentence, degree)
        
    def build(self, sentences):
        for sentence in sentences:
            self.sys_addsentence(sentence, self.hot[sentence])
                
    def input(self, c: str) -> List[str]:
        if c == '#':
            #print(self.cur_search)
            self.have_result = True
            # store new sentence
            if self.cur_search not in self.hot: self.hot[self.cur_search] = 0
            self.hot[self.cur_search] += 1
            self.sys_addsentence(self.cur_search, self.hot[self.cur_search])
            self.cur_search = ""
            self.cur_node = self.root
            return []
        self.cur_search += c
        if not self.have_result: 
            return []
        
        if c not in self.cur_node.dic:
            self.have_result = False
            return []
        else:
            self.cur_node = self.cur_node.dic[c]
            tmp = []
            while self.cur_node.hotsentences:
                tmp.append(heapq.heappop(self.cur_node.hotsentences))
            res = [hotsentence.sentence for hotsentence in tmp]
            while tmp:
                heapq.heappush(self.cur_node.hotsentences, tmp.pop())
            return res[::-1]

