import unittest
from mock import Mock,MagicMock
import mock
from pcp_mpstat import MetricRepository

class MetricRepositoryTest(unittest.TestCase):

    def test_returns_the_current_value_for_a_metric_that_has_instances(self):
        utime_mock = Mock(
            netValues = [(Mock(inst=111),'dummyprocess',12345)],
            netPrevValues = [(Mock(inst=111),'dummyprocess',12354)]
        )
        group = {'kernel.percpu.cpu.user':utime_mock}
        m_repo = MetricRepository(group)

        c_utime = m_repo.current_value('kernel.percpu.cpu.user',111)

        self.assertEquals(c_utime,12345)

    def test_returns_the_current_value_for_a_metric_that_has_no_instances(self):
        utime_mock = Mock(
            netValues = [('NULL',None,12345)],
            netPrevValues = [('NULL',None,12354)]
        )
        group = {'kernel.all.cpu.user':utime_mock}
        m_repo = MetricRepository(group)

        c_utime = m_repo.current_value('kernel.all.cpu.user',None)

        self.assertEquals(c_utime,12345)

    def test_returns_none_if_a_metric_does_not_exist_for_an_instance(self):
        utime_mock = Mock(
            netValues = [(Mock(inst=111),'dummyprocess',12345)],
            netPrevValues = [(Mock(inst=111),'dummyprocess',12354)]
        )
        group = {'kernel.percpu.cpu.user':utime_mock}
        m_repo = MetricRepository(group)

        c_utime = m_repo.current_value('kernel.percpu.cpu.vuser',111)

        self.assertIsNone(c_utime)

    def test_returns_none_if_a_metric_does_not_exist_for_a_metric_that_has_no_instance(self):
        utime_mock = Mock(
            netValues = [('NULL',None,12345)],
            netPrevValues = [('NULL',None,12354)]
        )
        group = {'kernel.all.cpu.user':utime_mock}
        m_repo = MetricRepository(group)

        c_utime = m_repo.current_value('kernel.all.cpu.guest',None)

        self.assertIsNone(c_utime)

    def test_returns_the_previous_value_for_a_metric_that_has_instances(self):
        utime_mock = Mock(
            netValues = [(Mock(inst=111),'dummyprocess',12345)],
            netPrevValues = [(Mock(inst=111),'dummyprocess',12354)]
        )
        group = {'kernel.percpu.cpu.user':utime_mock}
        m_repo = MetricRepository(group)

        c_utime = m_repo.previous_value('kernel.percpu.cpu.user',111)

        self.assertEquals(c_utime,12354)

    def test_returns_the_previous_value_for_a_metric_that_has_no_instances(self):
        utime_mock = Mock(
            netValues = [('NULL',None,12345)],
            netPrevValues = [('NULL',None,12354)]
        )
        group = {'kernel.all.cpu.user':utime_mock}
        m_repo = MetricRepository(group)

        c_utime = m_repo.previous_value('kernel.all.cpu.user',None)

        self.assertEquals(c_utime,12354)

    def test_returns_none_if_a_metric_for_previous_value_does_not_exist_for_an_instance(self):
        utime_mock = Mock(
            netValues = [(Mock(inst=111),'dummyprocess',12345)],
            netPrevValues = [(Mock(inst=111),'dummyprocess',12354)]
        )
        group = {'kernel.percpu.cpu.user':utime_mock}
        m_repo = MetricRepository(group)

        c_utime = m_repo.previous_value('kernel.percpu.cpu.vuser',111)

        self.assertIsNone(c_utime)

    def test_returns_none_if_a_metric_for_previous_value_does_not_exist_for_a_metric_that_has_no_instance(self):
        utime_mock = Mock(
            netValues = [('NULL',None,12345)],
            netPrevValues = [('NULL',None,12354)]
        )
        group = {'kernel.all.cpu.user':utime_mock}
        m_repo = MetricRepository(group)

        c_utime = m_repo.previous_value('kernel.all.cpu.guest',None)

        self.assertIsNone(c_utime)

    def test_checks_if_metric_values_are_fetched_only_once_if_not_available(self):
        proc_utime_mock = Mock(
            netValues = [(Mock(inst=111),'dummyprocess',12345)],
            netPrevValues = [(Mock(inst=111),'dummyprocess',12354)]
        )
        group = {'kernel.percpu.cpu.user':proc_utime_mock}
        m_repo = MetricRepository(group)

        with mock.patch.object(m_repo,'_MetricRepository__fetch_current_values',return_value={111:12345}) as method:
            c_ptime = m_repo.current_value('kernel.percpu.cpu.user',111)
            fetch_call_count = method.call_count

        self.assertEquals(fetch_call_count,1)

    def test_checks_if_metric_values_are_not_fetched_if_already_available(self):
        proc_utime_mock = Mock(
            netValues = [(Mock(inst=111),'dummyprocess',12345)],
            netPrevValues = [(Mock(inst=111),'dummyprocess',12354)]
        )
        group = {'kernel.percpu.cpu.user':proc_utime_mock}
        m_repo = MetricRepository(group)
        m_repo.current_cached_values = {'kernel.percpu.cpu.user':{111:12354}}

        with mock.patch.object(m_repo,'_MetricRepository__fetch_current_values',return_value={111:12345}) as method:
            c_ptime = m_repo.current_value('kernel.percpu.cpu.user',111)
            fetch_call_count = method.call_count

        self.assertEquals(fetch_call_count,0)

if __name__ == "__main__":
    unittest.main()
