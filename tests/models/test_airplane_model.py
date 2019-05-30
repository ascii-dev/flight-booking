from api.models.airplane import Airplane


class TestAirplaneModel:
    def test_new_airplane_succeeds(self, init_db, new_airplane):
        """
        Test that airplane can be created successfully through the
        model
        :param init_db: initialize the database
        :param new_airplane: creates new airplane through the model
        :return: assertion
        """
        assert new_airplane == new_airplane.save()

    def test_get_a_single_airplane_succeeds(self, init_db, new_airplane):
        """
        Tests that getting a single airplane from the database
        through the model is successful
        :param init_db: initialize the database
        :param new_airplane: creates new airplane through the model
        :return: assertion
        """
        new_airplane.save()
        assert Airplane.query.get(new_airplane.id) == new_airplane

    def test_update_a_airplane_succeeds(self, init_db, new_airplane):
        """
        Tests that updating a airplane from the database through
        the model is successful
        :param init_db: initialize the database
        :param new_airplane: creates a new airplane through the model
        :return: assertion
        """
        new_airplane.save()
        new_airplane.update(capacity=321)
        assert new_airplane.capacity == 321

    def test_delete_a_airplane_succeeds(self, init_db, new_airplane):
        """
        Tests that deleting a airplane from the database through the
        model is successful
        :param init_db: initialize the database
        :param new_airplane: creates a new airplane through the model
        :return: None
        """
        new_airplane.save()
        new_airplane.delete()

    def test_get_airplane_string_representation(self, new_airplane):
        """
        Tests to compute and assert string representation of
        a new airplane
        :param new_airplane: creates a new airplane through the model
        :return: assertion
        """
        brand = new_airplane.brand
        model = new_airplane.model
        capacity = new_airplane.capacity
        assert repr(new_airplane) == \
            f'<Airplane {brand} {model} {capacity}>'
