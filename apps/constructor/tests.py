from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from apps.constructor.models import (Application, Municipal_district, Settlement, Locality,
                                     Settlement_type, Project_type, Status, Contest, User, Section,
                                     Schema)
from apps.locations.models import Locality_type
from apps.profiles.models import Profile, Roles


class ApplicationAPITest(APITestCase):

    def setUp(self):
        # Здесь создаются необходимые объекты для тестов
        self.municipal_district = Municipal_district.objects.create(
            RegionName="Тестовый регион",
            RegionNameE="Регион",
            OKTMO="123456",
            Population=50000,
            RegOKTMO="654321",
            RegIsNorthern=True
        )
        self.settlement_type = Settlement_type.objects.create(
            title="Registration",
            abbreviation="test"
        )
        self.locality_type = Locality_type.objects.create(title="Locality Type 1")
        self.settlement = Settlement.objects.create(
            RegID=self.municipal_district,
            MunicTypeID=self.settlement_type,
            MunicName="Тестовое поселение",
            MunicNameE="Тестовое поселение",
            Population=50000,
            OKTMO="123456",
            OKATO="123456"
        )
        self.locality = Locality.objects.create(
            MunicID=self.settlement,
            RegID=self.municipal_district,
            OKTMO="123456",
            LocName="Тестовое поселение",
            LocNameE="Тестовое поселение",
            LocPopulation=50000,
            LocTypeID=self.locality_type,
            Latitude="55.75",
            Longitude="37.55"
        )
        self.section = Section.objects.create(title="Section 1")
        self.project_type = Project_type.objects.create(
            title="Project Type 1",
            section=self.section
        )
        self.status = Status.objects.create(title="Создана", section=self.section)
        self.contest = Contest.objects.create(
            title="Contest 1",
            section=self.section, status='opened',
        )
        self.contest.contest_types.add(self.settlement_type)
        self.contest.save()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.role = Roles.objects.create(title="admin", section=self.section)
        self.profile = Profile.objects.create(
            user=self.user,
            role=self.role,
            section=self.section,
            municipal_district=self.municipal_district,
            settlement=self.settlement,
            locality=self.locality,
            profile_type=self.settlement_type
        )
        self.schema = Schema.objects.create(
            title='Схема проекта',
            properties={},
            required=[],
            section=self.section,
            type='object'
        )
        self.application_data = {
            "title": "Test Project",
            "municipal_district": self.municipal_district.id,
            "settlement": self.settlement.id,
            "locality": self.locality.id,
            "project_type": self.project_type.id,
            "status": self.status.id,
            "contest": self.contest.id,
            "author": self.user.id,
            "custom_data": {"key": "value"},
            "section": self.section.id,
            "documents": []
        }
        self.application_create_data = {
            "title": "Test Project",
            "municipal_district": self.municipal_district,
            "settlement": self.settlement,
            "locality": self.locality,
            "project_type": self.project_type,
            "status": self.status,
            "contest": self.contest,
            "author": self.user,
            "custom_data": {"key": "value"},
            "section": self.section,
            "documents": []
        }

        # Аутентификация пользователя
        self.client.login(username='testuser', password='testpassword')
        self.token = self.get_jwt_token()

    def get_jwt_token(self):
        url = reverse('custom_token_get')  # Замените на ваш эндпоинт для получения токена
        response = self.client.post(url, {"username": "testuser", "password": "testpassword"}, format='json')
        return response.data['access']

    def test_create_application(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        url = reverse('application_main')
        response = self.client.post(url, self.application_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Application.objects.count(), 1)
        self.assertEqual(Application.objects.get().title, 'Test Project')

    def test_update_application(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        application = Application.objects.create(**self.application_create_data)
        url = reverse('application_detail', args=[application.id])
        updated_data = self.application_data.copy()
        updated_data["title"] = "Updated Project"
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Application.objects.get().title, 'Updated Project')

    def test_get_application_list(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        Application.objects.create(**self.application_create_data)
        url = reverse('application_main')

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(response.data["total_results"], 0)

    # def test_get_application_detail(self):
    #     application = Application.objects.create(**self.application_data)
    #     url = reverse('application-detail', args=[application.id])
    #     response = self.client.get(url, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['title'], 'Test Project')
