from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
import graphene
from graphql import GraphQLError

User = get_user_model()


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class UserByIdQuery(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.Int(required=True), description="Gets single User by ID")

    def resolve_user(self, info, id):
        user = info.context.user
        if not user.has_perm('auth.view_user'):
            raise GraphQLError(f"Cannot query field `{info.field_name}` on type `{info.parent_type}`.")

        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            raise GraphQLError(f"User with id={id} not found.")


schema = graphene.Schema(query=UserByIdQuery)
