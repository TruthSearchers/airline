from django.db.models import Max
from django.test import Client,TestCase
from .models import Airport,Flights,Passenger
# Create your tests here.

class FlightTestCase(TestCase):
        def setUp(self):
            a1=Airport.objects.create(code="AAA",city="City A")
            a2=Airport.objects.create(code="BBB",city="City B")

            Flights.objects.create(origin=a1,destination=a2,duration=100)
            Flights.objects.create(origin=a1,destination=a1,duration=200)
            Flights.objects.create(origin=a1,destination=a2,duration=-100)

        def test_departure_count(self):
            a=Airport.objects.get(code="AAA")
            self.assertEqual(a.departure.count(),3)

        def test_arrival_count(self):
            a=Airport.objects.get(code="AAA")
            self.assertEqual(a.arrival.count(),1)

        def test_valid_flight(self):
            a1=Airport.objects.get(code='AAA')
            a2=Airport.objects.get(code='BBB')
            f=Flights.objects.get(origin=a1,destination=a2,duration=100)
            self.assertTrue(f.is_valid_flight())
        
        def test_invalid_flight_destination(self):
            a1=Airport.objects.get(code='AAA')
            f=Flights.objects.get(origin=a1,destination=a1)
            self.assertFalse(f.is_valid_flight())

        def test_invalid_flight_duration(self):
            a1=Airport.objects.get(code="AAA")
            a2=Airport.objects.get(code="BBB")
            f=Flights.objects.get(origin=a1,destination=a2,duration=-100)
            self.assertFalse(f.is_valid_flight())

        def test_index(self):
            c=Client()
            response=c.get('/flights/')
            self.assertEqual(response.status_code,200)
            self.assertEqual(response.context["flights"].count(),3)
        
        def test_valid_flight_page(self):
            a1=Airport.objects.get(code="AAA")
            f=Flights.objects.get(origin=a1,destination=a1)

            c=Client()
            response=c.get(f'/flights/{f.id}')
            self.assertEqual(response.status_code,200)

        def test_invalid_flight_page(self):
            non_existent_id = -1
            c = Client()
            response = c.get(f"/flights/{non_existent_id}")
            self.assertEqual(response.status_code, 404)


        def test_flight_page_passengers(self):
            f=Flights.objects.get(pk=1)
            p=Passenger.objects.create(first="Sahil",last="Singhavi")
            f.passengers.add(p)

            c=Client()
            response=c.get(f"/flights/{f.id}")
            self.assertEqual(response.status_code,200)
            self.assertEqual(response.context['pasengers'].count(),1)
        
        def test_flight_page_non_passengers(self):
            f=Flights.objects.get(pk=1)
            p=Passenger.objects.create(first="Sahil",last="Singhavi")
            c=Client()
            response=c.get(f'/flights/{f.id}')
            self.assertEqual(response.status_code,200)
            self.assertEqual(response.context['non_passengers'].count(),1)

