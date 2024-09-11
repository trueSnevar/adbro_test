import graphene

from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from graphql import GraphQLError

from .models import Item

User = get_user_model()


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class ItemType(DjangoObjectType):
    class Meta:
        model = Item
        fields = ('id', 'name', 'description', 'price')


class Query(graphene.ObjectType):
    user = graphene.Field(
        UserType,
        id=graphene.Int(required=True),
        description="Gets single User by ID"
    )
    item = graphene.Field(
        ItemType,
        id=graphene.Int(required=True),
        description="Get a single item by ID"
    )
    all_items = graphene.List(
        ItemType,
        description="Get all items"
    )

    def resolve_user(self, info, id):
        user = info.context.user
        if not user.has_perm('auth.view_user'):
            raise GraphQLError(
                f"Cannot query field `{info.field_name}` on type `{info.parent_type}`."
            )

        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            raise GraphQLError(f"User with id={id} not found.")

    def resolve_item(self, info, id):
        try:
            return Item.objects.get(id=id)
        except Item.DoesNotExist:
            return None

    def resolve_all_items(self, info):
        return Item.objects.all()


schema = graphene.Schema(query=Query)
