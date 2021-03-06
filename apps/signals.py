import django.dispatch


# Сигнализирует о добавлении новой сущности.
signal_new_entity = django.dispatch.Signal(providing_args=['entity'])

# Сигнализирует о публикации новой сущности.
signal_entity_published = django.dispatch.Signal(providing_args=['entity'])

# Сигнализирует о том, что пользователь проголосовал за материал или отозвал голос.
signal_support_changed = django.dispatch.Signal()
