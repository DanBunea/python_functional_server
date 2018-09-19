We have an web API

Requirements

We should be able to write and read articles and their comments.

Acceptance Test

We save an article:


POST /api/1/save/Article
```json
{
"title":"New article",
"content":"The content"
}
```

and we receive the article + id
```json
{
id: 13, - can be any value
title:"New article",
content:"The content"
}
```
We then add 2 new comments:

POST /api/1/save/Article

```json
{
id: 13, - can be any value
comments:[
    {"comment":"This was awesome!"},
    {"comment":"I loved it as well!"},
]
}
```
response:
```json
{
id: 13, - can be any value
title:"New article",
content:"The content"
}
```
and now reading the articles and the comments:


POST api/1/query/Article
```json
{
    find: [id,title,content,{comments:[id,comment]}],
    where:{id:13}
}
```
should return

```json
{"13":{

    id: 13, - can be any value
    comments:{
    "113":{"comment":"This was awesome!"},
    "114":{"comment":"I loved it as well!"},
    }
   }
   }
```
