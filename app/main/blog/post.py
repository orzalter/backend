# coding:utf8
import json
from json.decoder import JSONDecodeError

from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func

from app import db
from app.api.format import Format
from app.models import *

from . import blog, resource


@resource.resource('/post')
class BlogPost(Resource):
    """单篇文章操作"""

    def __init__(self):
        self.parser = RequestParser()

    def get(self):
        """获取文章所有信息

        Params:
            id (:obj:`int`): id

        Returns:
            Post:
                id      (int):     id
                title   (str):     标题
                article (str):     文章
                tags    (str):     分类
        """
        self.parser.add_argument(
            'id', location='args', type=int, required=True, help='id')
        args = self.parser.parse_args()

        data = dict()

        post = Post.query.filter_by(id=args['id']).first()
        if not post:
            return Format.error(message='Post (id) not exists', code=404)

        # 标签
        tags = [dict(id=tag.id, name=tag.name) for tag in post.tags]

        data['post'] = dict(
            id=post.id,
            title=post.title,
            article=post.article,
            tags=tags,
        )

        return Format.success(data=data)

    def post(self):
        """新增或編輯文章所有信息

        Params:
            id (:obj:`int`): id

        Returns:
            Post:
                id      (int):     id
                title   (str):     标题
                article (str):     文章
                tags    (str):     分类
        """
        self.parser.add_argument(
            'id', location='json', type=int, help='id')
        self.parser.add_argument(
            'title', location='json', type=str, required=True, help='title')
        self.parser.add_argument(
            'article', location='json', type=str, required=True, help='article')
        self.parser.add_argument(
            'tags', location='json', type=str, help='tags')
        args = self.parser.parse_args()

        if args['id']:
            #  編輯
            blogpost = Post.query.filter_by(id=args['id']).first()
            if not blogpost:
                return Format.error(message='Post (id) not exists')
        else:
            blogpost = Post(title=args['title'])

        blogpost.title = args['title']
        blogpost.article = args['article']

        if args['tags']:
            try:
                tags_list = json.loads(args['tags'].replace("'", "\""))
                if not isinstance(tags_list, list):
                    raise JSONDecodeError
            except JSONDecodeError:
                return Format.error(message='Tag format error')

            tags = [_tagname.name.lower() for _tagname in Tag.query.all()]

            rela_tags = []
            for tag in tags_list:
                if tag.strip().lower() in tags:
                    new_tag = Tag.query.filter(
                        func.lower(Tag.name) == tag).first()
                    rela_tags.append(new_tag)
                else:
                    new_tag = Tag(name=tag.strip().lower())
                    rela_tags.append(new_tag)
                    db.session.add(new_tag)
                    # db.session.commit()
            blogpost.tags = rela_tags
        try:
            db.session.add(blogpost)
            db.session.commit()
            data = dict()
            data['post'] = dict(title=args['title'])
        except:
            return Format.error(message='Add post error')

        return Format.success(data=data)

    def delete(self):
        """删除文章

        Params:
            id (:obj:`int`): 文章id
        """
        self.parser.add_argument(
            'id', location='args', type=int, required=True, help='id')
        args = self.parser.parse_args()

        post = Post.query.filter_by(id=args['id']).first()

        if not post:
            return Format.error(message='Post (id) not exists')

        try:
            db.session.delete(post)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return Format.error(message='Delete post fail')
        data = dict()
        data['post'] = dict(title=post.title)
        return Format.success(data=data)
