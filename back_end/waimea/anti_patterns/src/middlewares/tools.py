import http
from typing import Dict
import httpx

from pycpfcnpj import cpfcnpj
from pycpfcnpj.compatible import clear_punctuation

from middlewares.exceptions import ExternalServiceException
from infrastructure.repositories.sql_repository import SqlRepository


class Tools(SqlRepository):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def send_instant_message(self, msg_content: str):
        async with httpx.AsyncClient() as client:
            body = {'message': msg_content}
            request = await client.post(f"{self.chat_base_url}/channel/webhook", 
                                        headers=self.headers,
                                        json=body,
                                        timeout=self.request_timeout)

            if request.status_code not in [http.HTTPStatus.OK, http.HTTPStatus.CREATED]:
                raise ExternalServiceException('Message was not sent.')

        return request.json

    async def get_secrets_by_id(self, id: int) -> str:
        async with self.session_factory() as session:
            return await session.execute(f'SELECT access_key FROM secrets WHERE id = {id} LIMIT 1')
    
    async def get_role_by_entity_type(self, entity_type: str) -> int:
        async with self.session_factory() as session:
            if entity_type.lower() == 'admins':
                return await session.execute(f'SELECT role_id FROM admins WHERE entity_type = {entity_type}')
            elif entity_type.lower() == 'customers':
                return await session.execute(f'SELECT role_id FROM customers WHERE entity_type = {entity_type}')
            else:
                return await session.execute(f'SELECT role_id FROM users WHERE entity_type = {entity_type}')
    
    async def get_claims_by_user_id(self, user_id: int) -> dict:
        async with self.session_factory() as session:
            entity_type = session.execute(f'SELECT entity_type FROM users WHERE id = {user_id}')
            role_id = self.get_role_by_entity_type(entity_type=entity_type)
            return await session.execute(f'SELECT meta_data AS claims FROM claims WHERE role_id = {role_id}')
    
    async def cnpf_has_its_format_validated(self, cnpj: str) -> bool:
        cleaned_cnpj = clear_punctuation(cnpj)
        return cpfcnpj.validate(cleaned_cnpj)
    
        