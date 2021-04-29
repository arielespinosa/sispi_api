
from django.test import TestCase
from sispi.models.meta import Municipality
from sispi.models.outputs import Domain


class DomainPointsOnMunicipalityTestCase(TestCase):

    def test_domain(self):
        d = Domain.objects.get(resolution=3)
        print(d)

        self.assertEqual(d.slug_name, '27km')
