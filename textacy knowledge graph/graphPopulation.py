from neomodel import StructuredNode, StringProperty, RelationshipTo, config, StructuredRel


config.DATABASE_URL = 'bolt://neo4j:password@localhost:7687'
config.ENCRYPTED_CONNECTION=False


class RelationshipModel(StructuredRel):
    DBpediaURL = StringProperty()
    relationType = StringProperty()


class Object(StructuredNode):
    object_name = StringProperty(unique_index=True)
    DBpediaURL = StringProperty()
    # books = RelationshipFrom(Subject, 'predicate')


class Subject(StructuredNode):
    subject_name = StringProperty(unique_index=True)
    DBpediaURL = StringProperty()
    predicate = RelationshipTo(
        Object, 'predicate', model=RelationshipModel)


class GraphPopulation:

    def popGraph(self, spoData, entityLinks):

        # print("Data received in graph population:")
        # print(spoData)
        for index in range(len(spoData)):
            spo = spoData[index]

            subjectDBpediaURL = entityLinks[index][0]
            objectDBpediaURL = entityLinks[index][2]

            subjectTemp = Subject.nodes.first_or_none(subject_name=spo[0])
            subject_extracted = None
            if subjectTemp == None:
                subject_extracted = Subject(
                    subject_name=spo[0], DBpediaURL=subjectDBpediaURL).save()
            else:
                subject_extracted = subjectTemp
            objectTemp = Object.nodes.first_or_none(object_name=spo[2])
            object_extracted = None
            if objectTemp == None:
                object_extracted = Object(
                    object_name=spo[2], DBpediaURL=objectDBpediaURL).save()
            else:
                object_extracted = objectTemp

            subject_extracted.predicate.definition['relation_type'] = spo[1]
            relationship = subject_extracted.predicate.connect(
                object_extracted)
            relationship.relationType = spo[1]
            relationship.DBpediaURL = entityLinks[index][1]
            relationship.save()

        # all_subject_nodes = Subject.nodes.all()
        # all_object_nodes = Object.nodes.all()
        #
        # for node in all_subject_nodes:
        #     print(node)
        #
        # for node in all_object_nodes:
        #     print(node)

    def delete_all_nodes(self):
        all_subject_nodes = Subject.nodes.all()
        all_object_nodes = Object.nodes.all()

        for node in all_subject_nodes:
            node.delete()

        for node in all_object_nodes:
            node.delete()
