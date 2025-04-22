from django.db import models


class Role(models.TextChoices):
    OPERATOR = 'OPERATOR', 'Оператор'
    PARKING_ADMIN = 'PARKING_ADMIN', 'Администратор'


class LanguageCode(models.TextChoices):
    EN = 'en', 'English'
    RU = 'ru', 'Русский'


class CriticalityLevel(models.TextChoices):
    EVENT = 'EVENT', 'Событие'
    INCIDENT = 'INCIDENT', 'Инцидент'


class TicketSection(models.TextChoices):
    NEW = 'NEW', 'Новая'
    L2 = 'L2', 'Вторая линия'
    L3 = 'L3', 'Третья линия'
    CANCELLED = 'CANCELLED', 'Отменено'
    DONE = 'DONE', 'Завершено'


class ProblemFrequency(models.TextChoices):
    ONE_TIME = 'ONE_TIME', 'Разовая проблема'
    PERIODIC = 'PERIODIC', 'Периодически повторяющаяся'


class IssueStatusClosed(models.TextChoices):
    CHECKED = 'CHECKED', 'Проверено'
    CANCELED = 'CANCELED', 'Отменено'
    DUPLICATED = 'DUPLICATED', 'Дубликат'


class ProblemArea(models.TextChoices):
    SHLAGBAUM = 'SHLAGBAUM', 'Шлагбаум'
    CONTROLLER = 'CONTROLLER', 'Контроллер'
    CALL_PANEL = 'CALL_PANEL', 'Вызывная панель'
    QR_PANEL = 'QR_PANEL', 'QR панель'
    FIXED_CAMERAS = 'FIXED_CAMERAS', 'Камеры фикс'
    SURVEILLANCE_CAMERA = 'SURVEILLANCE_CAMERA', 'Камера обзорная'
    VIDEO_RECORDER = 'VIDEO_RECORDER', 'Видеорегистратор'
    SWITCH = 'SWITCH', 'Коммутатор'
    RADOMOSTY = 'RADOMOSTY', 'Радиомосты'
    LOCAL_NETWORK = 'LOCAL_NETWORK', 'Локальная Сеть'
    INTERNET = 'INTERNET', 'Интернет'
    OPERATOR_PC = 'OPERATOR_PC', 'ПК Оператора'
    SERVER = 'SERVER', 'Сервер'
    RECOGNITION = 'RECOGNITION', 'Распознавание'
    BILLING_SOFTWARE = 'BILLING_SOFTWARE', 'Софт - биллинг'
    REPORTS = 'REPORTS', 'Отчёты'
    TELEGRAM_BOT = 'TELEGRAM_BOT', 'Телеграмм бот'
    PAYMENTS = 'PAYMENTS', 'Платежи'
    MONITORING = 'MONITORING', 'Мониторинг'
    PHONE = 'PHONE', 'Телефон'
    ATS = 'ATS', 'АТС'
    FISCALIZATION = 'FISCALIZATION', 'Фискализация'
    INTEGRATION = 'INTEGRATION', 'Интеграция с другим ПО'
    MOBILE_APP = 'MOBILE_APP', 'Мобильное приложение Паркур'


class City(models.TextChoices):
    ALMATY = 'ALMATY', 'АЛМАТЫ'
    ASTANA = 'ASTANA', 'АСТАНА'
    SHYMKENT = 'SHYMKENT', 'ШЫМКЕНТ'
    OTHER = 'OTHER', 'ДРУГОЙ'


class EventProblems(models.TextChoices):
    FIX_MASK_HANGS_FLARE = 'FIX_MASK_HANGS_FLARE', 'Фикса (маска, зависания, засвет)'
    CALLS_NOT_WORKING = 'CALLS_NOT_WORKING', 'Звонки не работают'
    INCORRECT_GATE_PROCESSING = 'INCORRECT_GATE_PROCESSING', 'Некорректная отработка шлагбаума'
    SOFTWARE_BUG = 'SOFTWARE_BUG', 'Баг'
    ENGINEER_REQUIRED = 'ENGINEER_REQUIRED', 'Нужен инженер'
    OTHER = 'OTHER', 'Другое'


class IncidentProblems(models.TextChoices):
    FIX_FULLY_DROPPED = 'FIX_FULLY_DROPPED', 'Фикса полностью слетела'
    SOFTWARE_CRASHED = 'SOFTWARE_CRASHED', 'Софт упал'
    KASPI_PAYMENTS_UNAVAILABLE = 'KASPI_PAYMENTS_UNAVAILABLE', 'Каспи платежи не доступны'
    OVERLOADED_POST_BROKEN = 'OVERLOADED_POST_BROKEN', 'Нагруженный пост сломался'
    INTERNET_DISCONNECTED = 'INTERNET_DISCONNECTED', 'Интернет выключился'
    OTHER = 'OTHER', 'Другое'


class State(models.TextChoices):
    START = 'START', 'Старт'
    ADMIN = 'ADMIN', 'Админ'
    PARKING = 'PARKING', 'Парковка'
    WAITING_PARKING = 'WAITING_PARKING', 'Ожидается выбор парковки'
    WAITING_CRITICALITY = 'WAITING_CRITICALITY', 'Ожидается уровень критичности'
    WAITING_PROBLEM_AREA = 'WAITING_PROBLEM_AREA', 'Ожидается область проблемы'
    WAITING_DESCRIPTION = 'WAITING_DESCRIPTION', 'Ожидается описание'
    CONTACT = 'CONTACT', 'Контакт'
    WAITING_ADD_USER = 'WAITING_ADD_USER', 'Ожидается номер пользователя'
    WAITING_ADD_USER_ROLE = 'WAITING_ADD_USER_ROLE', 'Ожидается роль'
    SEARCHING = 'SEARCHING', 'Поиск'
    WAITING_SEARCHING = 'WAITING_SEARCHING', 'Ожидается ответ от поиска'
    CANCELLED = 'CANCELLED', 'Отменено'
    ADMIN_WAITING_PARKING = 'ADMIN_WAITING_PARKING', 'Админ: ожидание парковки'
    ADMIN_WAITING_OPERATOR = 'ADMIN_WAITING_OPERATOR', 'Админ: ожидание оператора'
    ADMIN_OPERATORS_PARKING = 'ADMIN_OPERATORS_PARKING', 'Админ: назначение парковки'
    ADMIN_WAITING_OPERATORS_PARKING = 'ADMIN_WAITING_OPERATORS_PARKING', 'Админ: ожидание парковок'
    ADMIN_WAITING_DUTY_OPERATOR = 'ADMIN_WAITING_DUTY_OPERATOR', 'Админ: ожидание дежурного'
    ADMIN_WAITING_DUTY_DATE = 'ADMIN_WAITING_DUTY_DATE', 'Админ: ожидание даты'
    ADMIN_WAITING_OPERATORS_MANAGING = 'ADMIN_WAITING_OPERATORS_MANAGING', 'Управление операторами'
    ADMIN_WAITING_MANAGE_PARKING = 'ADMIN_WAITING_MANAGE_PARKING', 'Управление парковками'
    ADMIN_WAITING_MANAGE_PARKING_OPERATOR = 'ADMIN_WAITING_MANAGE_PARKING_OPERATOR', 'Управление оператором'
    ADMIN_WAITING_PARKINGS_MANAGING = 'ADMIN_WAITING_PARKINGS_MANAGING', 'Ожидание парковок'
    ADMIN_WAITING_SET_ADMIN = 'ADMIN_WAITING_SET_ADMIN', 'Ожидание назначения админа'
    ADMIN_WAITING_SET_USER = 'ADMIN_WAITING_SET_USER', 'Ожидание пользователя'
    ADMIN_WAITING_GROUP_NAME = 'ADMIN_WAITING_GROUP_NAME', 'Ожидание имени группы'


class AsanaIssueStatus(models.TextChoices):
    CREATED = 'CREATED', 'Создано'
    UNDER_ANALYSIS = 'UNDER_ANALYSIS', 'На анализе'
    ASSIGNEE_APPOINTED = 'ASSIGNEE_APPOINTED', 'Исполнитель назначен'
    IN_PROGRESS = 'IN_PROGRESS', 'В исполнении'
    COMPLETED = 'COMPLETED', 'Выполнено'
    NOT_COMPLETED = 'NOT_COMPLETED', 'Не выполнено'
    VERIFIED = 'VERIFIED', 'Проверено'
    CANCELED = 'CANCELED', 'Отменено'
    DUPLICATE = 'DUPLICATE', 'Дубликат'
    FOR_REVISION = 'FOR_REVISION', 'На доработку'