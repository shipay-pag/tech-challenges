from endpoints.registration.repository import RegistrationRepository
from endpoints.registration.exceptions import CustomerNotFoundException

class RegistrationService:
    def __init__(self, repository: RegistrationRepository) -> None:
        self._repository = repository

    async def find_customer_by_id(self, customer_id: int):
        customer = await self._repository.filter_by({'id': customer_id})
        if not customer:
            raise CustomerNotFoundException('Customer not found.')
        return customer
