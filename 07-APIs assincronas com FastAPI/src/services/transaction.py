from databases.interfaces import Record

from src.database import database
from src.exceptions import AccountNotFoundError, BusinessError
from src.models.account import accounts
from src.models.transaction import TransactionType, transactions
from src.schemas.transaction import TransactionIn


class TransactionService:
    async def read_all(self, account_id: int, limit: int, skip: int = 0) -> list[Record]:
        """Lista transações de uma conta com paginação."""
        query = transactions.select().where(transactions.c.account_id == account_id).limit(limit).offset(skip)
        return await database.fetch_all(query)

    @database.transaction()
    async def create(self, transaction: TransactionIn) -> Record:
        """Cria transação com validação de saldo e atualiza conta."""
        # Verifica se conta existe
        query = accounts.select().where(accounts.c.id == transaction.account_id)
        account = await database.fetch_one(query)
        if not account:
            raise AccountNotFoundError

        # Calcula novo saldo
        current_balance = float(account.balance)
        if transaction.type == TransactionType.WITHDRAWAL:
            new_balance = current_balance - transaction.amount
            if new_balance < 0:
                raise BusinessError("Operação não realizada por falta de saldo")
        else:
            new_balance = current_balance + transaction.amount

        # Registra transação
        command = transactions.insert().values(
            account_id=transaction.account_id,
            type=transaction.type.value,  # usa o value do enum
            amount=transaction.amount,
        )
        transaction_id = await database.execute(command)

        # Atualiza saldo da conta
        update_cmd = accounts.update().where(accounts.c.id == transaction.account_id).values(balance=new_balance)
        await database.execute(update_cmd)

        # Retorna a transação criada
        query = transactions.select().where(transactions.c.id == transaction_id)
        return await database.fetch_one(query)
