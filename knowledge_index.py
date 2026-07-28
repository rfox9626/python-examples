import re

class KnowledgeIndex:
    def __init__(self):
        self.doc_base = {}

    def display(self):
        print("{}".format(self.doc_base))

    def sanitize_words(self, text):
        return [re.sub(r"[?.,!]", "", word).casefold() for word in text.split()]

    def add_document(self, doc_id: int, text: str) -> None:
        clean_list = self.sanitize_words(text)
        for word in clean_list:
                if word in self.doc_base:
                    self.doc_base[word].add(doc_id)
                else:
                    self.doc_base[word] = {doc_id}

    def search(self, query: str) -> set:

        clean_list = self.sanitize_words(query)

        if not clean_list:
            return set()

        ret_set = self.doc_base.get(clean_list[0], set())

        for word in clean_list[1:]:
            word_docs = self.doc_base.get(word, set())
            ret_set = ret_set & word_docs

            if not ret_set:
                break
            
        return ret_set


"""
INSTRUCTIONS:
Build an inverted index that maps cleaned, case-insensitive keywords to a set of unique 
document IDs rather than doing slow linear scans through text files. By leveraging 
dictionary lookups and set intersections, the engine achieves fast, constant-time 
search performance even as the document store grows.

Test cases
q = KnowledgeIndex()
q.add_document(9626, "Python is great for building backend services and automation!?!!!")
q.add_document(102, "Automation tools often rely on robust programming languages.")
q.add_document(103, "Building a knowledge base requires efficient indexing algorithms.")
q.add_document(201, "Python! Python? Python... It's everywhere.")
q.display()
x = q.search("automation")
print("x = {}".format(x))
"""
