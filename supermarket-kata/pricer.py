"""
Implement a solution to the Supermarket cash register problem, using models
discussed during kata exercise.
"""

from decimal import Decimal


###
###  Base Data Objects (pojo's)
###

class _DataObject(object):
    """ helper base class that allows keyword args in constructor to become
        attributes of instance
    """

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class Item(_DataObject):
    """ An item represents something in your shopping cart.
    """

    name = None
    sku = None
    strategy = None  # instance of a PricingStrategy implementation
    pricing = None   # instance of a Pricing object


class Pricing(_DataObject):
    """ All the pricing data needed for an item in the store
    """

    base_price = None
    unit = None      # lb, each




###
###   Pricing Strategies
###

class StrategyInterface(object):
    """ Abstract base class for different Pricing Strategies for products in the
        store
    """

    def price_for(self, pricing, units):
        """ Given pricing data for an item and the number of units, return a
            price
        """
        raise NotImplementedError

    def discount_for(self, pricing, total_units):
        """ Given a total number of units in the cart, return a discount """
        return 0


class BasePricePerUnitStrategy(StrategyInterface):
    """ Implementation of a PricingStrategy that only cares about base price """

    def price_for(self, pricing, units):
        return pricing.base_price * units


class BasePriceWithDiscountAfterXItems(BasePricePerUnitStrategy, _DataObject):
    """ Implementation of a PricingStrategy that will use base price normally,
        but when a certain threshold is reached, it will lower the price.  An
        example would be "5 for $10, or $3 each".
    """

    discount = None
    break_point = None

    def discount_for(self, pricing, total_units):
        if total_units % self.break_point == 0:
            return self.discount * total_units


class BuyXGetYFreeStrategy(BasePricePerUnitStrategy, _DataObject):
    """ Implementation of a PricingStrategy that will use base price normally,
        but when a threshhold is reached, it will discount the appropriate
        amount.  Examples are "Buy 1 Get 1 Free" or "Buy 5 Get 2 Free".
    """

    x = None
    y = None

    def discount_for(self, pricing, total_units):
        if total_units % (self.x + 1) == 0:
            return self.y * pricing.base_price



###
###  Store Data
###

class InventoryAdapter(object):
    """ The inventory adapter knows about the products and prices in the store
    """

    def __init__(self):
        self.inventory = {
        'chips': Item(name='Chips',
                      strategy=BasePricePerUnitStrategy(),
                      pricing=Pricing(base_price=Decimal('3.00'), unit='each'),
                      sku=10001),
        'apples': Item(name='Apples ($2/lb)',
                      strategy=BasePricePerUnitStrategy(),
                      pricing=Pricing(base_price=Decimal('2.00'), unit='lb'),
                      sku=10002),
        'cereal': Item(name='Cereal',
                      strategy=BasePriceWithDiscountAfterXItems(discount=Decimal('0.50'), break_point=4),
                      pricing=Pricing(base_price=Decimal('3.00'), unit='each'),
                      sku=10003),
        'ice_cream': Item(name='Ice Cream',
                      strategy=BuyXGetYFreeStrategy(x=2, y=1),
                      pricing=Pricing(base_price=Decimal('4.00'), unit='each'),
                      sku=10004)
        }

    def by_sku(self, sku):
        return [item for item in self.inventory.values() if item.sku == sku][0]

    def by_name(self, name):
        return self.inventory[name]




###
###  The Engine
###

class Register(object):
    """ The Cash Register maintains most of the brains about how to price the
        items in the user's cart.
    """

    def __init__(self, inventory_adapter):
        self.items = []
        self.inventory_adapter = inventory_adapter

    def reset(self):
        """ Clear out the items for this transaction """
        self.items = []

    def add_item(self, sku, units=1):
        """ Add an item to this transaction
            @param sku
            @param units (either quantity or weight in pounds)
        """
        item = self.inventory_adapter.by_sku(sku)
        self.items.append((units, item))

    def print_receipt(self):
        """ Print out the current pricing state for the transaction
        """
        output = []
        total = Decimal(0)
        total_units = {}
        total_discounts = {}
        for units, item in self.items:
            price = item.strategy.price_for(item.pricing, units)
            total += price
            output.append('%s  $%s' % (item.name, price))

            current_total = total_units.setdefault(item.sku, 0)
            total_units[item.sku] += units
            discount = item.strategy.discount_for(item.pricing, total_units[item.sku])
            if discount:
                total_discount = total_discounts.setdefault(item.sku, 0)
                this_discount = discount - total_discount
                total_discounts[item.sku] += discount
                total -= this_discount
                output.append('* Discount  -$%s' % this_discount)
        output.append('------------')
        output.append('Total  $%s' % total)
        print "\n".join(output)
        return "\n".join(output)

