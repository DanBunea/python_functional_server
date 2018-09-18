from commons import debug
from database_services import Article, Comment
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

        if obj.comments:
            json["comments"] = []
            for comment in obj.comments:
                transformer = CommentTransformer()
                json_comment = {}
                transformer.to_json(json_comment, comment)

                json["comments"].append(json_comment)


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




