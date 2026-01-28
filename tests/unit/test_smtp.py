from smtp.smtp import SMTPClient


def test_smtp_send_returns_false():
    client = SMTPClient()
    result = client.send("Test Subject", "Test Text", "test@example.com")
    assert result == False
