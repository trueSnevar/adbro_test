
class IntrospectionDisabledException(Exception):
    """
    Custom exception to handle unauthorized introspection attempts.
    """
    def __init__(self, message, name='Query'):
        super().__init__(message)
        self._name = name

class FieldVisibilityMiddleware:
    """
    Middleware that hides the 'user' field from introspection for users
    without the 'auth.view_user' permission or superuser access.
    """

    def _user_is_allowed_to_introspect(self, user) -> bool:
        """ Determine if the user is allowed
         to introspect the schema.
        """
        return user.is_authenticated and user.is_superuser

    def resolve(self, next_resolver, root, info, **kwargs):
        if info.field_name.lower() in ['__schema', '__type']:
            if not self._user_is_allowed_to_introspect(info.context.user):
                raise IntrospectionDisabledException(
                    f"Cannot query field 'user' on type '{kwargs.get('name', 'Query')}'",
                    kwargs.get('name', 'Query')
                )

        return next_resolver(root, info, **kwargs)
