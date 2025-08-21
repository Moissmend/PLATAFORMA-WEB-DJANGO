class SistemaPrincipalRouter:

    router_app_labels = {'catalogos', 'clientes', 'configuraciones', 'empleados', }

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.router_app_labels:
            return 'finsurhn_sp_db'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.router_app_labels:
            return 'finsurhn_sp_db'
        return None
    
    def allow_relation(self, obj1, obj2, **hints):
        if(
            obj1._meta.app_label in self.router_app_labels or
            obj2._meta.app_label in self.router_app_labels
        ):
            return True
        return None
    
    #NO MIGRATE
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return None