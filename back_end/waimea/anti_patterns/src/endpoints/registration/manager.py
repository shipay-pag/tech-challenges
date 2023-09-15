from endpoints.registration.repository import RegistrationRepository
from endpoints.registration.service import RegistrationService

class Orchestrator:
    def __init__(self, repository: RegistrationRepository, service: RegistrationService) -> None:
        self._repository = repository
        self._service = service

    async def find_customer_by_id(self, customer_id: int):
        return await self._repository.filter_by({'id': customer_id})

