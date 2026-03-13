class AppError(Exception):
    """Базовое исключение приложения"""
    pass


class ConflictError(AppError):
    """Ресурс уже существует"""
    pass


class UnauthorizedError(AppError):
    """Ошибка аутентификации"""
    pass


class ForbiddenError(AppError):
    """Запрещено (нет прав)"""
    pass


class NotFoundError(AppError):
    """Ресурс не найден"""
    pass


class ExternalServiceError(AppError):
    """Ошибка внешнего сервиса"""
    pass