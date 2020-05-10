from ResponseMachine import ResponseMachine;
from ResponseMachine import CosineSimilarity;
import pytest;

answerString ="subgenus Hippotigris; the plains zebra, the Grévy's zebra and the mountain zebra;horses and donkeys;aims to breed zebras that are phenotypically similar to the quagga; Grévy's zebra and the mountain zebra ";        

paragraph = "Zebras are several species of African equids (horse family) united by their distinctive black and white stripes. Their stripes come in different patterns, unique to each individual. They are generally social animals that live in small harems to large herds. Unlike their closest relatives, horses and donkeys, zebras have never been truly domesticated. There are three species of zebras: the plains zebra,the Grévy's zebra and the mountain zebra. The plains zebra and the mountain zebra belong to the subgenus Hippotigris, but Grévy's zebra is the sole species of subgenus Dolichohippus. The latter resembles an ass, to which it is closely related, while the former two are morePage 2 / 3 horse-like. All three belong to the genus Equus, along with other living equids. The unique stripes of zebras make them one of theanimals most familiar to people. They occur in a variety of habitats,such as grasslands, savannas, woodlands, thorny scrublands,mountains, and coastal hills. However, various anthropogenic factors have had a severe impact on zebra populations, in particular hunting for skins and habitat destruction. Grévy's zebra and the mountain zebra are endangered. While plains zebras are much more plentiful, one subspecies - the Quagga - became extinct in the late 19th century. Though there is currently a plan, called the Quagga Project,that aims to breed zebras that are phenotypically similar to the Quagga, in a process called breeding back."

questions = ["Which Zebras are endangered?",
             "What is the aim of the Quagga Project?",
             "Which animals are some of their closest relatives?",
             "Which are the three species of zebras?",
             "Which subgenus do the plains zebra and the mountain zebra belong to?"
             ]


cosineSimilarity = CosineSimilarity()  
responseMachine = ResponseMachine(paragraph,answerString,questions);

@pytest.mark.similarity
def test_cosine_similarity():
    result = cosineSimilarity.findSimilarity("hello","hello") ;
    assert(result == 1)

@pytest.mark.similarity
def test_cosine_error():
    result = cosineSimilarity.findSimilarity("hello","hellow") ;
    assert(result <= 1)
    
@pytest.mark.similarity
def test_input():
    with pytest.raises(ZeroDivisionError) :
        cosineSimilarity.findSimilarity("","") 

#Test ResponseMachine
@pytest.mark.responseMachine
def test_responsemachine_init():
    assert(responseMachine.paragraph == paragraph)

@pytest.mark.responseMachine
def test_responsemachine_processInput():
    paragraph,answers = responseMachine.processInput();
    inputAnswers = answerString.split(";");
    assert((len(answers) == len(inputAnswers)) and (answers[1] == inputAnswers[1]) )

@pytest.mark.responseMachine
def test_find_context():
    paragraph,answers = responseMachine.processInput();
    context = responseMachine.findContext(answers,paragraph);
    assert(len(context) == len(answers) )
    assert(context[0]["index"] == 5)
    assert(context[0]["similarity"] >0)

@pytest.mark.responseMachine
def test_find_context_negative():
    paragraph,answers = responseMachine.processInput();
    context = responseMachine.findContext(paragraph,answers);
    assert(len(context) == len(paragraph) )
    assert(context[0]["index"] != 5)

@pytest.mark.responseMachine
def test_find_context_sameContext():
    paragraph,answers = responseMachine.processInput();
    context = responseMachine.findContext(answers,answers);
    assert(len(context) == len(answers) )
    assert(context[0]["index"] == 0)

@pytest.mark.responseMachine
def test_find_context_findAnswer():
    contextSentences,answer = responseMachine.findAnswer();
    
    assert(answer[0].strip() == "Grévy's zebra and the mountain zebra")
    assert(answer[1].strip() == "aims to breed zebras that are phenotypically similar to the quagga")
    assert(answer[2].strip() == "horses and donkeys")
    assert(answer[3].strip() == "the plains zebra, the Grévy's zebra and the mountain zebra")
    assert(answer[4].strip() == "subgenus Hippotigris")
    

