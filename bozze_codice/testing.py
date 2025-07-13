import re
import unittest
from unittest.mock import ANY, patch, MagicMock
from datetime import datetime
import model
from collections import namedtuple
import pandas as pd

class TestDBSingleton(unittest.TestCase):
    
    @patch('psycopg2.connect')
    def test_get_cursor_new_connection(self, mock_connect):
        # Simula una connessione chiusa
        model.DBSingleton._connection = None
        
        # Configura il mock
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Test
        with model.DBSingleton.get_cursor() as cursor:
            self.assertEqual(cursor, mock_cursor)
        
        # Verifiche
        mock_connect.assert_called_once()
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()

    @patch('psycopg2.connect')
    def test_get_cursor_existing_connection(self, mock_connect):
        # Simula una connessione esistente
        mock_conn = MagicMock()
        mock_conn.closed = False
        model.DBSingleton._connection = mock_conn
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        
        # Test
        with model.DBSingleton.get_cursor() as cursor:
            self.assertEqual(cursor, mock_cursor)
        
        # Verifiche
        mock_connect.assert_not_called()
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()

    def test_close_connection(self):
        # Simula una connessione esistente
        mock_conn = MagicMock()
        model.DBSingleton._connection = mock_conn
        
        # Test
        model.DBSingleton.close_connection()
        
        # Verifiche
        mock_conn.close.assert_called_once()
        self.assertIsNone(model.DBSingleton._connection)


class TestPersona(unittest.TestCase):
    
    def setUp(self):
        self.persona = model.Persona(
            nome="Mario",
            cognome="Rossi",
            data_nascita="1980-01-01",
            sesso="M",
            codice_fiscale="RSSMRA80A01H501R",
            indirizzo="Via Roma 1",
            citta="Roma",
            cap="00100",
            telefono="1234567890",
            email="mario.rossi@example.com",
            username="mrossi",
            password="password123"
        )
    
    def test_properties(self):
        # Test nome
        self.assertEqual(self.persona.nome, "Mario")
        self.persona.nome = "Luigi"
        self.assertEqual(self.persona.nome, "Luigi")
        
        # Test cognome
        self.assertEqual(self.persona.cognome, "Rossi")
        
        # Test codice fiscale
        self.assertEqual(self.persona.cf, "RSSMRA80A01H501R")
        
        # Test username e get_id (per Flask-Login)
        self.assertEqual(self.persona.username, "mrossi")
        self.assertEqual(self.persona.get_id(), "mrossi")


class TestPaziente(unittest.TestCase):
    
    def setUp(self):
        self.paziente = model.Paziente(
            nome="Mario",
            cognome="Rossi",
            data_nascita="1980-01-01",
            sesso="M",
            codice_fiscale="RSSMRA80A01H501R",
            indirizzo="Via Roma 1",
            citta="Roma",
            cap="00100",
            telefono="1234567890",
            email="mario.rossi@example.com",
            username="mrossi",
            pw="password123"
        )
    
    @patch('model.DBSingleton.get_cursor')
    def test_get_id_paziente(self, mock_get_cursor):
        # Configura il mock
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (123,)
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        
        # Test
        result = self.paziente.get_id_paziente()
        self.assertEqual(result, 123)
        
        # Verifica query
        mock_cursor.execute.assert_called_once_with(
            "SELECT id_paziente FROM Paziente WHERE codice_fiscale = %s",
            ("RSSMRA80A01H501R",)
        )
    
    @patch('model.DBSingleton.get_cursor')
    def test_inserisci_glicemia(self, mock_get_cursor):
        # Configura il mock
        mock_cursor = MagicMock()
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        
        # Mock get_id_paziente per evitare chiamate al DB
        with patch.object(self.paziente, 'get_id_paziente', return_value=123):
            # Test
            self.paziente.inserisci_glicemia(120, True, "Nessuno")
            
            # Verifica query
            mock_cursor.execute.assert_called_once_with(
                """INSERT INTO Glicemia 
                        (paziente, pasto, sintomi, valore) 
                        VALUES (%s, %s, %s, %s)""",
                        (123, True, "Nessuno", 120)
            )
    
    @patch('model.DBSingleton.get_cursor')
    def test_get_diabetologo(self, mock_get_cursor):
        # Configura il mock
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (456, "Luigi", "Verdi")
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        
        # Mock get_id_paziente
        with patch.object(self.paziente, 'get_id_paziente', return_value=123):
            # Test
            result = self.paziente.get_diabetologo()
            expected = [{"id": 456, "nome": "Luigi", "cognome": "Verdi"}]
            self.assertEqual(result, expected)


class TestDiabetologo(unittest.TestCase):
    
    def setUp(self):
        self.diabetologo = model.Diabetologo(
            nome="Luigi",
            cognome="Verdi",
            data_nascita="1975-05-15",
            sesso="M",
            codice_fiscale="VRDLGU75M15H501R",
            indirizzo="Via Milano 2",
            citta="Milano",
            cap="20100",
            telefono="0987654321",
            email="luigi.verdi@example.com",
            username="lverdi",
            pw="password456"
        )
    
    @patch('model.DBSingleton.get_cursor')
    def test_get_id_diabetologo(self, mock_get_cursor):
        # Configura il mock
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (789,)
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        
        # Test
        result = self.diabetologo.get_id_diabetologo()
        self.assertEqual(result, 789)
        
        # Verifica query
        mock_cursor.execute.assert_called_once_with(
            """SELECT id_diabetologo
                        FROM Diabetologo 
                        WHERE codice_fiscale = %s""",
                        ("VRDLGU75M15H501R",)
        )
    
    @patch('model.DBSingleton.get_cursor')
    def test_inserisci_terapia(self, mock_get_cursor):
        # Configura il mock
        mock_cursor = MagicMock()
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        
        # Mock get_id_diabetologo
        with patch.object(self.diabetologo, 'get_id_diabetologo', return_value=789):
            # Test
            self.diabetologo.inserisci_terapia(
                id_paz=123,
                farmaco="Insulina",
                dose="10 UI",
                assunzioni_gg=2,
                data_inizio="2023-01-01",
                data_fine="2023-12-31",
                indicazioni="Prima dei pasti"
            )
            
            # Verifica query
            mock_cursor.execute.assert_called_once_with(
                """INSERT INTO Terapia 
                        (paziente, diabetologo, farmaco, dosaggio, assunzioni_gg, data_inizio, data_fine,indicazioni) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s,%s)""",
                        (123, 789, "Insulina", "10 UI", 2, "2023-01-01", "2023-12-31", "Prima dei pasti")
            )
    
    @patch('model.DBSingleton.get_cursor')
    def test_visualizza_n_c_pazienti_associati(self, mock_get_cursor):
        # Configura il mock
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            (123, "Mario", "Rossi", 120.5),
            (124, "Anna", "Bianchi", 110.2)
        ]
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        
        # Mock get_id_diabetologo
        with patch.object(self.diabetologo, 'get_id_diabetologo', return_value=789):
            # Test
            result = self.diabetologo.visualizza_n_c_pazienti_associati()
            expected = [
                {"id": 123, "nome": "Mario", "cognome": "Rossi", "media": 120.5},
                {"id": 124, "nome": "Anna", "cognome": "Bianchi", "media": 110.2}
            ]
            self.assertEqual(result, expected)


class TestPazienteDiabetologoObserver(unittest.TestCase):
    
    def setUp(self):
        self.paziente = model.Paziente(
            nome="Mario",
            cognome="Rossi",
            data_nascita="1980-01-01",
            sesso="M",
            codice_fiscale="RSSMRA80A01H501R",
            indirizzo="Via Roma 1",
            citta="Roma",
            cap="00100",
            telefono="1234567890",
            email="mario.rossi@example.com",
            username="mrossi",
            pw="password123"
        )
        self.observer = model.PazienteDiabetologoObserver(self.paziente)
    
    @patch('model.DBSingleton.get_cursor')
    def test_on_diabetologo_deleted(self, mock_get_cursor):
        # Configura i mock
        mock_cursor = MagicMock()
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        
        # Mock per _trova_nuovo_diabetologo
        mock_cursor.fetchone.side_effect = [
            (456,),  # Nuovo diabetologo
            ("Luigi", "Verdi")  # Dettagli nuovo diabetologo
        ]
        
        # Mock get_id_paziente
        with patch.object(self.paziente, 'get_id_paziente', return_value=123):
            # Test
            self.observer.on_diabetologo_deleted(789, "Dr. Smith")
            
            # Verifica che il paziente sia stato riassegnato
            mock_cursor.execute.assert_any_call("""
                UPDATE Paziente
                SET diabetologo_associato = %s
                WHERE id_paziente = %s
            """, (456, 123))
            
            # Verifica che l'alert sia stato creato
            mock_cursor.execute.assert_any_call("""
                INSERT INTO alerts (id_paziente, orario, alert_case)
                VALUES (%s, %s, %s)
            """, (123, unittest.mock.ANY, unittest.mock.ANY))

class TestAdmin(unittest.TestCase):
    
    def setUp(self):
        self.admin = model.Admin(
            nome="Admin",
            cognome="System",
            data_nascita="1980-01-01",
            sesso="M",
            codice_fiscale="DMNSYM80A01H501R",
            indirizzo="Via Admin 1",
            citta="Roma",
            cap="00100",
            telefono="1234567890",
            email="admin@system.com",
            username="admin",
            pw="admin123"
        )

    @patch('model.DBSingleton.get_cursor')
    def test_get_id_admin(self, mock_get_cursor):
        # Configura il mock
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (1,)
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        
        # Test
        result = self.admin.get_id_admin()
        self.assertEqual(result, 1)
        
        # Verifica query
        mock_cursor.execute.assert_called_once_with(
            "SELECT id_admin FROM Admin WHERE codice_fiscale = %s",
            ("DMNSYM80A01H501R",)
        )

    @patch('model.DBSingleton.get_cursor')
    def test_genera_username_paziente(self, mock_get_cursor):
        # Configura il mock con tutti i campi necessari (15 elementi)
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (
            1, "Mario", "Rossi", "1980-01-01", "M", "RSSMRA80A01H501R",
            "Via Roma 1", "Roma", "00100", "1234567890", "mario@example.com",
            True, None, None, "password123"
        )
        mock_cursor.fetchall.return_value = [("Mario", "Rossi")]
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        
        username = model.Admin.genera_username(1)
        self.assertEqual(username, "Mario.Rossi1_P")

    @patch('model.DBSingleton.get_cursor')
    def test_genera_username_diabetologo(self, mock_get_cursor):
        # Configura il mock con TUTTI i 15 campi necessari
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (
            1,                      # id_richiesta
            "Luigi",                # nome
            "Verdi",                # cognome
            "1975-05-15",           # data_nascita
            "M",                    # sesso
            "VRDLGU75M15H501R",     # codice_fiscale
            "Via Milano 2",         # indirizzo
            "Milano",               # citta
            "20100",                # cap
            "0987654321",           # telefono
            "luigi@example.com",    # email
            False,                  # flag_paziente (False per diabetologo)
            None,                   # stato_richiesta
            None,                   # data_richiesta
            "password456"           # password
        )
        mock_cursor.fetchall.return_value = [("Luigi", "Verdi")]  # Diabetologi esistenti
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        
        username = model.Admin.genera_username(1)
        self.assertEqual(username, "Luigi.Verdi1_D")

    @patch('model.DBSingleton.get_cursor')
    def test_inserisci_paziente(self, mock_get_cursor):
        # Configura il mock
        mock_cursor = MagicMock()
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        
        # Crea un paziente di test
        paziente = model.Paziente(
            nome="Mario", cognome="Rossi", data_nascita="1980-01-01", sesso="M",
            codice_fiscale="RSSMRA80A01H501R", indirizzo="Via Roma 1", citta="Roma",
            cap="00100", telefono="1234567890", email="mario@example.com",
            username="mrossi", pw="password123"
        )
        
        # Test
        model.Admin.inserisci_paziente(paziente)
        
        # Verifica
        args, _ = mock_cursor.execute.call_args
        # Normalizza la query SQL rimuovendo spazi extra e newline
        normalized_sql = ' '.join(args[0].split())
        
        # Verifica solo la struttura base senza dipendere dalla formattazione esatta
        self.assertTrue("INSERT INTO Paziente" in normalized_sql)
        self.assertTrue("VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" in normalized_sql)
        
        # Verifica i parametri
        self.assertEqual(args[1], (
            "Mario", "Rossi", "1980-01-01", "M", "RSSMRA80A01H501R", 
            "Via Roma 1", "Roma", "00100", "1234567890", 
            "mario@example.com", "mrossi", "password123"
        ))

    @patch('model.DBSingleton.get_cursor')
    def test_associa_a_diabetologo(self, mock_get_cursor):
        # Configura il mock
        mock_cursor = MagicMock()
        mock_cursor.fetchone.side_effect = [
            (1,),  # ID diabetologo con meno pazienti
            None    # Per l'update
        ]
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        
        # Crea un paziente di test
        paziente = model.Paziente(
            nome="Mario", cognome="Rossi", data_nascita="1980-01-01", sesso="M",
            codice_fiscale="RSSMRA80A01H501R", indirizzo="Via Roma 1", citta="Roma",
            cap="00100", telefono="1234567890", email="mario@example.com",
            username="mrossi", pw="password123"
        )
        
        # Test
        model.Admin.associa_a_diabetologo(paziente)
        
        # Verifica con SQL normalizzato
        calls = [re.sub(r'\s+', ' ', call[0][0]).strip() 
                for call in mock_cursor.execute.call_args_list]
        
        expected_select = "SELECT d.id_diabetologo FROM diabetologo d LEFT JOIN paziente p ON d.id_diabetologo = p.diabetologo_associato GROUP BY d.id_diabetologo ORDER BY COUNT(p.id_paziente) ASC LIMIT 1"
        self.assertTrue(any(expected_select in call for call in calls), 
                    "Query di selezione diabetologo non trovata")
    # @patch('model.DBSingleton.get_cursor')
    # @patch('model.Admin.genera_username')
    # @patch('model.PersonaFactory.crea_persona')
    # @patch('model.Admin.inserisci_paziente')
    # @patch('model.Admin.associa_a_diabetologo')
    @patch('model.DBSingleton.get_cursor')
    def test_approva_richiesta_paziente(self, mock_get_cursor):
        # Configura il mock
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (
            1, "Mario", "Rossi", "1980-01-01", "M", "RSSMRA80A01H501R", 
            "Via Roma 1", "Roma", "00100", "1234567890", "mario@example.com", 
            True, None, None, "password123"
        )
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        
        # Test
        model.Admin.approva_richiesta(1)
        
        # Verifica con SQL normalizzato
        calls = [call[0][0] for call in mock_cursor.execute.call_args_list]
        update_calls = [c for c in calls if 'UPDATE RichiesteAccount' in c]
        self.assertTrue(update_calls, "Update query non chiamata")

        @patch('model.DBSingleton.get_cursor')
        def test_rifiuta_richiesta(self, mock_get_cursor):
            # Configura il mock
            mock_cursor = MagicMock()
            mock_cursor.fetchone.return_value = (1,)  # Simula che la richiesta esista
            mock_get_cursor.return_value.__enter__.return_value = mock_cursor
            
            # Test
            model.Admin.rifiuta_richiesta(1)
            
            # Verifica query
            mock_cursor.execute.assert_called_with(
                "UPDATE RichiesteAccount SET stato_richiesta=%s WHERE id_richiesta = %s",
                ('rifiutata', 1)
            )

    @patch('model.DBSingleton.get_cursor')
    def test_elimina_paziente(self, mock_get_cursor):
        # Configura il mock
        mock_cursor = MagicMock()
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        
        # Test
        model.Admin.elimina_paziente(1)
        
        # Verifica query
        mock_cursor.execute.assert_called_once_with(
            "DELETE FROM Paziente WHERE id_paziente = %s", (1,)
        )

    @patch('model.DBSingleton.get_cursor')
    @patch('model.PazienteDiabetologoObserver')
    def test_elimina_diabetologo(self, mock_observer, mock_get_cursor):
        # Configura il mock
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = ("Luigi", "Verdi")  # Nome e cognome diabetologo
        mock_cursor.fetchall.return_value = [  # Pazienti associati
            ("Mario", "Rossi", "1980-01-01", "M", "RSSMRA80A01H501R", 
             "Via Roma 1", "Roma", "00100", "1234567890", "mario@example.com",
             "mrossi", "password123")
        ]
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        
        # Configura l'Observer mock
        observer_instance = MagicMock()
        mock_observer.return_value = observer_instance
        
        # Test
        self.admin.elimina_diabetologo(1)
        
        # Verifiche
        mock_cursor.execute.assert_any_call(
            "SELECT nome, cognome FROM Diabetologo WHERE id_diabetologo = %s", (1,))
        
        # Verifica che l'observer sia stato chiamato
        observer_instance.on_diabetologo_deleted.assert_called_once_with(1, "Luigi Verdi")
        
        # Verifica che il diabetologo sia stato eliminato
        mock_cursor.execute.assert_called_with(
            "DELETE FROM Diabetologo WHERE id_diabetologo = %s", (1,)
        )


class TestPersonaFactory(unittest.TestCase):
    
    def test_crea_persona_paziente(self):
        persona = model.PersonaFactory.crea_persona(
            "paziente", "Mario", "Rossi", "1980-01-01", "M", "RSSMRA80A01H501R",
            "Via Roma 1", "Roma", "00100", "1234567890", "mario@example.com",
            "mrossi", "password123"
        )
        self.assertIsInstance(persona, model.Paziente)
        self.assertEqual(persona.nome, "Mario")
        self.assertEqual(persona.cognome, "Rossi")
    
    def test_crea_persona_diabetologo(self):
        persona = model.PersonaFactory.crea_persona(
            "diabetologo", "Luigi", "Verdi", "1975-05-15", "M", "VRDLGU75M15H501R",
            "Via Milano 2", "Milano", "20100", "0987654321", "luigi@example.com",
            "lverdi", "password456"
        )
        self.assertIsInstance(persona, model.Diabetologo)
        self.assertEqual(persona.nome, "Luigi")
        self.assertEqual(persona.cognome, "Verdi")
    
    def test_crea_persona_admin(self):
        persona = model.PersonaFactory.crea_persona(
            "admin", "Admin", "System", "1980-01-01", "M", "DMNSYM80A01H501R",
            "Via Admin 1", "Roma", "00100", "1234567890", "admin@system.com",
            "admin", "admin123"
        )
        self.assertIsInstance(persona, model.Admin)
        self.assertEqual(persona.nome, "Admin")
        self.assertEqual(persona.cognome, "System")
    
    def test_crea_persona_tipo_non_valido(self):
        with self.assertRaises(ValueError):
            model.PersonaFactory.crea_persona(
                "tipo_non_valido", "Nome", "Cognome", "2000-01-01", "M", "CODICEFISCALE",
                "Indirizzo", "Città", "00100", "1234567890", "email@example.com",
                "username", "password"
            )


class TestUtilityMethods(unittest.TestCase):

    @patch('model.DBSingleton.get_cursor')
    def test_get_contatti_diabetologo(self, mock_get_cursor):
        # Configura il mock per un diabetologo
        mock_diabetologo = MagicMock(spec=model.Diabetologo)
        mock_diabetologo.get_all_pazienti_associati.return_value = [
            {"id": 1, "nome": "Paziente1", "cognome": "Test1"},
            {"id": 2, "nome": "Paziente2", "cognome": "Test2"}
        ]
        
        # Test per diabetologo
        with patch('model.current_user', mock_diabetologo):
            result = model.get_contatti()
            self.assertEqual(len(result), 2)
            mock_diabetologo.get_all_pazienti_associati.assert_called_once()

    @patch('model.DBSingleton.get_cursor')
    def test_get_contatti_paziente(self, mock_get_cursor):
        # Configura il mock per un paziente
        mock_paziente = MagicMock(spec=model.Paziente)
        mock_paziente.get_diabetologo.return_value = [{"id": 1, "nome": "Dottore", "cognome": "Test"}]
        
        # Test per paziente
        with patch('model.current_user', mock_paziente):
            result = model.get_contatti()
            self.assertEqual(len(result), 1)
            mock_paziente.get_diabetologo.assert_called_once()

    def test_get_user_id(self):
        # Test per diabetologo
        mock_diabetologo = MagicMock(spec=model.Diabetologo)
        mock_diabetologo.get_id_diabetologo.return_value = 123
        with patch('model.current_user', mock_diabetologo):
            self.assertEqual(model.get_user_id(), 123)
        
        # Test per paziente
        mock_paziente = MagicMock(spec=model.Paziente)
        mock_paziente.get_id_paziente.return_value = 456
        with patch('model.current_user', mock_paziente):
            self.assertEqual(model.get_user_id(), 456)
        
        # Test per admin
        mock_admin = MagicMock(spec=model.Admin)
        mock_admin.get_id_admin.return_value = 789
        with patch('model.current_user', mock_admin):
            self.assertEqual(model.get_user_id(), 789)

    @patch('model.DBSingleton.get_cursor')
    @patch('model.generate_password_hash')
    def test_inserisci_richiesta(self, mock_hash, mock_get_cursor):
        # Configura i mock
        mock_cursor = MagicMock()
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        mock_hash.return_value = "hashed_password"
        
        # Dati di test
        test_data = {
            "nome": "Mario", "cognome": "Rossi", "data_nascita": "1980-01-01",
            "sesso": "M", "codice_fiscale": "RSSMRA80A01H501R", 
            "indirizzo": "Via Roma 1", "citta": "Roma", "cap": "00100",
            "telefono": "1234567890", "email": "mario@example.com",
            "is_paziente": True, "password": "password123"
        }
        
        # Test
        model.inserisci_richiesta(**test_data)
        
        # Verifiche
        mock_hash.assert_called_once_with("password123")
        mock_cursor.execute.assert_called_once()
        args, _ = mock_cursor.execute.call_args
        self.assertTrue("INSERT INTO RichiesteAccount" in args[0])
        self.assertEqual(args[1][:10], (
            "Mario", "Rossi", "1980-01-01", "M", "RSSMRA80A01H501R",
            "Via Roma 1", "Roma", "00100", "1234567890", "mario@example.com"
        ))
        self.assertEqual(args[1][10], True)
        self.assertEqual(args[1][11], "hashed_password")

    @patch('model.DBSingleton.get_cursor')
    @patch('model.PersonaFactory.crea_persona')
    def test_get_by_username(self, mock_crea_persona, mock_get_cursor):
        # Configura i mock
        mock_cursor = MagicMock()
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        
        # Test per paziente
        mock_cursor.fetchone.return_value = (
            "Mario", "Rossi", "1980-01-01", "M", "RSSMRA80A01H501R",
            "Via Roma 1", "Roma", "00100", "1234567890", "mario@example.com",
            "mrossi", "hashed_pw"
        )
        result = model.get_by_username("mrossi")
        mock_crea_persona.assert_called_once_with(
            "paziente", "Mario", "Rossi", "1980-01-01", "M", "RSSMRA80A01H501R",
            "Via Roma 1", "Roma", "00100", "1234567890", "mario@example.com",
            "mrossi", "hashed_pw"
        )
        
        # Test per nessun utente trovato
        mock_cursor.fetchone.return_value = None
        result = model.get_by_username("nonexistent")
        self.assertIsNone(result)

    @patch('model.DBSingleton.get_cursor')
    def test_get_richieste_account_pazienti(self, mock_get_cursor):
        # Configura il mock
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            (1, "Mario", "Rossi", "RSSMRA80A01H501R"),
            (2, "Luigi", "Verdi", "VRDLGU75M15H501R")
        ]
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        
        # Test
        result = model.get_richieste_account_pazienti()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["label"], "Mario Rossi RSSMRA80A01H501R")
        self.assertEqual(result[0]["value"], 1)
        
        # Verifica query
        mock_cursor.execute.assert_called_once_with(
            "SELECT id_richiesta, nome, cognome, codice_fiscale FROM richiesteaccount WHERE stato_richiesta = %s AND paziente = %s", 
            ("in_attesa", "TRUE",)
        )

    @patch('model.DBSingleton.get_cursor')
    def test_get_dati_richiesta_account_by_id(self, mock_get_cursor):
        # Configura il mock
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (
            "Mario", "Rossi", "1980-01-01", "M", "RSSMRA80A01H501R",
            "Via Roma 1", "Roma", "00100", "1234567890", "mario@example.com",
            True, datetime.now(), "in_attesa"
        )
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        
        # Test
        result = model.get_dati_richiesta_account_by_id(1)
        self.assertEqual(result["nome"], "Mario")
        self.assertEqual(result["cognome"], "Rossi")
        self.assertEqual(result["paziente"], True)
        
        # Verifica query
        mock_cursor.execute.assert_called_once()

    @patch('model.DBSingleton.get_cursor')
    def test_get_dettagli_paziente(self, mock_get_cursor):
        # Configura il mock
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (
            1, "Mario", "Rossi", "1980-01-01", "M", "RSSMRA80A01H501R",
            "Via Roma 1", "Roma", "00100", "1234567890", "mario@example.com",
            "mrossi", 5
        )
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        
        # Test
        result = model.get_dettagli_paziente(1)
        self.assertEqual(result["id_paziente"], 1)
        self.assertEqual(result["nome"], "Mario")
        self.assertEqual(result["diabetologo_associato"], 5)
        
        # Verifica query
        mock_cursor.execute.assert_called_once()

    @patch('model.DBSingleton.get_cursor')
    def test_get_all_pazienti(self, mock_get_cursor):
        # Configura il mock
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            (1, "Mario", "Rossi", "RSSMRA80A01H501R", "1980-01-01", "mario@example.com", "1234567890"),
            (2, "Luigi", "Verdi", "VRDLGU75M15H501R", "1975-05-15", "luigi@example.com", "0987654321")
        ]
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        
        # Test
        result = model.get_all_pazienti()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["nome"], "Mario")
        self.assertEqual(result[1]["telefono"], "0987654321")
        
        # Verifica query
        mock_cursor.execute.assert_called_once()

    @patch('model.DBSingleton.get_cursor')
    @patch('model.Diabetologo')
    @patch('model.go.Figure')
    def test_visualizza_media_glicemia_per_diabetologi(self, mock_figure, mock_diabetologo, mock_get_cursor):
        # Configura i mock
        mock_cursor = MagicMock()
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        
        # Mock per get_all_diabetologi
        mock_cursor.fetchall.return_value = [
            (1, "Luigi", "Verdi", "VRDLGU75M15H501R", "1975-05-15", "luigi@example.com", "0987654321")
        ]
        
        # Mock per Diabetologo e visualizza_n_c_pazienti_associati
        mock_diab_instance = MagicMock()
        mock_diab_instance.visualizza_n_c_pazienti_associati.return_value = [
            {"media": 120.5}, {"media": 110.2}
        ]
        mock_diabetologo.return_value = mock_diab_instance
        
        # Test
        result = model.visualizza_media_glicemia_per_diabetologi()
        
        # Verifiche
        mock_figure.assert_called_once()
        mock_diab_instance.visualizza_n_c_pazienti_associati.assert_called_once()


from model import *

class TestUtilityMethods(unittest.TestCase):

    def assertSqlEqual(self, actual, expected):
        """Helper method to compare SQL queries ignoring whitespace differences"""
        # Normalize both queries by replacing multiple spaces/tabs/newlines with single space
        actual_normalized = ' '.join(actual.split())
        expected_normalized = ' '.join(expected.split())
        self.assertEqual(actual_normalized, expected_normalized)

    @patch('model.DBSingleton.get_cursor')
    def test_visualizza_media_glicemia_pazienti_diabetologo(self, mock_get_cursor):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (
            1, "Luigi", "Verdi", "1975-05-15", "M", "VRDLGU75M15H501R",
            "Via Milano 2", "Milano", "20100", "0987654321", "luigi@example.com",
            "lverdi", "password123"
        )
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        
        mock_diabetologo = MagicMock()
        mock_diabetologo.visualizza_n_c_pazienti_associati.return_value = [
            {"nome": "Mario", "cognome": "Rossi", "media": 120.5},
            {"nome": "Anna", "cognome": "Bianchi", "media": 110.2}
        ]
        
        with patch('model.Diabetologo', return_value=mock_diabetologo):
            fig = visualizza_media_glicemia_pazienti_diabetologo(1)
            self.assertIsNotNone(fig)
            
            args, kwargs = mock_cursor.execute.call_args
            self.assertSqlEqual(args[0], "SELECT * FROM Diabetologo WHERE id_diabetologo = %s")
            self.assertEqual(args[1], (1,))

    @patch('model.DBSingleton.get_cursor')
    def test_visualizza_pazienti_associati_singolo_diab(self, mock_get_cursor):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            ("Mario", "Rossi", "mrossi"),
            ("Anna", "Bianchi", "abianchi")
        ]
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        
        result = visualizza_pazienti_associati_singolo_diab(1)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["nome"], "Mario")
        
        args, kwargs = mock_cursor.execute.call_args
        self.assertSqlEqual(args[0], 
            "SELECT p.nome, p.cognome, p.username FROM paziente p WHERE p.diabetologo_associato = %s ORDER BY p.cognome, p.nome")
        self.assertEqual(args[1], (1,))

    @patch('model.DBSingleton.get_cursor')
    def test_get_id_paziente_by_username(self, mock_get_cursor):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (123,)
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        
        result = get_id_paziente_by_username("mrossi")
        self.assertEqual(result, 123)
        
        args, kwargs = mock_cursor.execute.call_args
        self.assertSqlEqual(args[0], "SELECT id_paziente FROM paziente WHERE username = %s")
        self.assertEqual(args[1], ("mrossi",))

    @patch('model.DBSingleton.get_cursor')
    def test_get_dati_glicemia_filtrati(self, mock_get_cursor):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            (120.5, datetime.now(), None),
            (130.2, datetime.now(), "Vertigini")
        ]
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        
        result = get_dati_glicemia_filtrati(1, "settimanale", "andamento")
        self.assertEqual(len(result), 2)
        
        mock_cursor.fetchall.return_value = [(0, 125.5), (3, 130.2)]
        result = get_dati_glicemia_filtrati(1, "mensile", "media")
        self.assertEqual(len(result), 2)

    @patch('model.DBSingleton.get_cursor')
    def test_get_terapie_paziente(self, mock_get_cursor):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            (1, 1, "Insulina", "10 UI", 2, "2023-01-01", "2023-12-31", "Prima dei pasti")
        ]
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        
        result = get_terapie_paziente(1, 1)
        self.assertEqual(len(result), 1)
        
        args, _ = mock_cursor.execute.call_args
        self.assertSqlEqual(args[0], "SELECT * FROM Terapia t WHERE paziente=%s AND diabetologo=%s")
        self.assertEqual(args[1], (1, 1))

    @patch('model.DBSingleton.get_cursor')
    def test_get_info_base_paziente(self, mock_get_cursor):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (
            "mrossi", "Mario", "Rossi", "1980-01-01", "M", 120.5
        )
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        
        result = get_info_base_paziente(1, 1)
        self.assertEqual(len(result), 6)
        self.assertEqual(result[1], "Mario")
        
        args, kwargs = mock_cursor.execute.call_args
        self.assertSqlEqual(args[0], 
            "SELECT username, nome, cognome, data_nascita, sesso, COALESCE(AVG(g.valore), 0) AS media FROM paziente p LEFT JOIN Glicemia g ON p.id_paziente = g.paziente WHERE p.diabetologo_associato = %s AND p.id_paziente = %s GROUP BY p.id_paziente")
        self.assertEqual(args[1], (1, 1))

    @patch('model.DBSingleton.get_cursor')
    def test_get_info_base_diabetologo(self, mock_get_cursor):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            ("lverdi", "Luigi", "Verdi", "1975-05-15", "M", 10)
        ]
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        
        result = get_info_base_diabetologo(1)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][2], "Verdi")
        
        args, kwargs = mock_cursor.execute.call_args
        self.assertSqlEqual(args[0], 
            "SELECT d.username, d.nome, d.cognome, d.data_nascita, d.sesso, COUNT(*) FROM Diabetologo d JOIN Paziente p ON d.id_diabetologo=p.diabetologo_associato WHERE id_diabetologo=%s GROUP BY d.username,d.nome,d.cognome,d.data_nascita,d.sesso")
        self.assertEqual(args[1], (1,))

    @patch('model.DBSingleton.get_cursor')
    def test_get_messaggi(self, mock_get_cursor):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            ("Ciao", datetime.now(), True),
            ("Come stai?", datetime.now(), False)
        ]
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        
        mock_paziente = MagicMock()
        mock_paziente.__class__ = Paziente
        
        with patch('model.current_user', mock_paziente):
            result = get_messaggi(1)
            self.assertEqual(len(result), 2)
            self.assertTrue(all(isinstance(m, tuple) for m in result))
            
            args, kwargs = mock_cursor.execute.call_args
            self.assertSqlEqual(args[0], 
                "Select contenuto, orario, is_mittente from messaggio where id_paziente = %s order by orario")
            self.assertEqual(args[1], (1,))

    @patch('model.DBSingleton.get_cursor')
    def test_insert_messaggio(self, mock_get_cursor):
        mock_cursor = MagicMock()
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        
        insert_messaggio(1, "Test message", True)
        
        args, kwargs = mock_cursor.execute.call_args
        self.assertSqlEqual(args[0], 
            "Insert into messaggio values (%s,current_timestamp,%s,%s)")
        self.assertEqual(args[1], (1, True, "Test message"))

    @patch('model.DBSingleton.get_cursor')
    def test_get_nomecognome(self, mock_get_cursor):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = ("Mario", "Rossi")
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        
        result = get_nomecognome(1)
        self.assertEqual(result.nome, "Mario")
        self.assertEqual(result.cognome, "Rossi")
        
        args, kwargs = mock_cursor.execute.call_args
        self.assertSqlEqual(args[0], 
            "SELECT nome, cognome FROM diabetologo WHERE id_diabetologo = %s UNION ALL SELECT nome, cognome FROM paziente WHERE id_paziente = %s")
        self.assertEqual(args[1], (1, 1))

    @patch('model.DBSingleton.get_cursor')
    def test_modifica_dati_paziente_db(self, mock_get_cursor):
        mock_cursor = MagicMock()
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        
        modifica_dati_paziente_db(1, indirizzo="Via Nuova 1", email="new@example.com")
        
        args, kwargs = mock_cursor.execute.call_args
        self.assertTrue("UPDATE paziente" in args[0])
        self.assertEqual(args[1][0], "Via Nuova 1")
        self.assertEqual(args[1][1], "new@example.com")
        self.assertEqual(args[1][2], 1)



    @patch('model.DBSingleton.get_cursor')
    def test_check_farmaco(self, mock_get_cursor):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (True, True)
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        
        with patch('model.get_diabetologo_associato', return_value=1):
            check_farmaco(1, "TestFarmaco", "100mg")
            
            args_list = mock_cursor.execute.call_args_list
            found = False
            for args, kwargs in args_list:
                if "Insert into alerts" in args[0]:
                    self.assertSqlEqual(args[0], 
                        "Insert into alerts values(%s,current_timestamp,%s)")
                    self.assertEqual(args[1][0], 1)
                    self.assertTrue("TestFarmaco" in args[1][1])
                    found = True
            self.assertTrue(found)

    @patch('model.DBSingleton.get_cursor')
    def test_get_alerts_paziente(self, mock_get_cursor):
        mock_cursor = MagicMock()
        mock_cursor.fetchmany.return_value = [
            (datetime.now(), "Alert 1"),
            (datetime.now(), "Alert 2")
        ]
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        
        result = get_alerts_paziente(1)
        self.assertEqual(len(result), 2)
        self.assertTrue(all(isinstance(a, tuple) for a in result))
        
        args, kwargs = mock_cursor.execute.call_args
        self.assertSqlEqual(args[0], 
            "SELECT orario, alert_case FROM alerts where id_paziente = %s")
        self.assertEqual(args[1], (1,))

    @patch('model.DBSingleton.get_cursor')
    def test_get_diabetologo_associato(self, mock_get_cursor):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (1,)  # Restituisce una tupla
        mock_get_cursor.return_value.__enter__.return_value = mock_cursor
        
        # Modifica l'assert per verificare il primo elemento della tupla
        result = get_diabetologo_associato(1)
        self.assertEqual(result[0], 1)  # Verifica il primo elemento della tupla
        
        # Oppure modifica la funzione originale per restituire solo il valore
        # e non la tupla

    def test_visualizza_andamento_glicemia(self):
        test_data = [
            (120.5, datetime(2023, 1, 1), None),
            (130.2, datetime(2023, 1, 2), "Vertigini")
        ]
        
        fig = visualizza_andamento_glicemia(test_data)
        self.assertIsNotNone(fig)

    def test_visualizza_media_glicemica_fasce_orarie(self):
        test_data = [
            (0, 120.5),
            (3, 130.2),
            (6, 110.8)
        ]
        
        fig = visualizza_media_glicemica_fasce_orarie(test_data)
        self.assertIsNotNone(fig)

def test_crea_calendario_ipoglicemia_con_pallini(self):
    # Crea dati di test reali nel formato corretto
    test_data = [
        {'valore': 55.0, 'data_inserimento': '2023-05-15'},
        {'valore': 65.0, 'data_inserimento': '2023-05-20'}
    ]
    
    # Converti in DataFrame
    df = pd.DataFrame(test_data)
    
    # Converti la colonna data in datetime
    df['data_inserimento'] = pd.to_datetime(df['data_inserimento'])
    
    # Test con dati reali
    fig = crea_calendario_ipoglicemia_con_pallini(df.to_dict('records'), 2023, 5)
    self.assertIsNotNone(fig)

if __name__ == '__main__':
    unittest.main()


