import nltk

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('brown')

from textblob import TextBlob

from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize

class Similarity: # pragma: no cover
    
    def findSimilarity(self,sentence1 , sentence2) -> float:
        pass
        

class CosineSimilarity(Similarity):
    
    def findSimilarity(self,sentence1 , sentence2 ):
        sentence1List=[]; sentence2List =[];
    
        s1_list = word_tokenize(sentence1.lower())
        s2_list = word_tokenize(sentence2.lower())
        
        # remove stop words from string 
        s1_set = {w for w in s1_list if not w in stopwords.words()}  
        s2_set = {w for w in s2_list if not w in stopwords.words()}
    
        # form a set containing keywords of both strings  
        rvector = s1_set.union(s2_set)  
        
        for w in rvector: 
            if w in s1_set: sentence1List.append(1) # create a vector 
            else: sentence1List.append(0) 
            if w in s2_set: sentence2List.append(1) 
            else: sentence2List.append(0) 
            
        c = 0
        # cosine formula  
        for i in range(len(rvector)): 
            c+= sentence1List[i]*sentence2List[i] 
            
        cosine = c / float((sum(sentence1List)*sum(sentence2List))**0.5) 
        
        return cosine

class ResponseMachine:
    
    paragraph = ""
    answerstring = ""
    questions = []
    
    def __init__(self,p,a,q):
        self.paragraph = p;
        self.answerstring = a ;
        self.questions =q;
    
    def findContext(self, vector1 , vector2):
        
        contexts = [];
        
        cosineSimilarity = CosineSimilarity()
        
        for vector1Sentence in vector1:
            contextSimilarities = []
            for vector2Sentence in vector2:
                contextSimilarities.append(cosineSimilarity.findSimilarity(vector1Sentence,vector2Sentence))
            
            context = {"index" : contextSimilarities.index(max(contextSimilarities)), "similarity" :max(contextSimilarities) }
            contexts.append(context)
    
        return contexts; 
    
    def processInput(self):
        
        blob = TextBlob(self.paragraph);
        paragrahSentences = [str(sentence) for sentence in blob.sentences]
        
        answers = self.answerstring.split(";");
        
        return paragrahSentences , answers
   
    
    def findAnswer(self):
        
        paragraphSentences , answers = self.processInput();
        
        #********************Backward Context*****************************
        
        #Find the context sentences from the paragraph using answers
        contextSentencesDetails = self.findContext(answers,paragraphSentences);
              
        contextSentences = [  str(paragraphSentences[context["index"]]) for context in contextSentencesDetails]
        
        #Find the answer using the context sentences and the question
        answerDetails = self.findContext(self.questions,contextSentences);
        
        answer = [  str(answers[context["index"]]) for context in answerDetails]
    
        return contextSentences,answer

    def main(): # pragma: no cover
        
        paragraph = "";
        answer_string = "";
        questions = [];
        
        f = open("input.txt","r")
        lines = f.readlines();
        
        paragraph = lines[0].strip()
        
        for counter in range(1,6):
            questions.append(lines[counter].strip())
        
        answer_string = lines[6].strip()
        
        responseMachine = ResponseMachine(paragraph,answer_string, questions)
        contexts, answers = responseMachine.findAnswer()
        print("***********************")
        for answer in answers:
            print(answer.strip())
        
    if __name__=="__main__": 
        main() 