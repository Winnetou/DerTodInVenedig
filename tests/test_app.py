import os
import pandas
import unittest

from DerTodInVenedig.app import app, validate, query_data

from DerTodInVenedig.converter import read_data_to_df


class AppE2ETest(unittest.TestCase):
    def setUp(self):
        super(AppE2ETest, self).setUp()
        self.valid_url = '/mortality_rate?country_code=DEU&year_from=1950&year_to=1976&mr_type=IMR'
        self.invalid_url = '/mortality_rate?country_code=ZU&year_from=20&year_to=zz&mr_type=STDS'

    def test_request_happy_path(self):
        with app.test_client() as client:
            response = client.get(self.valid_url)
            self.assertEquals(response.status_code, 200)

    def test_request_unhappy_path(self):
        with app.test_client() as client:
            response = client.get(self.invalid_url)
            self.assertEqual(response.status_code, 422)


class BackendTest(unittest.TestCase):
    def test_validate_happy_path(self):
        try:
            validate('DEU', '1970', '1980', 'U5MR')
        except:
            self.fail()

    def test_validate_unhappy_path(self):
        self.assertRaises(AssertionError, validate, 'DEU', '1258', '2019', 'U2')

    def test_query(self):
        reality = query_data('DEU', '1970', '1971', 'IMR')
        self.assertIsInstance(reality['avg_value'], float)


class ConverterTest(unittest.TestCase):

    def setUp(self):
        super(ConverterTest, self).setUp()
        data_dir = 'data'
        file_name = 'RatesDeaths_AllIndicators.xlsx'
        self.data_file_path = os.path.join(data_dir, file_name)

    def test_data_format(self):
        ''' 
        Check we get a DF object with 
        columns, index on 
        it should have years, iso codes, etc
        '''
        data = read_data_to_df(self.data_file_path)
        self.assertIsInstance(data, pandas.DataFrame)
        for expected_column in ['U5MR', 'IMR', 'NMR']:
            self.assertIn(expected_column, data)
        # should have 'year' and 'ISO Code'
        for expected_column in ['year', 'ISO Code']:
            self.assertIn(expected_column, data.index.names)


if __name__ == '__main__':
    unittest.main()
