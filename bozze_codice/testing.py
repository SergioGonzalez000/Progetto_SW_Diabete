import unittest
from unittest.mock import Mock, PropertyMock, patch, MagicMock
import model  # Sostituisci con il tuo nome file/module
import unittest
from unittest.mock import patch, MagicMock
import model
from datetime import datetime, date
import plotly.graph_objects as go
import pandas as pd

class TestPersona(unittest.TestCase):
    def setUp(self):
        self.persona = model.Persona(
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
        self.paziente = model.Paziente(
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

    @patch("model.get_cursor")
    def test_inserisci_assunzione_farmaco(self, mock_get_cursor):
            mock_cursor = MagicMock()
            mock_get_cursor.return_value.__enter__.return_value = mock_cursor
            self.paziente.get_id_paziente = MagicMock(return_value=42)

            self.paziente.inserisci_assunzione_farmaco("Metformina", "500mg")
            mock_cursor.execute.assert_called_once()

    @patch("model.get_cursor")
    def test_inserisci_segnalazione_valida(self, mock_get_cursor):
            mock_cursor = MagicMock()
            mock_get_cursor.return_value.__enter__.return_value = mock_cursor
            self.paziente.get_id_paziente = MagicMock(return_value=42)

            self.paziente.inserisci_segnalazione("sintomo", "mal di testa", "2024-01-01")
            mock_cursor.execute.assert_called_once()



    @patch("model.get_cursor")
    def test_get_diabetologo(self, mock_get_cursor):
            mock_cursor = MagicMock()
            mock_get_cursor.return_value.__enter__.return_value = mock_cursor
            self.paziente.get_id_paziente = MagicMock(return_value=42)

            mock_cursor.fetchone.return_value = [1, "Mario", "Rossi"]
            result = self.paziente.get_diabetologo()

            self.assertEqual(result, [{"id": 1, "nome": "Mario", "cognome": "Rossi"}])


class TestDiabetologo(unittest.TestCase):
        def setUp(self):
            self.diabetologo = model.Diabetologo(
                nome="Giovanni", cognome="Verdi", data_nascita="1970-10-10", sesso="M",
                codice_fiscale="VRDGVN70R10H501Z", indirizzo="Via Firenze 5", citta="Torino", cap="10100",
                telefono="1231231234", email="giovanni.verdi@example.com", username="giovanni.verdi", pw="medico123"
            )

        @patch("model.get_cursor")
        def test_get_id_diabetologo(self, mock_get_cursor):
            mock_cursor = MagicMock()
            mock_get_cursor.return_value.__enter__.return_value = mock_cursor
            mock_cursor.fetchone.return_value = [99]

            result = self.diabetologo.get_id_diabetologo()
            self.assertEqual(result, 99)

        @patch("model.get_cursor")
        def test_inserisci_terapia(self, mock_get_cursor):
            mock_cursor = MagicMock()
            mock_get_cursor.return_value.__enter__.return_value = mock_cursor
            self.diabetologo.get_id_diabetologo = MagicMock(return_value=99)

            self.diabetologo.inserisci_terapia(
                id_paz=42,
                farmaco="Insulina",
                dose="20UI",
                assunzioni_gg=2,
                data_inizio="2024-06-01",
                data_fine="2024-07-01",
                indicazioni="Dopo i pasti"
            )

            mock_cursor.execute.assert_called_once()

        @patch("model.get_cursor")
        def test_modifica_terapia_paziente(self, mock_get_cursor):
            mock_cursor = MagicMock()
            mock_get_cursor.return_value.__enter__.return_value = mock_cursor
            self.diabetologo.get_id_diabetologo = MagicMock(return_value=99)

            self.diabetologo.modifica_terapia_paziente(
                id_paz=42,
                id_t=5,
                farmaco="Insulina",
                dose="30UI",
                assunzioni_gg=2,
                data_inizio="2024-06-01",
                data_fine="2024-07-15",
                indicazioni="Modificata dose"
            )

            mock_cursor.execute.assert_called_once()

        @patch("model.get_cursor")
        def test_visualizza_n_c_pazienti_associati(self, mock_get_cursor):
            mock_cursor = MagicMock()
            mock_get_cursor.return_value.__enter__.return_value = mock_cursor
            self.diabetologo.get_id_diabetologo = MagicMock(return_value=99)

            mock_cursor.fetchall.return_value = [
                (1, "Anna", "Rosa", 110.5),
                (2, "Marco", "Blu", 95.2),
            ]

            result = self.diabetologo.visualizza_n_c_pazienti_associati()
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0]["nome"], "Anna")

class TestAdmin(unittest.TestCase):

    @patch("model.get_cursor")
    def test_genera_username_paziente(self, mock_get_cursor):
        # Simula richiesta paziente
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (1, "Mario", "Rossi", "", "", "", "", "", "", "", "", True)
        mock_cursor.fetchall.return_value = [("1",)]
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor

        username = model.Admin.genera_username(1)
        self.assertEqual(username, "Mario.Rossi1_P")

    @patch("model.get_cursor")
    def test_genera_username_diabetologo(self, mock_get_cursor):
        # Simula richiesta diabetologo
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (1, "Luigi", "Bianchi", "", "", "", "", "", "", "", "", False)
        mock_cursor.fetchall.return_value = [("1",), ("2",)]
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor

        username = model.Admin.genera_username(1)
        self.assertEqual(username, "Luigi.Bianchi2_D")

    @patch("model.get_cursor")
    @patch("model.PersonaFactory.crea_persona")
    def test_approva_richiesta_paziente(self, mock_crea_persona, mock_get_cursor):
        # Configura il mock del cursore
        mock_cursor = MagicMock()
        
        # Configura il mock per supportare il context manager
        mock_connection = MagicMock()
        mock_connection.__enter__.return_value = mock_cursor
        mock_get_cursor.return_value = mock_connection
        
        # Configura i dati di ritorno per il test
        richiesta = (1, "Anna", "Verdi", "1990-01-01", "F", "XYZ123", "Via Roma", 
                    "Milano", "20100", "123456", "a@b.it", True, "", "", "pass")
        mock_cursor.fetchone.return_value = richiesta
        
        # Configura il mock per la creazione del paziente
        paziente_mock = MagicMock(spec=model.Paziente)
        mock_crea_persona.return_value = paziente_mock
        
        # Chiamata alla funzione da testare
        model.Admin.approva_richiesta(1)
        
        # Verifiche
        mock_cursor.execute.assert_any_call(
            "UPDATE RichiesteAccount SET stato_richiesta=%s WHERE id_richiesta = %s ",
            ('approvata', 1)
        )
    @patch("model.get_cursor")
    def test_rifiuta_richiesta(self, mock_get_cursor):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (1, "x", "x", "x")
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor

        model.Admin.rifiuta_richiesta(1)
        mock_cursor.execute.assert_called_with(
            "UPDATE RichiesteAccount SET stato_richiesta=%s WHERE id_richiesta = %s", ('rifiutata', 1))

    @patch("model.get_cursor")
    def test_rifiuta_richiesta_cf_not_found(self, mock_get_cursor):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor

        with self.assertRaises(ValueError):
            model.Admin.rifiuta_richiesta_cf("ABC123")

    @patch("model.get_cursor")
    def test_elimina_paziente(self, mock_get_cursor):
        mock_cursor = MagicMock()
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor

        model.Admin.elimina_paziente(42)
        mock_cursor.execute.assert_called_with("DELETE FROM Paziente WHERE id_paziente = %s", (42,))

    @patch("model.get_cursor")
    def test_elimina_diabetologo(self, mock_get_cursor):
        mock_cursor = MagicMock()
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor

        model.Admin.elimina_diabetologo(24)
        mock_cursor.execute.assert_called_with("DELETE FROM Diabetologo WHERE id_diabetologo = %s", (24,))

    @patch("model.get_cursor")
    def test_associa_a_diabetologo(self, mock_get_cursor):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = [3]
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor

        paziente_mock = MagicMock()
        paziente_mock.cf = "XYZ123"

        model.Admin.associa_a_diabetologo(paziente_mock)
        mock_cursor.execute.assert_called_with("UPDATE Paziente SET diabetologo_associato=%s WHERE codice_fiscale = %s ", (3, "XYZ123"))


class TestPersonaFactory(unittest.TestCase):
    @patch('model.Paziente')
    @patch('model.Diabetologo')
    @patch('model.Admin')
    def test_crea_persona(self, mock_admin, mock_diabetologo, mock_paziente):
        # Test creazione paziente
        model.PersonaFactory.crea_persona(
            "paziente", "Mario", "Rossi", "1990-01-01", "M", 
            "RSSMRA90A01H501U", "Via Roma", "Roma", "00100", 
            "1234567890", "mario@example.com", "mario.rossi", "pass"
        )
        mock_paziente.assert_called_once()
        
        # Test creazione diabetologo
        model.PersonaFactory.crea_persona(
            "diabetologo", "Luigi", "Bianchi", "1980-01-01", "M", 
            "BNCLGU80A01H501Y", "Via Milano", "Milano", "20100", 
            "0987654321", "luigi@example.com", "luigi.bianchi", "pass"
        )
        mock_diabetologo.assert_called_once()
        
        # Test creazione admin
        model.PersonaFactory.crea_persona(
            "admin", "Admin", "Admin", "1970-01-01", "M", 
            "DMNDMN70A01H501X", "Via Admin", "Admin", "00100", 
            "1231231234", "admin@example.com", "admin", "pass"
        )
        mock_admin.assert_called_once()
        
        # Test tipo non valido
        with self.assertRaises(ValueError):
            model.PersonaFactory.crea_persona(
                "invalid", "Nome", "Cognome", "2000-01-01", "M",
                "CFCFCF00A01H501Z", "Via", "Città", "00100",
                "1234567890", "email@example.com", "username", "pass"
            )


class TestUtilityFunctions(unittest.TestCase):

    @patch('model.get_cursor')
    @patch('model.generate_password_hash')
    def test_inserisci_richiesta(self, mock_hash, mock_get_cursor):
        mock_cursor = MagicMock()
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        mock_hash.return_value = "hashed_password"
        
        model.inserisci_richiesta(
            "Mario", "Rossi", "1990-01-01", "M", "RSSMRA90A01H501U",
            "Via Roma", "Roma", "00100", "1234567890", "mario@example.com",
            True, "password123"
        )
        
        # Verifica semplificata
        self.assertTrue(mock_cursor.execute.called)
        call_args = mock_cursor.execute.call_args[0][0]
        self.assertIn("INSERT INTO RichiesteAccount", call_args)

    @patch('model.get_cursor')
    @patch('model.PersonaFactory.crea_persona')
    def test_get_by_username(self, mock_crea_persona, mock_get_cursor):
        mock_cursor = MagicMock()
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        
        # Test paziente trovato
        paziente_data = ("Mario", "Rossi", "1990-01-01", "M", "RSSMRA90A01H501U",
                        "Via Roma", "Roma", "00100", "1234567890", "mario@example.com",
                        "mario.rossi", "hashed_pass")
        mock_cursor.fetchone.side_effect = [paziente_data, None, None]
        
        result = model.get_by_username("mario.rossi")
        mock_crea_persona.assert_called_once_with(
            "paziente", *paziente_data[:-1], paziente_data[-1]
        )
        
        # Test diabetologo trovato
        mock_crea_persona.reset_mock()
        mock_cursor.fetchone.side_effect = [None, paziente_data, None]
        
        result = model.get_by_username("mario.rossi")
        mock_crea_persona.assert_called_once_with(
            "diabetologo", *paziente_data[:-1], paziente_data[-1]
        )
        
        # Test admin trovato
        mock_crea_persona.reset_mock()
        mock_cursor.fetchone.side_effect = [None, None, paziente_data]
        
        result = model.get_by_username("mario.rossi")
        mock_crea_persona.assert_called_once_with(
            "admin", *paziente_data[:-1], paziente_data[-1]
        )
        
        # Test nessun utente trovato
        mock_cursor.fetchone.side_effect = [None, None, None]
        result = model.get_by_username("non.esiste")
        self.assertIsNone(result)

    @patch('model.get_cursor')
    def test_get_richieste_account_pazienti(self, mock_get_cursor):
        mock_cursor = MagicMock()
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            (1, "Mario", "Rossi", "RSSMRA90A01H501U"),
            (2, "Luigi", "Bianchi", "BNCLGU80A01H501Y")
        ]
        
        result = model.get_richieste_account_pazienti()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["label"], "Mario Rossi RSSMRA90A01H501U")
        self.assertEqual(result[0]["value"], 1)
        
        mock_cursor.execute.assert_called_once_with(
            "SELECT id_richiesta, nome, cognome, codice_fiscale FROM richiesteaccount WHERE stato_richiesta = %s AND paziente = %s",
            ("in_attesa", "TRUE")
        )

    @patch('model.get_cursor')
    def test_get_richieste_account_diabetologi(self, mock_get_cursor):
        mock_cursor = MagicMock()
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            (1, "Giovanni", "Verdi", "VRDGVN70R10H501Z"),
            (2, "Anna", "Neri", "NRENNA80M41H501X")
        ]
        
        result = model.get_richieste_account_diabetologi()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["label"], "Giovanni Verdi VRDGVN70R10H501Z")
        self.assertEqual(result[0]["value"], 1)
        
        mock_cursor.execute.assert_called_once_with(
            "SELECT id_richiesta, nome, cognome, codice_fiscale FROM richiesteaccount WHERE stato_richiesta = %s AND paziente = %s",
            ("in_attesa", "FALSE")
        )



class TestDatabaseFunctions(unittest.TestCase):

    @patch('model.get_cursor')
    def test_get_dati_richiesta_account_by_id(self, mock_get_cursor):
        # Configura il mock
        mock_cursor = MagicMock()
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        
        # Dati di test
        test_data = (
            "Mario", "Rossi", date(1990, 1, 1), "M", "RSSMRA90A01H501U",
            "Via Roma 1", "Roma", "00100", "1234567890", "mario@example.com",
            True, date(2023, 1, 1), "approvata"
        )
        mock_cursor.fetchone.return_value = test_data
        
        # Chiamata alla funzione
        result = model.get_dati_richiesta_account_by_id(1)
        
        # Verifiche
        self.assertIsNotNone(result)
        self.assertEqual(result["nome"], "Mario")
        self.assertEqual(result["cognome"], "Rossi")
        self.assertEqual(result["stato_richiesta"], "approvata")
        mock_cursor.execute.assert_called_once()

    @patch('model.get_cursor')
    def test_get_dettagli_paziente(self, mock_get_cursor):
        mock_cursor = MagicMock()
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        
        test_data = (
            1, "Luca", "Bianchi", date(1985, 5, 20), "M", "BNCLCU85E20H501Y",
            "Via Milano 10", "Milano", "20100", "0987654321", "luca@example.com",
            "luca.bianchi", 3
        )
        mock_cursor.fetchone.return_value = test_data
        
        result = model.get_dettagli_paziente(1)
        
        self.assertIsNotNone(result)
        self.assertEqual(result["id_paziente"], 1)
        self.assertEqual(result["diabetologo_associato"], 3)
        mock_cursor.execute.assert_called_once()

    @patch('model.get_cursor')
    def test_get_all_pazienti(self, mock_get_cursor):
        mock_cursor = MagicMock()
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        
        test_data = [
            (1, "Mario", "Rossi", "RSSMRA90A01H501U", date(1990, 1, 1), "mario@example.com", "1234567890"),
            (2, "Luigi", "Verdi", "VRDLGU80A01H501Y", date(1980, 1, 1), "luigi@example.com", "0987654321")
        ]
        mock_cursor.fetchall.return_value = test_data
        
        result = model.get_all_pazienti()
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["nome"], "Mario")
        self.assertEqual(result[1]["email"], "luigi@example.com")
        mock_cursor.execute.assert_called_once()

    @patch('model.get_cursor')
    def test_get_dettagli_diabetologo(self, mock_get_cursor):
        mock_cursor = MagicMock()
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        
        test_data = (
            1, "Giovanni", "Neri", date(1975, 6, 15), "M", "NRIGNN75H15H501Z",
            "Via Torino 5", "Torino", "10100", "1231231234", "giovanni@example.com", "giovanni.neri"
        )
        mock_cursor.fetchone.return_value = test_data
        
        result = model.get_dettagli_diabetologo(1)
        
        self.assertIsNotNone(result)
        self.assertEqual(result["id_diabetologo"], 1)
        self.assertEqual(result["username"], "giovanni.neri")
        mock_cursor.execute.assert_called_once()

    @patch('model.get_cursor')
    def test_get_all_diabetologi(self, mock_get_cursor):
        mock_cursor = MagicMock()
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        
        test_data = [
            (1, "Anna", "Rossi", "RSSNNA70A01H501X", date(1970, 1, 1), "anna@example.com", "1234567890"),
            (2, "Paolo", "Bianchi", "BNCPLA80A01H501Y", date(1980, 1, 1), "paolo@example.com", "0987654321")
        ]
        mock_cursor.fetchall.return_value = test_data
        
        result = model.get_all_diabetologi()
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["nome"], "Anna")
        self.assertEqual(result[1]["codice_fiscale"], "BNCPLA80A01H501Y")
        mock_cursor.execute.assert_called_once()

    @patch('model.get_cursor')
    @patch('model.get_all_diabetologi')
    @patch('model.Diabetologo')
    def test_visualizza_media_glicemia_per_diabetologi(self, mock_diabetologo, mock_get_all_diabetologi, mock_get_cursor):
        # Configura i mock
        mock_cursor = MagicMock()
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        
        # Mock per get_all_diabetologi
        mock_get_all_diabetologi.return_value = [
            {"id_diabetologo": 1, "nome": "Giovanni", "cognome": "Neri"},
            {"id_diabetologo": 2, "nome": "Anna", "cognome": "Rossi"}
        ]
        
        # Mock per Diabetologo e visualizza_n_c_pazienti_associati
        mock_diab1 = MagicMock()
        mock_diab1.visualizza_n_c_pazienti_associati.return_value = [
            {"nome": "Paziente1", "media": 120},
            {"nome": "Paziente2", "media": 130}
        ]
        
        mock_diab2 = MagicMock()
        mock_diab2.visualizza_n_c_pazienti_associati.return_value = [
            {"nome": "Paziente3", "media": 110},
            {"nome": "Paziente4", "media": 140}
        ]
        
        mock_diabetologo.side_effect = [mock_diab1, mock_diab2]
        
        # Chiamata alla funzione
        fig = model.visualizza_media_glicemia_per_diabetologi()
        
        # Verifiche di base
        self.assertIsNotNone(fig)
        self.assertEqual(mock_diabetologo.call_count, 2)
        
        # Verifica che la figura abbia i dati corretti (test semplificato)
        self.assertEqual(fig.data[0].x[0], "Giovanni Neri")
        self.assertEqual(fig.data[0].x[1], "Anna Rossi")
        
    @patch('model.get_cursor')
    @patch('model.get_all_diabetologi')
    def test_visualizza_media_glicemia_senza_dati(self, mock_get_all_diabetologi, mock_get_cursor):
        # Configura mock senza dati
        mock_get_all_diabetologi.return_value = []
        
        # Chiamata alla funzione
        fig = model.visualizza_media_glicemia_per_diabetologi()
        
        # Verifica che la figura mostri il messaggio di nessun dato
        self.assertIsNotNone(fig)
        self.assertEqual(fig.layout.annotations[0].text, "Nessun dato disponibile")



class TestAdditionalFunctions(unittest.TestCase):

    @patch('model.get_cursor')
    @patch('model.Diabetologo')
    def test_visualizza_media_glicemia_pazienti_diabetologo(self, mock_diabetologo, mock_get_cursor):
        # Configura mock del database
        mock_cursor = MagicMock()
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (
            1, "Giovanni", "Neri", "1970-01-01", "M", "NRIGNN70A01H501Z",
            "Via Roma", "Roma", "00100", "1234567890", "giovanni@example.com", 
            "giovanni.neri", "password123"
        )
        
        # Configura mock Diabetologo
        mock_diab = MagicMock()
        mock_diab.visualizza_n_c_pazienti_associati.return_value = [
            {"nome": "Mario", "cognome": "Rossi", "media": 120.5},
            {"nome": "Luigi", "cognome": "Bianchi", "media": 135.2}
        ]
        mock_diabetologo.return_value = mock_diab
        
        # Chiamata alla funzione
        fig = model.visualizza_media_glicemia_pazienti_diabetologo(1)
        
        # Verifiche
        self.assertIsInstance(fig, go.Figure)
        self.assertEqual(len(fig.data[0].x), 2)
        self.assertEqual(fig.data[0].y[0], 120.5)
        mock_cursor.execute.assert_called_once()

    @patch('model.get_cursor')
    def test_visualizza_pazienti_associati_singolo_diab(self, mock_get_cursor):
        mock_cursor = MagicMock()
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            ("Mario", "Rossi", "mario.rossi"),
            ("Luigi", "Bianchi", "luigi.bianchi")
        ]
        
        result = model.visualizza_pazienti_associati_singolo_diab(1)
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["cognome"], "Rossi")
        self.assertEqual(result[1]["username"], "luigi.bianchi")
        mock_cursor.execute.assert_called_once()

    @patch('model.get_cursor')
    def test_get_id_paziente_by_username(self, mock_get_cursor):
        mock_cursor = MagicMock()
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (42,)
        
        result = model.get_id_paziente_by_username("mario.rossi")
        self.assertEqual(result, 42)
        mock_cursor.execute.assert_called_once()

    @patch('model.get_cursor')
    def test_get_dati_glicemia_filtrati(self, mock_get_cursor):
        mock_cursor = MagicMock()
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        test_data = [
            (120, datetime(2023, 1, 1), "Nessuno"),
            (135, datetime(2023, 1, 2), "Affaticamento")
        ]
        mock_cursor.fetchall.return_value = test_data
        
        # Test filtro andamento giornaliero
        result = model.get_dati_glicemia_filtrati(1, "giornaliero", "andamento")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][0], 120)
        
        # Test filtro media mensile
        mock_cursor.fetchall.return_value = [(0, 125.5), (3, 130.2)]
        result = model.get_dati_glicemia_filtrati(1, "mensile", "media")
        self.assertEqual(len(result), 2)

    @patch('model.get_cursor')
    def test_get_terapie_paziente(self, mock_get_cursor):
        mock_cursor = MagicMock()
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        test_data = [
            (1, 1, "Insulina", "20UI", 2, "2023-01-01", "2023-07-01", "Dopo i pasti"),
            (2, 1, "Metformina", "500mg", 1, "2023-01-01", None, "Mattina")
        ]
        mock_cursor.fetchall.return_value = test_data
        
        result = model.get_terapie_paziente(1, 1)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][2], "Insulina")

    def test_visualizza_andamento_glicemia(self):
        test_data = [
            (120, datetime(2023, 1, 1), "Nessuno"),
            (135, datetime(2023, 1, 2), "Affaticamento"),
            (110, datetime(2023, 1, 3), None)
        ]
        
        fig = model.visualizza_andamento_glicemia(test_data)
        
        self.assertIsInstance(fig, go.Figure)
        self.assertEqual(len(fig.data), 3)  # Linea + soglia minima + soglia massima
        self.assertEqual(fig.data[0].y[0], 120)
        
        # Test con dati vuoti
        with self.assertRaises(ValueError):
            model.visualizza_andamento_glicemia([])

    def test_visualizza_media_glicemica_fasce_orarie(self):
        test_data = [
            (0, 125.5),
            (3, 130.2),
            (6, 110.8),
            (9, 140.1)
        ]
        
        fig = model.visualizza_media_glicemica_fasce_orarie(test_data)
        
        self.assertIsInstance(fig, go.Figure)
        self.assertEqual(len(fig.data[0].x), 8)  # 8 fasce orarie
        self.assertEqual(fig.data[0].y[0], 125.5)
        
        # Test con dati vuoti
        with self.assertRaises(ValueError):
            model.visualizza_media_glicemica_fasce_orarie([])

    @patch('model.get_cursor')
    def test_get_eventi_basso_glucosio(self, mock_get_cursor):
        mock_cursor = MagicMock()
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        test_data = [
            (55, datetime(2023, 1, 1)),
            (58, datetime(2023, 1, 15))
        ]
        mock_cursor.fetchall.return_value = test_data
        
        result = model.get_eventi_basso_glucosio(1)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][0], 55)
        mock_cursor.execute.assert_called_once()



class TestRemainingFunctions(unittest.TestCase):

    @patch('model.get_cursor')
    def test_get_info_base_paziente(self, mock_get_cursor):
        mock_cursor = MagicMock()
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        test_data = ("mario.rossi", "Mario", "Rossi", date(1990,1,1), "M", 125.5)
        mock_cursor.fetchone.return_value = test_data
        
        result = model.get_info_base_paziente(1, 1)
        self.assertEqual(result, test_data)
        mock_cursor.execute.assert_called_once()

    @patch('model.get_cursor')
    def test_get_info_base_diabetologo(self, mock_get_cursor):
        mock_cursor = MagicMock()
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        test_data = [("giovanni.neri", "Giovanni", "Neri", date(1975,6,15), "M", 5)]
        mock_cursor.fetchall.return_value = test_data
        
        result = model.get_info_base_diabetologo(1)
        self.assertEqual(result, test_data)
        mock_cursor.execute.assert_called_once()

    @patch('model.get_cursor')
    def test_get_messaggi(self, mock_get_cursor):
        mock_cursor = MagicMock()
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        test_data = [
            ("Ciao come stai?", datetime(2023,5,15,10,30), True, 1),
            ("Tutto bene, grazie!", datetime(2023,5,15,10,35), False, 1)
        ]
        mock_cursor.fetchall.return_value = test_data
        
        result = model.get_messaggi(1, 2)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].contenuto, "Ciao come stai?")
        self.assertEqual(result[1].user_is_diabetologo, True)# mittente=diabetologo
        mock_cursor.execute.assert_called_once()

    @patch('model.get_cursor')
    def test_insert_messaggio(self, mock_get_cursor):
        mock_cursor = MagicMock()
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        
        # Test con diabetologo come mittente
        model.insert_messaggio(1, 2, "Ciao paziente")
        mock_cursor.execute.assert_called_with(
            "Insert into messaggio values (%s,%s,%s,current_timestamp,%s)",
            (1, 2, "Ciao paziente", True) #si aspetta che il mittente sia un diabetologo
        )
        
        # Test con paziente come mittente
        mock_cursor.reset_mock()
        mock_cursor.fetchone.return_value = None  # Simula che l'utente non è diabetologo
        model.insert_messaggio(2, 1, "Ciao dottore")
        mock_cursor.execute.assert_called_with(
            "Insert into messaggio values (%s,%s,%s,current_timestamp,%s)",
            (1, 2, "Ciao dottore", False)
        )

    @patch('model.get_cursor')
    def test_get_nomecognome(self, mock_get_cursor):
        mock_cursor = MagicMock()
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        test_data = ("Mario", "Rossi")
        mock_cursor.fetchone.return_value = test_data
        
        result = model.get_nomecognome(1)
        self.assertEqual(result.nome, "Mario")
        self.assertEqual(result.cognome, "Rossi")
        mock_cursor.execute.assert_called_once()

    @patch('model.get_cursor')
    def test_modifica_dati_paziente_db(self, mock_get_cursor):
        mock_cursor = MagicMock()
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        
        # Test con alcuni campi
        model.modifica_dati_paziente_db(
            1, nome="Mario", cognome="Rossi", indirizzo="Via Roma 1"
        )
        
        # Verifica che la query sia corretta
        self.assertIn("nome = %s", mock_cursor.execute.call_args[0][0])
        self.assertIn("cognome = %s", mock_cursor.execute.call_args[0][0])
        self.assertIn("indirizzo = %s", mock_cursor.execute.call_args[0][0])
        self.assertEqual(mock_cursor.execute.call_args[0][1][-1], 1)  # ID paziente
        
        # Test senza campi da aggiornare
        with self.assertRaises(ValueError):
            model.modifica_dati_paziente_db(1)

    @patch('model.get_cursor')
    def test_modifica_dati_diabetologo_db(self, mock_get_cursor):
        mock_cursor = MagicMock()
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        
        # Test con alcuni campi
        model.modifica_dati_diabetologo_db(
            1, nome="Giovanni", email="giovanni@example.com", telefono="1234567890"
        )
        
        # Verifica che la query sia corretta
        self.assertIn("nome = %s", mock_cursor.execute.call_args[0][0])
        self.assertIn("email = %s", mock_cursor.execute.call_args[0][0])
        self.assertIn("telefono = %s", mock_cursor.execute.call_args[0][0])
        self.assertEqual(mock_cursor.execute.call_args[0][1][-1], 1)  # ID diabetologo
        
        # Test senza campi da aggiornare
        with self.assertRaises(ValueError):
            model.modifica_dati_diabetologo_db(1)

    def test_is_number(self):
        self.assertTrue(model.is_number("123"))
        self.assertTrue(model.is_number("123.45"))
        self.assertTrue(model.is_number(123))
        self.assertTrue(model.is_number(123.45))
        self.assertFalse(model.is_number("abc"))
        self.assertFalse(model.is_number(None))

    @patch('model.get_cursor')
    def test_get_numero_pazienti_associati_by_id(self, mock_get_cursor):
        mock_cursor = MagicMock()
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (5,)
        
        result = model.get_numero_pazienti_associati_by_id(1)
        self.assertEqual(result, 5)
        mock_cursor.execute.assert_called_once()

if __name__ == '__main__':
    unittest.main()
