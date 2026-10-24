from fastapi import HTTPException, status
from repositories.categoria_repository import CategoriaRepository
from schemas.categoria import CategoriaCreate, CategoriaUpdate
from config.logger import logger

class CategoriaService:
    def __init__(self, repo: CategoriaRepository):
        self.repo = repo

    def criar_categoria(self, categoria_data: CategoriaCreate):
        # Regra: nome não pode ser nulo ou vazio
        if not categoria_data.nome or not categoria_data.nome.strip():
            logger.warning("Tentativa de criação de Categoria bloqueada: Nome em branco ou nulo.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O nome da categoria não pode ser vazio."
            )

        # Regra: Nome deve ser único
        if self.repo.get_by_nome(categoria_data.nome):
            logger.warning(f"Tentativa de criação de Categoria bloqueada: O nome '{categoria_data.nome}' já está em uso.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Já existe uma categoria cadastrada com este nome."
            )

        nova_categoria = self.repo.create(categoria_data)
        
        logger.info(f"Categoria criada com sucesso: ID {nova_categoria.id} | Nome: {nova_categoria.nome}")
        return nova_categoria

    def listar_categorias(self):
        return self.repo.get_all()

    def obter_categoria(self, categoria_id: int):
        categoria = self.repo.get_by_id(categoria_id)
        if not categoria:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoria não encontrada."
            )
        return categoria

    def atualizar_categoria(self, categoria_id: int, categoria_data: CategoriaUpdate):
        db_categoria = self.obter_categoria(categoria_id)

        # verifica se o nome já existe, em caso de tentativa de alterá-lo
        if categoria_data.nome and categoria_data.nome != db_categoria.nome:
            if self.repo.get_by_nome(categoria_data.nome):
                logger.warning(
                    f"Tentativa de atualização bloqueada: Categoria ID {categoria_id} "
                    f"tentou usar o nome '{categoria_data.nome}', que já pertence a outra categoria."
                )
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Já existe outra categoria cadastrada com este nome."
                )

        update_data = categoria_data.model_dump(exclude_unset=True)
        categoria_atualizada = self.repo.update(db_categoria, update_data)
        
        logger.info(f"Categoria atualizada com sucesso: ID {categoria_id}")
        return categoria_atualizada

    def excluir_categoria(self, categoria_id: int):
        # Verificação de existência
        db_categoria = self.obter_categoria(categoria_id)

        # Impede exclusão se houver produtos vinculados
        produtos_vinculados = self.repo.get_produtos_da_categoria(categoria_id)
        if produtos_vinculados:
            logger.warning(f"Tentativa de exclusão bloqueada: Categoria ID {categoria_id} possui produtos associados.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Impossível excluir: Existem produtos associados a esta categoria. Remova ou altere a categoria dos produtos primeiro."
            )

        self.repo.delete(db_categoria)
        
        logger.info(f"Categoria excluída com sucesso: ID {categoria_id}")

    #Funcionalidade Avançada
    def obter_produtos_da_categoria(self, categoria_id: int):
        self.obter_categoria(categoria_id)
        return self.repo.get_produtos_da_categoria(categoria_id)