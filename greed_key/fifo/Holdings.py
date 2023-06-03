class Holding:
    """
    class Holding : for storing the bought quantity and price information of the stock and providing the methods for
    finding the average buy price and quantity of the holdings
    """
    def __init__(self, quantity, price):
        self.quantity = quantity
        self.price = price

    @staticmethod
    def sell_from_holding_using_fifo(holdings, sell_quantity):
        """
        method to sell the given quantity of stock from the current holdings in FIFO order
        :param holdings: list of objects of the Holdings(Basically bought transaction data)
        :param sell_quantity: number of the quantity sold of the stock
        :return: list of objects of the Holding
        """

        # Finding the total number of the quantity of the stock
        total_quantity = 0
        for holding in holdings:
            total_quantity = total_quantity + holding.quantity

        # Reducing the quantity of stock in FIFO order
        if total_quantity >= sell_quantity:
            iterator = 0
            while sell_quantity != 0:
                if holdings[iterator].quantity != 0:
                    if sell_quantity <= holdings[iterator].quantity:
                        holdings[iterator].quantity = holdings[iterator].quantity - sell_quantity
                        sell_quantity = 0
                    else:
                        sell_quantity = sell_quantity - holdings[iterator].quantity
                        holdings[iterator].quantity = 0
                iterator = iterator + 1
        else:
            raise Exception('Invalid Sell Quantity')

        return holdings

    @staticmethod
    def get_avg_buy_price_net_quantity(holdings):
        """
        this method gives the average buy price and the quantity
        :param holdings: list of objects of the Holding
        :return: average buy price and the quantity
        """
        total_quantity = 0
        total_money = 0

        # finding the total quantity and the total money used to buy that quantity of stock
        for holding in holdings:
            total_money = total_money + (holding.quantity * holding.price)
            total_quantity = total_quantity + holding.quantity

        if total_quantity == 0:
            return 0, 0
        return total_money / total_quantity, total_quantity
