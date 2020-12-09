import graphene
from graphene import Argument
from graphene_django.types import DjangoObjectType
from .models import Post, Comment



class PostType(DjangoObjectType):
  class Meta:
    model = Post

class CommentType(DjangoObjectType):
  class Meta:
    model = Comment


class Query(object):
  all_post = graphene.List(PostType)
  post = graphene.Field(PostType, id=graphene.ID())

  all_comments = graphene.List(CommentType)
  comment = graphene.Field(CommentType, id=graphene.ID())

  def resolve_all_posts(self, info, **kwargs):
    return Post.objects.all()

  def resolve_post(self, info, id):
    return Post.objects.get(pk=id)

  def resolve_all_comments(self, info, **kwargs):
    return Comment.objects.all()

  def resolve_comment(self, info, id):
    return Comment.objects.get(pk=id)



class CreatePost(graphene.Mutation):
  class Arguments:
      title = graphene.String()
      description = graphene.String()
      publish_date = graphene.types.datetime.DateTime()
      author = graphene.String()

  post = graphene.Field(PostType)


  def mutate(self, info, title, description, publish_date=None, author=None):
    post = Post.objects.create(
        title=title,
        description=description,
        publish_date=publish_date,
        author=author
    )

    post.save()
    return CreatePost(
      post=post
    )

class UpdatePost(graphene.Mutation):
  class Arguments:
    id = graphene.ID()
    title = graphene.String()
    description = graphene.String()
    publish_date = graphene.types.datetime.DateTime()
    author = graphene.String()

  post = graphene.Field(PostType)

  def mutate(self, info, id, title, description, publish_date=None, author=None):
    post = Post.objects.get(pk=id)
    post.title = title if title is not None else post.title
    post.description = description if description is not None else post.description
    post.publish_date = publish_date if publish_date is not None else post.publish_date
    post.author = author if author is not None else post.author

    post.save()
    return UpdatePost(post=post)


class DeletePost(graphene.Mutation):
  class Arguments:
    id = graphene.ID()

  post = graphene.Field(PostType)

  def mutate(self, info, id):
    post = Post.objects.get(pk=id)
    if post is not None:
      post.delete()
    return DeletePost(post=post)

class CreateComment(graphene.Mutation):
  class Arguments:
    connected_post = graphene.String()
    author = graphene.String()
    comments = graphene.String()
    date_of_comment = graphene.types.datetime.DateTime()

  comment = graphene.Field(CommentType)

  def mutate(self, info, connected_post, author, comments, date_of_comment):
    comment = Comment.objects.create(
        connected_post = connected_post,
        author = author,
        comments = comments,
        date_of_comment = date_of_comment
    )
    return CreateComment(
      comment=comment
    )


class UpdateComment(graphene.Mutation):
  class Arguments:
    id = graphene.ID()
    connected_post = graphene.String()
    author = graphene.String()
    comments = graphene.String()
    date_of_comment = graphene.types.datetime.DateTime()

  comment = graphene.Field(CommentType)

  def mutate(self, info, id, connected_post, author, comments, date_of_comment):
    comment = Comment.objects.get(pk=id)
    comment.connected_post = connected_post if connected_post is not None else comment.connected_post
    comment.author = author if author is not None else comment.author
    comment.comments = comments if comments is not None else comment.comments
    comment.date_of_comment = date_of_comment if date_of_comment is not None else comment.date_of_comment

    comment.save()
    return UpdateComment(comment=comment)


class DeleteComment(graphene.Mutation):
  class Arguments:
    id = graphene.ID()

  comment = graphene.Field(CommentType)

  def mutate(self, info, id):
    comment = Comment.objects.get(pk=id)
    if comment is not None:
      comment.delete()
    return DeleteComment(comment=comment)


class Mutation(graphene.ObjectType):
  create_post = CreatePost.Field()
  update_post = UpdatePost.Field()
  delete_post = DeletePost.Field()

  create_comment = CreateComment.Field()
  update_comment = UpdateComment.Field()
  delete_comment = DeleteComment.Field()
