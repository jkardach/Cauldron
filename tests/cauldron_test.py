import cauldron
import multiprocessing
import unittest


class MockCauldron(cauldron.ICauldron):
    def __init__(self):
        self.explosion_called_count = multiprocessing.Value("i", 0)

    def cause_explosion(self):
        with self.explosion_called_count.get_lock():
            self.explosion_called_count += 1


class TestCauldron(unittest.TestCase):
    def test_cauldron_comm(self):
        mock_cauldron = MockCauldron()
        proc = cauldron.CauldronProcess(mock_cauldron)
        events = cauldron.CauldronEvents()
        process = multiprocessing.Process(
            name="CauldronProcess",
            target=proc.wait_for_events,
            args=(events,),
        )
        process.start()

        self.assertEqual(mock_cauldron.explosion_called_count.get_obj(), 0)
        events.cause_explosion()
        self.assertEqual(mock_cauldron.explosion_called_count.get_obj(), 1)
        events.cause_explosion()
        self.assertEqual(mock_cauldron.explosion_called_count.get_obj(), 2)
        events.cause_explosion()
        self.assertEqual(mock_cauldron.explosion_called_count.get_obj(), 3)

        process.join()


if __name__ == "__main__":
    unittest.main()
