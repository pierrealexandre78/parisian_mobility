# from src.etl.railways_lines_status import railways_lines_status
# import unittest

# raw_data = {
#     "disruptions": [
#         {
#             "id": "495b2cb4-79ab-11ef-ab99-0a58a9feac02",
#             "disruption_id": "d2bf89c0-79a9-11ef-81fe-0a58a9feac02",
#             "impact_id": "495b2cb4-79ab-11ef-ab99-0a58a9feac02",
#             "application_periods": [
#                 {"begin": "20240923T145400", "end": "20240924T051500"}
#             ],
#             "status": "active",
#             "updated_at": "20240923T145644",
#             "tags": ["Actualité"],
#             "cause": "perturbation",
#             "category": "Incidents",
#             "severity": {
#                 "name": "perturbée",
#                 "effect": "SIGNIFICANT_DELAYS",
#                 "color": "#EF662F",
#                 "priority": 30,
#             },
#             "messages": [
#                 {
#                     "text": "Métro 6 : Bagage oublié dans un train - Reprise progressive / trafic reste perturbé",
#                     "channel": {
#                         "content_type": "text/plain",
#                         "id": "17eac900-7a07-11e8-a990-005056a47b86",
#                         "name": "notification",
#                         "types": ["notification"],
#                     },
#                 },
#                 {
#                     "text": "<p>Le trafic reprend mais reste perturbé sur l'ensemble de la ligne en répercussion d'un bagage oublié dans un train à Denfert-Rochereau.<br><a href='http://www.ratp.fr'>Plus d'informations sur le site ratp.fr</a></p>",
#                     "channel": {
#                         "content_type": "text/html",
#                         "id": "3ae8df3e-7488-11e8-ac3b-005056a47b86",
#                         "name": "moteur",
#                         "types": ["web"],
#                     },
#                 },
#                 {
#                     "text": "Métro 6 : Bagage oublié dans un train - Reprise progressive / trafic reste perturbé",
#                     "channel": {
#                         "content_type": "text/plain",
#                         "id": "d9dbc5a6-7a06-11e8-8b8c-005056a44da2",
#                         "name": "titre",
#                         "types": ["title"],
#                     },
#                 },
#             ],
#             "impacted_objects": [
#                 {
#                     "pt_object": {
#                         "id": "line:IDFM:C01376",
#                         "name": "RATP Métro 6",
#                         "quality": 0,
#                         "line": {
#                             "id": "line:IDFM:C01376",
#                             "name": "6",
#                             "code": "6",
#                             "color": "6ECA97",
#                             "text_color": "000000",
#                             "codes": [
#                                 {"type": "Netex_PrivateCode", "value": "100110006"},
#                                 {"type": "source", "value": "FR1:Line:C01376:"},
#                             ],
#                             "physical_modes": [
#                                 {"id": "physical_mode:Metro", "name": "Métro"}
#                             ],
#                             "commercial_mode": {
#                                 "id": "commercial_mode:Metro",
#                                 "name": "Métro",
#                             },
#                             "network": {
#                                 "id": "network:IDFM:Operator_100",
#                                 "name": "RATP",
#                                 "links": [],
#                                 "codes": [
#                                     {"type": "source", "value": "FR1:Operator:100:LOC"}
#                                 ],
#                             },
#                             "opening_time": "052900",
#                             "closing_time": "021500",
#                             "geojson": {"type": "MultiLineString", "coordinates": []},
#                             "links": [],
#                         },
#                         "embedded_type": "line",
#                     }
#                 }
#             ],
#             "uri": "495b2cb4-79ab-11ef-ab99-0a58a9feac02",
#             "disruption_uri": "d2bf89c0-79a9-11ef-81fe-0a58a9feac02",
#             "contributor": "shortterm.tr_idfm",
#         }
#     ]
# }


# # test case using the above raw_data and expected_result
# class RatpLinesStatusFormatterTest(unittest.TestCase):
#     def test_ratp_lines_status_formatter(self):
#         expected_result = [
#             {
#                 "disruption_id": "d2bf89c0-79a9-11ef-81fe-0a58a9feac02",
#                 "begin": "20240923T145400",
#                 "end": "20240924T051500",
#                 "status": "active",
#                 "cause": "perturbation",
#                 "category": "Incidents",
#                 "effect": "SIGNIFICANT_DELAYS",
#                 "message": "Métro 6 : Bagage oublié dans un train - Reprise progressive / trafic reste perturbé, <p>Le trafic reprend mais reste perturbé sur l'ensemble de la ligne en répercussion d'un bagage oublié dans un train à Denfert-Rochereau.<br><a href='http://www.ratp.fr'>Plus d'informations sur le site ratp.fr</a></p>, Métro 6 : Bagage oublié dans un train - Reprise progressive / trafic reste perturbé",
#                 "impacted_objects": "RATP Métro 6",
#                 "line_id": "line:IDFM:C01376",
#             }
#         ]
#         self.assertEqual(expected_result, ratp_lines_status_formatter(raw_data))


# if __name__ == "__main__":
#     unittest.main()
