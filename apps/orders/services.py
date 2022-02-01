
import requests


class DolarsiService:

    def get_dolars(self):
        """
        get amount in dolar for sale
        """
        response = requests.get(
            'https://www.dolarsi.com/api/api.php?type=valoresprincipales')
        return response.json()[0]['casa']['venta'].replace(',', '.')

    def convert(self, amount):
        """
        calculate total in usd
        """
        result = float(self.get_dolars()) * float(amount)
        return "{:.2f}".format(result)
