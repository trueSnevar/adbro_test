
class IntrospectionDisabledException(Exception):
    """ Custom exception to handle
    unauthorized introspection attempts.
    """
    def __init__(self, message, name='Query'):
        super().__init__(message)
        self._name = name

class FieldVisibilityMiddleware:
    """
    Middleware that hides the 'user' field from introspection for users
    without the 'auth.view_user' permission or superuser access.
    """

    def _user_can_view_user_field(self, user) -> bool:
        """ Determine if the user is allowed
         to introspect the schema.
        """
        return user.is_authenticated and user.has_perm('auth.view_user')

    def resolve(self, next_resolver, root, info, **kwargs):
        """
        Filter out the 'user' field for users
        without the 'auth.view_user' permission.
        """
        if info.field_name == '__type':
            result = next_resolver(root, info, **kwargs)
            if hasattr(result, 'fields') and isinstance(result.fields, dict):
                if not self._user_can_view_user_field(info.context.user):
                    if 'user' in result.fields:
                        del result.fields['user']

            return result

        return next_resolver(root, info, **kwargs)

