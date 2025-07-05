import unittest
from unittest.mock import patch, MagicMock
from model import Persona, Paziente  # Sostituisci con il tuo nome file/module

class TestPersona(unittest.TestCase):
    def setUp(self):
        self.persona = Persona(
            nome="Mario", cognome="Rossi", data_nascita="1990-01-01", sesso="M",
            codice_fiscale="RSSMRA90A01H501U", indirizzo="Via Roma 1", citta="Roma", cap="00100",
            telefono="1234567890", email="mario.rossi@example.com", username="mario.rossi", password="password123"
        )

    def test_getters_setters(self):
        self.assertEqual(self.persona.nome, "Mario")
        self.persona.nome = "Luigi"
        self.assertEqual(self.persona.nome, "Luigi")

        self.assertEqual(self.persona.get_id(), "mario.rossi")

class TestPaziente(unittest.TestCase):
    def setUp(self):
        self.paziente = Paziente(
            nome="Luca", cognome="Bianchi", data_nascita="1985-05-20", sesso="M",
            codice_fiscale="BNCLCU85E20H501Y", indirizzo="Via Milano 10", citta="Milano", cap="20100",
            telefono="0987654321", email="luca.bianchi@example.com", username="luca.bianchi", pw="securepass"
        )

    @patch("model.get_cursor")
    def test_get_id_paziente(self, mock_get_cursor):
        mock_cursor = MagicMock()
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = [42]

        result = self.paziente.get_id_paziente()
        self.assertEqual(result, 42)
        mock_cursor.execute.assert_called_once_with(
            "SELECT id_paziente FROM Paziente WHERE codice_fiscale = %s",
            (self.paziente.cf,)
        )

    @patch("model.get_cursor")
    def test_inserisci_glicemia(self, mock_get_cursor):
        mock_cursor = MagicMock()
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        self.paziente.get_id_paziente = MagicMock(return_value=42)

        self.paziente.inserisci_glicemia(120, True, "nausea")
        mock_cursor.execute.assert_called_once()

if __name__ == '__main__':
    unittest.main()
