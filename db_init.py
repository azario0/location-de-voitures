from sqlalchemy import create_engine, text
from config import Config

def init_db():
    # Extraire le nom de la base de données de l'URI
    db_name = Config.SQLALCHEMY_DATABASE_URI.split('/')[-1]
    
    # Créer une connexion sans spécifier la base de données
    engine = create_engine('/'.join(Config.SQLALCHEMY_DATABASE_URI.split('/')[:-1]))
    
    with engine.connect() as conn:
        # Vérifier si la base de données existe, sinon la créer
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))
        conn.execute(text(f"USE {db_name}"))
        
        # Créer les tables si elles n'existent pas
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS cars (
                id INT AUTO_INCREMENT PRIMARY KEY,
                mark VARCHAR(50) NOT NULL,
                color VARCHAR(30) NOT NULL,
                class_type VARCHAR(30) NOT NULL,
                category VARCHAR(50) NOT NULL
            )
        """))
        
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS allocations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                car_id INT NOT NULL,
                start_date DATE NOT NULL,
                end_date DATE NOT NULL,
                client_name VARCHAR(100) NOT NULL,
                client_email VARCHAR(100) NOT NULL,
                client_phone VARCHAR(20) NOT NULL,
                FOREIGN KEY (car_id) REFERENCES cars(id)
            )
        """))
        
    print("Base de données et tables initialisées avec succès.")