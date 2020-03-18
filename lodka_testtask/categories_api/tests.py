from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from .models import Category


# Create your tests here.

class CategoriesViewSetTestCase(APITestCase):
    def setUp(self) -> None:
        self.valid_input = {
            "name": "Category 1",
            "children": [
                {
                    "name": "Category 1.1",
                    "children": [
                        {
                            "name": "Category 1.1.1",
                            "children": [
                                {
                                    "name": "Category 1.1.1.1"
                                },
                                {
                                    "name": "Category 1.1.1.2"
                                },
                                {
                                    "name": "Category 1.1.1.3"
                                }
                            ]
                        },
                        {
                            "name": "Category 1.1.2",
                            "children": [
                                {
                                    "name": "Category 1.1.2.1"
                                },
                                {
                                    "name": "Category 1.1.2.2"
                                },
                                {
                                    "name": "Category 1.1.2.3"
                                }
                            ]
                        }
                    ]
                },
                {
                    "name": "Category 1.2",
                    "children": [
                        {
                            "name": "Category 1.2.1"
                        },
                        {
                            "name": "Category 1.2.2",
                            "children": [
                                {
                                    "name": "Category 1.2.2.1"
                                },
                                {
                                    "name": "Category 1.2.2.2"
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        self.broken_input_data = {
            "name": "Category 1",
            "children": [
                {
                    "name": "Category 1.1",
                    "children": [
                        {
                            "name": "Category 1.1.1",
                            "children": [
                                {
                                    "name": ""
                                },
                                {
                                    "name": "Category 1.1.1.2"
                                },
                                {
                                    "name": "Category 1.1.1.3"
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        self.db_output = [
            {"id": 1, "name": "Category 1", "parent_id": None},
            {"id": 2, "name": "Category 1.1", "parent_id": 1},
            {"id": 3, "name": "Category 1.1.1", "parent_id": 2},
            {"id": 4, "name": "Category 1.1.1.1", "parent_id": 3},
            {"id": 5, "name": "Category 1.1.1.2", "parent_id": 3},
            {"id": 6, "name": "Category 1.1.1.3", "parent_id": 3},
            {"id": 7, "name": "Category 1.1.2", "parent_id": 2},
            {"id": 8, "name": "Category 1.1.2.1", "parent_id": 7},
            {"id": 9, "name": "Category 1.1.2.2", "parent_id": 7},
            {"id": 10, "name": "Category 1.1.2.3", "parent_id": 7},
            {"id": 11, "name": "Category 1.2", "parent_id": 1},
            {"id": 12, "name": "Category 1.2.1", "parent_id": 11},
            {"id": 13, "name": "Category 1.2.2", "parent_id": 11},
            {"id": 14, "name": "Category 1.2.2.1", "parent_id": 13},
            {"id": 15, "name": "Category 1.2.2.2", "parent_id": 13},
        ]

        self.get_data_1 = {
            "id": 2,
            "name": "Category 1.1",
            "parents": [
                {
                    "id": 1,
                    "name": "Category 1"
                }
            ],
            "children": [
                {
                    "id": 3,
                    "name": "Category 1.1.1"
                },
                {
                    "id": 7,
                    "name": "Category 1.1.2"
                }
            ],
            "siblings": [
                {
                    "id": 11,
                    "name": "Category 1.2"
                }
            ]
        }

        self.get_data_2 = {
            "id": 8,
            "name": "Category 1.1.2.1",
            "parents": [
                {
                    "id": 7,
                    "name": "Category 1.1.2"
                },
                {
                    "id": 2,
                    "name": "Category 1.1"
                },
                {
                    "id": 1,
                    "name": "Category 1"
                }
            ],
            "children": [],
            "siblings": [
                {
                    "id": 9,
                    "name": "Category 1.1.2.2"
                },
                {
                    "id": 10,
                    "name": "Category 1.1.2.3"
                }
            ]
        }

        self.nested_obj_error = {
            "non_field_errors": [
                "validation error in nested object"
            ]
        }

    def test_not_allowed_method(self):
        response = self.client.get(reverse('categories-list'), self.valid_input)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.patch(reverse('categories-list'), self.valid_input)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.delete(reverse('categories-list'), self.valid_input)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.put(reverse('categories-list'), self.valid_input)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_add_categories(self):
        response = self.client.post(reverse('categories-list'), data=self.valid_input, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        querysets = Category.objects.all()
        expectation_reality = zip(querysets, self.db_output)
        for er in expectation_reality:
            self.assertEqual(er[0].id, er[1]['id'])
            self.assertEqual(er[0].name, er[1]['name'])
            self.assertEqual(er[0].parent_id, er[1]['parent_id'])

    def test_output_categories(self):
        response = self.client.post(reverse('categories-list'), data=self.valid_input, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(reverse('categories-detail', args=[2]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.get_data_1)
        response = self.client.get(reverse('categories-detail', args=[8]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.get_data_2)

    def test_nested_field_validation(self):
        response = self.client.post(reverse('categories-list'), data=self.broken_input_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, self.nested_obj_error)
        querysets = Category.objects.all()
        self.assertTrue(not querysets)

