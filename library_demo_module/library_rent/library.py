from trytond.pool import *
from trytond.model import fields

# set __meta__ to use Trytons inheritance model
from trytond.transaction import Transaction

__metaclass__ = PoolMeta
__ALL__ = ['Book', 'Party']



class Book:
    # A model for 'Book'
    "BOOK"
    # To extend our Model all we have to do is instanciate a new class
    # and set __name__ to be the same as the model to extend
    __name__ = 'library.book'

    # A relational field to point on (one) party
    renter = fields.Many2One('party.party', 'Rented by')
    available = fields.Function(fields.Boolean('Available for rent'), 'on_change_with_available')

    @fields.depends('renter')
    def on_change_with_available(self, name=None):
        return self.renter == None


class Party:
    __name__ = 'party.party'

    # Reverse relation for book.renter (reference to all rented books)
    rented_books = fields.One2Many('library.book', 'renter', 'Rented Books')