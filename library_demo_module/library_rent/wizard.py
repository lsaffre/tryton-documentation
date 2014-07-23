from trytond.wizard import Wizard, StateView, StateAction, Button
from trytond.model import ModelView

class PrintLibraryReportStart(ModelView):
    'Print Library Report'
    __name__ = 'library.print_report.start'

class PrintLibraryReport(Wizard):
    'Print Library Report'
    __name__ = 'library.print_report'

    start = StateView(
        'library.print_report.start', 'library.print_view_form',
        [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Print', 'print_', 'tryton-print', default=True),
            ]
    )
    print_ = StateAction('library.book')

    def do_print_(self, action):
        data = {
            'library': self.start.book.id,
            }
        return action, data

    def transition_print_(self):
        return 'end'