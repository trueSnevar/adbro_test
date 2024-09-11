from graphene_django.views import GraphQLView


class CustomVisibilityGraphQLView(GraphQLView):
    """
    Custom GraphQL view that modifies the schema based on the user's permissions.
    If the user does not have the 'auth.view_user' permission, the 'user' field
    and 'UserType' will be removed from the schema.
    """

    def _filter_schema(self, request):
        user = request.user

        if not (user.is_authenticated and user.has_perm('auth.view_user')):
            schema = self.schema.graphql_schema
            type_map = schema.type_map

            if 'UserType' in type_map:
                del type_map['UserType']

            if 'Query' in type_map and 'user' in type_map['Query'].fields:
                del type_map['Query'].fields['user']

    def execute_graphql_request(self, request, data, query, variables, operation_name, context):
        self._filter_schema(request)
        return super().execute_graphql_request(
            request, data, query, variables,
            operation_name, context
        )

