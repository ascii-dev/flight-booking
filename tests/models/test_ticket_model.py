from api.models.ticket import Ticket


class TestTicketModel:
    def test_new_ticket_succeeds(self, init_db, new_ticket):
        """
        Test that ticket can be created successfully through the
        model
        :param init_db: initialize the database
        :param new_ticket: creates new ticket through the model
        :return: assertion
        """
        assert new_ticket == new_ticket.save()

    def test_get_a_single_ticket_succeeds(self, init_db, new_ticket):
        """
        Tests that getting a single ticket from the database
        through the model is successful
        :param init_db: initialize the database
        :param new_ticket: creates new ticket through the model
        :return: assertion
        """
        new_ticket.save()
        assert Ticket.query.get(new_ticket.id) == new_ticket

    def test_update_a_ticket_succeeds(self, init_db, new_ticket):
        """
        Tests that updating a ticket from the database through
        the model is successful
        :param init_db: initialize the database
        :param new_ticket: creates a new ticket through the model
        :return: assertion
        """
        new_ticket.save()
        new_ticket.update(status='paid')
        assert new_ticket.status.value == 'paid'

    def test_delete_a_ticket_succeeds(self, init_db, new_ticket):
        """
        Tests that deleting a ticket from the database through the
        model is successful
        :param init_db: initialize the database
        :param new_ticket: creates a new ticket through the model
        :return: None
        """
        new_ticket.save()
        new_ticket.delete()

    def test_get_ticket_string_representation(self, new_ticket):
        """
        Tests to compute and assert string representation of
        a new flight
        :param new_ticket: creates a new ticket through the model
        :return: assertion
        """
        status = new_ticket.status
        assert repr(new_ticket) == \
            f'<Ticket {status}>'
