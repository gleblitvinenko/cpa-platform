from rest_framework import permissions


class IsAdminOrBrandUser(permissions.BasePermission):
    """
    Custom permission to allow only admins and brand users to create offers.
    """

    # def has_permission(self, request, view):
    #     if view.action != 'create':
    #         return True
    #
    #     return request.user and (request.user.is_staff or request.user.user_type == 'brand')
    def has_permission(self, request, view):
        # Разрешить просмотр списка офферов для всех
        if view.action == 'list' or view.action == "retrieve":
            return True

        # Разрешить создание офферов только для администраторов и brand
        return request.user and (request.user.is_staff or request.user.user_type == 'brand')

    def has_object_permission(self, request, view, obj):
        # Запретить редактирование и удаление офферов для influencer
        if request.user.user_type == 'influencer' and (view.action in ['update', 'destroy']):
            return False

        # Разрешить просмотр и другие операции для остальных
        return True


class IsInfluencer(permissions.BasePermission):
    """
    Custom permission to allow only influencers to perform the action.
    """

    def has_permission(self, request, view):
        # Пользователь должен быть аутентифицирован
        if not request.user.is_authenticated:
            return False

        # Проверка, что пользователь является "influencer"
        return request.user.user_type == 'influencer'
