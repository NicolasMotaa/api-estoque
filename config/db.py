from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# 1. Descobre o caminho absoluto da pasta raiz do projeto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# 2. Força o load_dotenv a procurar o arquivo .env exatamente nessa pasta raiz
load_dotenv(os.path.join(BASE_DIR, ".env"))

# 3. Puxa a variável
url = os.getenv("DATABASE_URL")

# 4. Trava de segurança: se der erro, ele avisa o que aconteceu antes de travar o SQLAlchemy
if url is None:
    raise ValueError("Erro: O arquivo .env não foi encontrado na raiz ou a chave DATABASE_URL não existe nele!")

engine = create_engine(url)
Session = sessionmaker(bind=engine)
Base = declarative_base()