import unittest
from mock import Mock
from mock import call
from pcp_mpstat import CpuUtilReporter

class TestCpuUtilReporter(unittest.TestCase):
    def setUp(self):
        self.cpu_usage_total = Mock(
                            user_time = Mock(return_value = 1.23),
                            nice_time = Mock(return_value = 2.34),
                            sys_time = Mock(return_value =  3.45),
                            iowait_time = Mock(return_value = 4.56),
                            irq_hard = Mock(return_value = 5.67),
                            irq_soft = Mock(return_value = 6.78),
                            steal = Mock(return_value = 7.89),
                            guest_time = Mock(return_value = 8.90),
                            guest_nice = Mock(return_value = 1.34),
                            idle_time = Mock(return_value = 2.45)
                        )
        self.cpu_usage_1 = Mock(
                            cpu_number = Mock(return_value = 1),
                            user_time = Mock(return_value = 1.43),
                            nice_time = Mock(return_value = 2.35),
                            sys_time = Mock(return_value =  2.45),
                            iowait_time = Mock(return_value = 3.76),
                            irq_hard = Mock(return_value = 6.45),
                            irq_soft = Mock(return_value = 2.58),
                            steal = Mock(return_value = 2.59),
                            guest_time = Mock(return_value = 5.60),
                            guest_nice = Mock(return_value = 2.34),
                            idle_time = Mock(return_value = 6.67)
                        )
        self.cpu_usage_2 = Mock(
                            cpu_number = Mock(return_value = 2),
                            user_time = Mock(return_value = 2.43),
                            nice_time = Mock(return_value = 3.35),
                            sys_time = Mock(return_value =  5.45),
                            iowait_time = Mock(return_value = 2.76),
                            irq_hard = Mock(return_value = 7.45),
                            irq_soft = Mock(return_value = 3.58),
                            steal = Mock(return_value = 6.59),
                            guest_time = Mock(return_value = 2.60),
                            guest_nice = Mock(return_value = 7.34),
                            idle_time = Mock(return_value = 3.67)
                        )

    def test_print_report_with_no_options(self):
        options = Mock()
        options.cpu_list = None
        cpu_filter = Mock()
        cpu_filter.filter_cpus = Mock(return_value = [])
        cpu_util = Mock()
        cpu_util.get_totalcpu_util = Mock(return_value = self.cpu_usage_total)
        printer = Mock()
        report = CpuUtilReporter(cpu_filter, printer, options)
        timestamp = '2016-7-18 IST'

        report.print_report(cpu_util, timestamp)

        printer.assert_called_with('2016-7-18 IST\tALL\t 1.23\t  2.34\t 3.45\t    4.56\t 5.67\t  6.78\t   7.89\t    8.9\t  1.34\t  2.45')

    def test_print_report_with_online_cpus(self):
        options = Mock()
        options.cpu_list = "ON"
        cpu_filter = Mock()
        cpu_filter.filter_cpus = Mock(return_value = [self.cpu_usage_1, self.cpu_usage_2])
        printer = Mock()
        cpu_util = Mock()
        timestamp = '2016-7-18 IST'
        report = CpuUtilReporter(cpu_filter, printer, options)

        report.print_report(cpu_util, timestamp)

        calls = [call(' Timestamp\tCPU\t %usr\t %nice\t %sys\t %iowait\t %irq\t %soft\t %steal\t %guest\t %nice\t %idle'),
                 call('2016-7-18 IST\t  1\t 1.43\t  2.35\t 2.45\t    3.76\t 6.45\t  2.58\t   2.59\t    5.6\t  2.34\t  6.67'),
                 call('2016-7-18 IST\t  2\t 2.43\t  3.35\t 5.45\t    2.76\t 7.45\t  3.58\t   6.59\t    2.6\t  7.34\t  3.67')]

        printer.assert_has_calls(calls)

    def test_print_report_with_option_all(self):
        options = Mock()
        options.cpu_list = "ALL"
        cpu_filter = Mock()
        cpu_filter.filter_cpus = Mock(return_value = [self.cpu_usage_1, self.cpu_usage_2])
        printer = Mock()
        cpu_util = Mock()
        cpu_util.get_totalcpu_util = Mock(return_value = self.cpu_usage_total)
        timestamp = '2016-7-18 IST'
        report = CpuUtilReporter(cpu_filter, printer, options)

        report.print_report(cpu_util, timestamp)

        calls = [call(' Timestamp\tCPU\t %usr\t %nice\t %sys\t %iowait\t %irq\t %soft\t %steal\t %guest\t %nice\t %idle'),
                 call('2016-7-18 IST\tALL\t 1.23\t  2.34\t 3.45\t    4.56\t 5.67\t  6.78\t   7.89\t    8.9\t  1.34\t  2.45'),
                 call('2016-7-18 IST\t  1\t 1.43\t  2.35\t 2.45\t    3.76\t 6.45\t  2.58\t   2.59\t    5.6\t  2.34\t  6.67'),
                 call('2016-7-18 IST\t  2\t 2.43\t  3.35\t 5.45\t    2.76\t 7.45\t  3.58\t   6.59\t    2.6\t  7.34\t  3.67')]

        printer.assert_has_calls(calls)

if __name__ == "__main__":
    unittest.main()
