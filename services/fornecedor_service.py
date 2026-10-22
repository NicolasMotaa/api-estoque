from repositories.fornecedor_repository import FornecedorRepository
from schemas.fornecedor import FornecedorCreate, FornecedorUpdate
from fastapi import HTTPException, status

class FornecedorService:
    def __init__(self, repo: FornecedorRepository):
        self.repo = repo

    def criar_fornecedor(self, fornecedor_data: FornecedorCreate):

        #regra: nome não nulo
        if not fornecedor_data.nome:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="O fornecedor deve ter um nome")
        
        #regra: cnpj deve ser único
        if self.repo.get_by_cnpj(fornecedor_data.cnpj):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Impossível continuar: O CNPJ já está cadastrado na plataforma.")

        #regra: email deve ser único
        if self.repo.get_by_email(fornecedor_data.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Email já cadastrado")

        return self.repo.create(fornecedor_data)

    def listar_fornecedores(self):
        return self.repo.get_all()

    def obter_fornecedor(self, fornecedor_id:int):
        fornecedor =self.repo.get_by_id(fornecedor_id)
        if not fornecedor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Fornecedor não encontrado")
        return fornecedor

    def get_list_of_produtos(self, fornecedor_id:int):
        #validação
        self.obter_fornecedor(fornecedor_id)

        return self.repo.get_produtos_do_fornecedor(fornecedor_id)

    def atualizar_fornecedor(self, fornecedor_id:int, fornecedor_data:FornecedorUpdate):
        #validação
        db_fornecedor = self.obter_fornecedor(fornecedor_id)
        
        #verifica o caso de tentar mudar o email para um já existente
        if fornecedor_data.email and fornecedor_data.email != db_fornecedor.email:
            if self.repo.get_by_email(fornecedor_data.email):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                    detail="Email já cadastrado em outro fornecedor.")

        update_data = fornecedor_data.model_dump(exclude_unset=True)
        return self.repo.update(db_fornecedor, update_data)

    def excluir_fornecedor(self, fornecedor_id:int):
        db_fornecedor = self.obter_fornecedor(fornecedor_id)
        return self.repo.delete(db_fornecedor)