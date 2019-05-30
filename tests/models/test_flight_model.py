from api.models.flight import Flight


class TestFlightModel:
    def test_new_flight_succeeds(self, init_db, new_flight):
        """
        Test that flight can be created successfully through the
        model
        :param init_db: initialize the database
        :param new_flight: creates new flight through the model
        :return: assertion
        """
        assert new_flight == new_flight.save()

    def test_get_a_single_flight_succeeds(self, init_db, new_flight):
        """
        Tests that getting a single flight from the database
        through the model is successful
        :param init_db: initialize the database
        :param new_flight: creates new flight through the model
        :return: assertion
        """
        new_flight.save()
        assert Flight.query.get(new_flight.id) == new_flight

    def test_update_a_flight_succeeds(self, init_db, new_flight):
        """
        Tests that updating a flight from the database through
        the model is successful
        :param init_db: initialize the database
        :param new_flight: creates a new flight through the model
        :return: assertion
        """
        new_flight.save()
        new_flight.update(flying_from='Lagos')
        assert new_flight.flying_from == 'Lagos'

    def test_delete_a_flight_succeeds(self, init_db, new_flight):
        """
        Tests that deleting a flight from the database through the
        model is successful
        :param init_db: initialize the database
        :param new_flight: creates a new flight through the model
        :return: None
        """
        new_flight.save()
        new_flight.delete()

    def test_get_flight_string_representation(self, new_flight):
        """
        Tests to compute and assert string representation of
        a new flight
        :param new_flight: creates a new flight through the model
        :return: assertion
        """
        flying_from = new_flight.flying_from
        flying_to = new_flight.flying_to
        date = new_flight.date
        assert repr(new_flight) == \
            f'<Flight {flying_from} - {flying_to} ({date})>'
