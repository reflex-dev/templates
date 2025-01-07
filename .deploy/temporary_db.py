# reflex-dev/templates:.deploy/temporary_db.py to create default reflex.db when deployed
import reflex as rx

rx.utils.prerequisites.check_db_initialized() or rx.Model.alembic_init()
rx.Model.migrate(autogenerate=True)
