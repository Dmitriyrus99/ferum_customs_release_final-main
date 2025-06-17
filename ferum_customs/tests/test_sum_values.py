from ferum_customs.utilities import sum_values


class TestSumValues:
    def test_sum_of_list(self):
        assert sum_values([1, 2, 3]) == 6.0

    def test_empty_iterable(self):
        assert sum_values([]) == 0.0

    def test_mixed_numbers(self):
        assert sum_values([-1, 2.5, 3]) == 4.5
