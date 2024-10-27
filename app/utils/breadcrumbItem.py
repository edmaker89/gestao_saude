from typing import List, Optional, Dict  

class BreadcrumbItem:  
    def __init__(self, url: str, label: str, params: Optional[Dict] = None):  
        self.url = url  
        self.label = label  
        self.params = params if params is not None else {}  

class BreadcrumbManager:  
    def __init__(self):  
        self.routes = [  
            BreadcrumbItem('index', 'Início'),   
            BreadcrumbItem('aviso_new', 'Novo Aviso'),   
            BreadcrumbItem('aviso_edit', 'Editar Aviso'),   
        ]  

    def get_route(self, label_route: str) -> Optional[BreadcrumbItem]:  
        for item in self.routes:  
            if item.label == label_route:  
                return item  
        return None  
    
    def create_breadcrumbs(self, label_routes: List[str], params: Optional[List[Dict]] = None) -> List[BreadcrumbItem]:  
        breadcrumbs = []  
        for index, label in enumerate(label_routes):  
            item = self.get_route(label)  
            if item is not None:  
                # Se houver parâmetros para essa rota, atualize os parâmetros do BreadcrumbItem  
                if params is not None and index < len(params):  
                    item.params.update(params[index])  
                breadcrumbs.append(item)  
        return breadcrumbs 
    
    def transformar_rotas(self, rotas):  
        # Inicializa a lista que irá armazenar os rótulos e parâmetros  
        label_routes = []  
        params = []  

        # Percorre cada tupla na lista de rotas  
        for rot in rotas:  
            label, param = rot  
            label_routes.append(label)  # Adiciona o rótulo  
            params.append(param)         # Adiciona os parâmetros  

        return label_routes, params
    
    def gerar_breads(self, rotas):
        label_routes, params = self.transformar_rotas(rotas)
        breads = self.create_breadcrumbs(label_routes, params)
        return breads