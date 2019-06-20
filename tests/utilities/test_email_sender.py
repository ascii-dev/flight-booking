from unittest.mock import patch

from api.utilities.email import FlaskMailSender


@patch("api.utilities.email.Mail.send")
class TestFlaskMailSenderClass:
    """Tests for sending mail with FlaskMail"""
    def test_send_email_succeeds(self, mock_send_mail):
        """Tests that email can be sent successfully"""
        mock_send_mail.return_value = True

        response = FlaskMailSender.send_mail(
            recipients=['sammysgame.dev@gmail.com'],
            subject='test subject',
            body='<div style="color:red"><b>test body</b></div>')
        assert response is True
