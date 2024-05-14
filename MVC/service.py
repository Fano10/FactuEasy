from MVC.model import Bill,Product


class ServiceGetProductByBill(object):
    def __init__ (self,id):
        self.id = id
    
    def execute(self):
        products = Product.select().where(Product.idBill == self.id) #select plusieurs resultat tandis que get un seul resultat
        return products