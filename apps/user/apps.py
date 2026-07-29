from django.apps import AppConfig

# Config do app: define o nome e cria o gestor padrão após migrações
class UserConfig(AppConfig):
    name = 'apps.user'

    def ready(self):
        from django.db.models.signals import post_migrate
        from django.dispatch import receiver

        @receiver(post_migrate)
        def create_default_user_system(sender, **kwargs):
            
            if sender.name == 'apps.user':
                from .models import User

                if not User.objects.filter(username='admin').exists():
                    admin = User(
                        username='admin',
                        public=False,
                        about='Super User',
                        tipo='ADMIN',
                    )
                    admin.set_password('admin123')
                    admin.save()
