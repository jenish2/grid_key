import datetime
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import TransactionSerializer
from .models import Transaction
from .Holdings import Holding
import re


class HoldingsView(APIView):
    """ For managing the holdings of the stock """

    def get(self, request):
        """
        Get the average stock buy price and net holding quantity of the stock
        """

        # Getting teh all the transactions
        transactions = Transaction.objects.all()

        # for storing the buy transaction's data in Holding objects format
        holdings = []

        for transaction in transactions:
            if transaction.transaction_type.lower() == 'buy':
                # if the transaction is a buy transaction then we need to store the buy transaction data in the Holding
                # object format in holding list
                holdings.append(Holding(quantity=transaction.quantity, price=transaction.price))
            elif transaction.transaction_type.lower() == 'split':
                # For a split transaction we need to update the holding objects buy price and quantity data
                for holding in holdings:
                    holding.quantity = holding.quantity * transaction.ratio
                    holding.price = holding.price / transaction.ratio
            elif transaction.transaction_type.lower() == 'sell':
                holding = Holding.sell_from_holding_using_fifo(holdings, sell_quantity=transaction.quantity)
            else:
                raise Exception('Unknown transaction type')

        # Getting the average buy price and total holdings
        avg_buy_price, total_quantity = Holding.get_avg_buy_price_net_quantity(holdings)

        return Response({'avg_buy_price': avg_buy_price, 'total_quantity': total_quantity}, status=status.HTTP_200_OK)


class TransactionView(APIView):
    """Manages transactions"""

    def post(self, request):
        # Getting the transaction data from the request
        data = request.data

        # Pattern in which date should be passed in api request
        pattern_str = r'^\d{2}-\d{2}-\d{4}$'
        # Checking the date format validation
        if not re.match(pattern_str, data.get('date')):
            raise ValidationError('Invalid date :- please give a valid date in "dd-MM-yyyy" format')

        data['date'] = datetime.datetime.strptime(data['date'], "%d-%m-%Y").date()

        # Checking the transaction type is not split then split ration must be zero in api request
        if data.get('transaction_type').lower() in ['buy', 'sell']:
            if data.get('ratio') != 0:
                raise ValidationError('For Buy and Sell transactions must have the same split ratio to zero')

        # Checking the transaction type is split then split ration must be greater than one and quantity and price must
        # be zero in api request
        if data.get('transaction_type').lower() == 'split':
            if data.get('quantity') != 0 or data.get('price') != 0:
                raise ValidationError('For Split transactions must have the price and quantity to zero')
            if data.get('ratio') <= 0:
                raise ValidationError('For Split transactions must have the ratio greater than zero')

        # Checking the Data and Storing in Transaction table
        serializer = TransactionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

        return Response({"msg": "transaction added successfully", "data": serializer.data}, status=status.HTTP_200_OK)
