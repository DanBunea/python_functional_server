from commons import debug
from database_write_services import Article, Comment
from immutable import value, change



class ArticleTransformer:
    def from_json(self, json, obj):
        if json.has_key("title"):
            obj.title = json["title"]
        if json.has_key("content"):
            obj.content = json["content"]

        if "comments" in json.keys() and isinstance(json["comments"],list):
            for comment_json in json["comments"]:
                comment = Comment()

                transformer = CommentTransformer()
                transformer.from_json(comment_json,comment)

                obj.comments.append(comment)



    def to_json(self, json, obj):
        json["id"] = obj.id
        json["title"] = obj.title
        json["content"] = obj.content



class CommentTransformer:
    def from_json(self, json, obj):
        obj.comment = json["comment"]

    def to_json(self, json, obj):
        json["comment"] = obj.comment



transformers = dict(
    Article=ArticleTransformer,
    Comment=CommentTransformer
)


def transform_from_json(state):
    debug(transform_from_json.__name__, "json:", state.json)
    obj = state.data
    json = state.json

    transformer_cls = transformers[state.type.__name__]
    transformer = transformer_cls()
    transformer.from_json(json,obj)


    return state


def transform_to_json(state):
    debug(transform_to_json.__name__, "data:", state.data)
    obj = value("data")(state)
    json={}


    transformer_cls = transformers[state.type.__name__]
    transformer = transformer_cls()
    transformer.to_json(json,obj)

    return change("data",json)(state)


def transform_results(state):
    json = transform_results_to_json(state, state.data)
    return change("data",json)(state)


def get_property_name(whole):
    return whole.rsplit('.', 1)[1] if "." in whole else whole



def property_to_json(json, element, value):
    prop_name = get_property_name(element)

    json[prop_name]= value

counter = 0

def count_fields(dic):
    global counter
    if isinstance(dic, list):
        for val in dic:
            if isinstance(val, str) or isinstance(val, unicode):
                counter = counter + 1
            else:
                count_fields(val)
    else:
        for key in dic.keys():
            count_fields(dic[key])
    return counter


    # debug(1,prop_name, value)
def transform_results_to_json(state,results):
    # global index
    # index=0
    fields= state.json["find"]

    # print 1, fields, index

    def get_id_dict(parent_dict, unique_key):
        # unique_key = row.id
        if not parent_dict.has_key(unique_key):
            parent_dict[unique_key] = {}
        return parent_dict[unique_key]


    def transform_row_to_json(row, json, element_list, transform_field_function=property_to_json, relation=None, path=[], column_index=0):
        # global index
        global counter
        # print 2,index,relation,path, element_list
        if relation:
            path.append(relation)
        for element in element_list:
            #property
            if isinstance(element, str) or isinstance(element, unicode):
                transform_field_function(json, element, row[column_index])
                column_index+=1
            #relation
            elif isinstance(element, dict):
                # print 33, ".".join(path)
                relation_key = element.keys()[0]
                relation_list = element[relation_key]

                #create relation_dict
                relation_name = get_property_name(relation_key)
                relation_dic = get_id_dict(json, relation_name)
                if row[column_index]!=None:
                    inner_dic = get_id_dict(relation_dic, row[column_index])
                    #recursive
                    column_index=transform_row_to_json(row, inner_dic, relation_list, relation=relation_name, path=path, column_index=column_index)
                else:
                    counter = 0
                    column_index+=count_fields(relation_list)

        return column_index


    results_json = {}

    debug("transform_results_to_json", len(results))
    for res in results:

        json = get_id_dict(results_json, res[0])
        index = 0
        index = transform_row_to_json(res, json, fields, path=[], column_index=0)
    return results_json




