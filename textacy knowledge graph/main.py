import graphPopulation
import knowledgeExtraction
import dataLoading
import entityRecognitionLinking

dataLoader=dataLoading.DataLoader()

inputText=dataLoader.load_text_from_file(filepath="train-00000-of-00001.parquet")
inputText_partials=dataLoader.load_text_lists_from_file(filepath="train-00000-of-00001.parquet")

knowledgeExtractionObj = knowledgeExtraction.KnowledgeExtraction()
sop_list = knowledgeExtractionObj.retrieveKnowledge(inputText)

sop_list_strings = []
for sop in sop_list:
    temp = []
    temp.append(sop[0].text)
    temp.append(sop[1].text)
    temp.append(sop[2].text)
    sop_list_strings.append(temp)

# print(sop_list_strings)


entityRecognitionLinkingObj = entityRecognitionLinking.EntityRecognitionLinking()

entityRelJson = entityRecognitionLinkingObj.entityRecogLink_partials(inputText_partials)

entityLinkTriples = []
for sop in sop_list_strings:
    tempTriple = ['', '', '']
    for resource in entityRelJson['Resources']:
        if resource['@surfaceForm'] == sop[0]:
            tempTriple[0] = resource['@URI']
        if resource['@surfaceForm'] == sop[1]:
            tempTriple[1] = resource['@URI']
        if resource['@surfaceForm'] == sop[2]:
            tempTriple[2] = resource['@URI']
    entityLinkTriples.append(tempTriple)
# print(entityLinkTriples)


graphPopulationObj = graphPopulation.GraphPopulation()
graphPopulationObj = graphPopulationObj.popGraph(
    sop_list_strings, entityLinkTriples)

