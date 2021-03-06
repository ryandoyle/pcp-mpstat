import unittest
from mock import Mock
from mock import call
from pcp_mpstat import InterruptUsageReporter

class TestHardInterruptUsageReporter(unittest.TestCase):
    def setUp(self):
        interrupts = [ Mock(), Mock()]
        interrupts[0].configure_mock(
                            name = Mock(return_value = 'SOME_INTERRUPT'),
                            value = Mock(return_value = 1.23))
        interrupts[1].configure_mock(
                            name = Mock(return_value = 'ANOTHER_INTERRUPT'),
                            value = Mock(return_value = 2.34))
        self.cpu_interrupt_zero = Mock(
                                cpu_number = Mock(return_value = 0) ,
                                interrupts = interrupts
                                )
        self.cpu_interrupt_one = Mock(
                                cpu_number = Mock(return_value = 1),
                                interrupts = interrupts
                                )
    def test_print_report(self):
        interrupt_usage = Mock()
        printer = Mock()
        options = Mock()
        cpu_interrupts = [self.cpu_interrupt_zero]
        interrupt_usage.get_percpu_interrupts = Mock(return_value = cpu_interrupts)
        cpu_filter = Mock()
        cpu_filter.filter_cpus = Mock(return_value = cpu_interrupts)
        report = InterruptUsageReporter(interrupt_usage, cpu_filter, printer, options)
        timestamp = '2016-7-18 IST'
        calls = [call(' Timestamp\t cpu\tSOME_INTERRUPT/s\tANOTHER_INTERRUPT/s\t'),
                call('2016-7-18 IST\t   0\t            1.23\t               2.34\t')]

        report.print_report(timestamp)

        printer.assert_has_calls(calls, any_order = False)

    def test_print_report_with_cpu_filter_on(self):
        interrupt_usage = Mock()
        printer = Mock()
        options = Mock()
        cpu_interrupts = [self.cpu_interrupt_zero, self.cpu_interrupt_one]
        interrupt_usage.get_percpu_interrupts = Mock(return_value = cpu_interrupts)
        cpu_filter = Mock()
        cpu_filter.filter_cpus = Mock(return_value = [self.cpu_interrupt_zero])
        report = InterruptUsageReporter(interrupt_usage, cpu_filter, printer, options)
        timestamp = '2016-7-18 IST'
        calls = [call(' Timestamp\t cpu\tSOME_INTERRUPT/s\tANOTHER_INTERRUPT/s\t'),
                call('2016-7-18 IST\t   0\t            1.23\t               2.34\t')]

        report.print_report(timestamp)

        printer.assert_has_calls(calls, any_order = False)
if __name__ == '__main__':
    unittest.main()
