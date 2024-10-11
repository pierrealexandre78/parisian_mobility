# from src.etl.velib_formater import (
#     velib_station_info_formatter,
#     velib_station_status_formatter,
# )
# import unittest

# # Run it using `python -m src.tests.test_velib_formatter`


# class VelibFormaterTestCases(unittest.TestCase):
#     def test_format_velib_station_status(self):
#         station_status = {
#             "data": {
#                 "stations": [
#                     {
#                         "is_installed": 1,
#                         "is_renting": 1,
#                         "is_returning": 1,
#                         "last_reported": 1727080246,
#                         "numBikesAvailable": 11,
#                         "numDocksAvailable": 2,
#                         "num_bikes_available": 11,
#                         "num_bikes_available_types": [{"ebike": 3, "mechanical": 8}],
#                         "num_docks_available": 2,
#                         "station_id": 516395829,
#                     }
#                 ]
#             },
#             "lastUpdatedOther": 1727082804,
#             "ttl": 3600,
#         }

#         expected_output = [
#             {
#                 "uuid": "3fa23a1b2f4a76b0ee3e2338645271ca",
#                 "station_id": 516395829,
#                 "num_bikes_available": 11,
#                 "num_bikes_mechanical": 8,
#                 "num_bikes_ebike": 3,
#                 "num_docks_available": 2,
#                 "is_renting": 1,
#                 "last_updated_other": 1727082804,
#                 "last_reported": 1727080246,
#             }
#         ]
#         self.assertEqual(
#             expected_output, velib_station_status_formatter(station_status)
#         )

#     def test_format_velib_station_info(self):
#         station_info = {
#             "data": {
#                 "stations": [
#                     {
#                         "station_id": 516395829,
#                         "name": "Rue de la Victoire - Clignancourt",
#                         "lat": 48.890127,
#                         "lon": 2.344207,
#                         "capacity": 20,
#                     }
#                 ]
#             },
#             "lastUpdated": 1727082804,
#             "ttl": 3600,
#         }

#         expected_output = [
#             {
#                 "station_id": 516395829,
#                 "name": "Rue de la Victoire - Clignancourt",
#                 "lat": 48.890127,
#                 "long": 2.344207,
#                 "capacity": 20,
#             }
#         ]
#         self.assertEqual(expected_output, velib_station_info_formatter(station_info))


# if __name__ == "__main__":
#     unittest.main()
