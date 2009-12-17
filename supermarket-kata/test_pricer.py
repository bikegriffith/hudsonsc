
from nose import tools as NT
from pricer import InventoryAdapter
from pricer import Register


class TestPricingOneItem(object):

    def setup(self):
        self.inventory = InventoryAdapter()
        self.register = Register(self.inventory)

        self.chips = self.inventory.by_name('chips')
        self.apples = self.inventory.by_name('apples')
        self.cereal = self.inventory.by_name('cereal')
        self.ice_cream = self.inventory.by_name('ice_cream')

    def test_should_price_1_bag_of_chips_at_3(self):
        self.register.add_item(self.chips.sku, 1)
        receipt = self.register.print_receipt()
        NT.assert_equals(receipt, "Chips  $3.00\n"\
                                  "------------\n"\
                                  "Total  $3.00")

    def test_should_price_2_bags_of_chips_at_6(self):
        self.register.add_item(self.chips.sku, 1)
        self.register.add_item(self.chips.sku, 1)
        receipt = self.register.print_receipt()
        NT.assert_equals(receipt, "Chips  $3.00\n"\
                                  "Chips  $3.00\n"\
                                  "------------\n"\
                                  "Total  $6.00")

    def test_should_price_apples_at_2_dollars_per_pound(self):
        self.register.add_item(self.apples.sku, 3)
        self.register.add_item(self.apples.sku, 1)
        receipt = self.register.print_receipt()
        NT.assert_equals(receipt, "Apples ($2/lb)  $6.00\n"\
                                  "Apples ($2/lb)  $2.00\n"\
                                  "------------\n"\
                                  "Total  $8.00")

    def test_should_price_cereal_at_3_if_less_than_4_total(self):
        self.register.add_item(self.cereal.sku, 1)
        self.register.add_item(self.cereal.sku, 1)
        self.register.add_item(self.cereal.sku, 1)
        receipt = self.register.print_receipt()
        NT.assert_equals(receipt, "Cereal  $3.00\n"\
                                  "Cereal  $3.00\n"\
                                  "Cereal  $3.00\n"\
                                  "------------\n"\
                                  "Total  $9.00")

    def test_should_discount_cereal_after_4th_is_added(self):
        self.register.add_item(self.cereal.sku, 1)
        self.register.add_item(self.cereal.sku, 1)
        self.register.add_item(self.cereal.sku, 1)
        self.register.add_item(self.cereal.sku, 1)
        receipt = self.register.print_receipt()
        NT.assert_equals(receipt, "Cereal  $3.00\n"\
                                  "Cereal  $3.00\n"\
                                  "Cereal  $3.00\n"\
                                  "Cereal  $3.00\n"\
                                  "* Discount  -$2.00\n"\
                                  "------------\n"\
                                  "Total  $10.00")

    def test_should_discount_cereal_after_4th_is_added_and_again_after_8th(self):
        self.register.add_item(self.cereal.sku, 1)
        self.register.add_item(self.cereal.sku, 1)
        self.register.add_item(self.cereal.sku, 1)
        self.register.add_item(self.cereal.sku, 1)
        self.register.add_item(self.cereal.sku, 1)
        self.register.add_item(self.cereal.sku, 1)
        self.register.add_item(self.cereal.sku, 1)
        self.register.add_item(self.cereal.sku, 1)
        receipt = self.register.print_receipt()
        NT.assert_equals(receipt, "Cereal  $3.00\n"\
                                  "Cereal  $3.00\n"\
                                  "Cereal  $3.00\n"\
                                  "Cereal  $3.00\n"\
                                  "* Discount  -$2.00\n"\
                                  "Cereal  $3.00\n"\
                                  "Cereal  $3.00\n"\
                                  "Cereal  $3.00\n"\
                                  "Cereal  $3.00\n"\
                                  "* Discount  -$2.00\n"\
                                  "------------\n"\
                                  "Total  $20.00")

    def test_should_get_3rd_ice_cream_free(self):
        self.register.add_item(self.ice_cream.sku, 1)
        self.register.add_item(self.ice_cream.sku, 1)
        self.register.add_item(self.ice_cream.sku, 1)
        receipt = self.register.print_receipt()
        NT.assert_equals(receipt, "Ice Cream  $4.00\n"\
                                  "Ice Cream  $4.00\n"\
                                  "Ice Cream  $4.00\n"\
                                  "* Discount  -$4.00\n"\
                                  "------------\n"\
                                  "Total  $8.00")

    def test_it_all(self):
        self.register.add_item(self.apples.sku, 2)
        self.register.add_item(self.apples.sku, 6)
        self.register.add_item(self.ice_cream.sku, 1)
        self.register.add_item(self.apples.sku, 3)
        self.register.add_item(self.ice_cream.sku, 1)
        self.register.add_item(self.cereal.sku, 1)
        self.register.add_item(self.ice_cream.sku, 1)
        self.register.add_item(self.cereal.sku, 1)
        self.register.add_item(self.cereal.sku, 1)
        self.register.add_item(self.cereal.sku, 1)
        self.register.add_item(self.cereal.sku, 1)
        self.register.add_item(self.chips.sku, 1)
        receipt = self.register.print_receipt()
        NT.assert_equals(receipt, "Apples ($2/lb)  $4.00\n"\
                                  "Apples ($2/lb)  $12.00\n"\
                                  "Ice Cream  $4.00\n"\
                                  "Apples ($2/lb)  $6.00\n"\
                                  "Ice Cream  $4.00\n"\
                                  "Cereal  $3.00\n"\
                                  "Ice Cream  $4.00\n"\
                                  "* Discount  -$4.00\n"\
                                  "Cereal  $3.00\n"\
                                  "Cereal  $3.00\n"\
                                  "Cereal  $3.00\n"\
                                  "* Discount  -$2.00\n"\
                                  "Cereal  $3.00\n"\
                                  "Chips  $3.00\n"\
                                  "------------\n"\
                                  "Total  $46.00")

