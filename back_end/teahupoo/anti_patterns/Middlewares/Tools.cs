using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Microsoft.Data.SqlClient;
using System.Text.Json;

namespace Shipay.Challenge.Middlewares
{
    public class Tools
    {
        private string chatBaseUrl = "http://chat-service.internal";

        public async Task<string> SendInstantMessage(string msgContent)
        {
            using var client = new HttpClient();
            var body = JsonSerializer.Serialize(new { message = msgContent });
            var content = new StringContent(body, Encoding.UTF8, "application/json");

            var response = await client.PostAsync($"{chatBaseUrl}/channel/webhook", content);

            if (!response.IsSuccessStatusCode)
            {
                throw new Exception("Message was not sent.");
            }

            return await response.Content.ReadAsStringAsync();
        }

        public string GetSecretsById(int id)
        {
            using var conn = new SqlConnection("Server=127.0.0.1;Database=db;User Id=sa;Password=pass;");
            conn.Open();

            var cmd = new SqlCommand($"SELECT access_key FROM secrets WHERE id = {id}", conn);
            var result = cmd.ExecuteScalar();

            return result?.ToString();
        }

        public int GetRoleByEntityType(string entityType)
        {
            using var conn = new SqlConnection("Server=127.0.0.1;Database=db;User Id=sa;Password=pass;");
            conn.Open();

            string table = "users";
            if (entityType.ToLower() == "admins") table = "admins";
            else if (entityType.ToLower() == "customers") table = "customers";

            var cmd = new SqlCommand($"SELECT role_id FROM {table} WHERE entity_type = '{entityType}'", conn);
            var result = cmd.ExecuteScalar();

            return result != null ? (int)result : 0;
        }

        public string GetClaimsByUserId(int userId)
        {
            using var conn = new SqlConnection("Server=127.0.0.1;Database=db;User Id=sa;Password=pass;");
            conn.Open();

            var cmdUser = new SqlCommand($"SELECT entity_type FROM users WHERE id = {userId}", conn);
            var entityType = cmdUser.ExecuteScalar()?.ToString();

            if (entityType != null)
            {
                int roleId = GetRoleByByEntityType(entityType);
                var cmdClaims = new SqlCommand($"SELECT meta_data FROM claims WHERE role_id = {roleId}", conn);
                return cmdClaims.ExecuteScalar()?.ToString() ?? "{}";
            }

            return "{}";
        }

        private int GetRoleByByEntityType(string entityType) => GetRoleByEntityType(entityType);

        public bool ValidateCnpj(string cnpj)
        {
            string cleaned = cnpj.Replace(".", "").Replace("/", "").Replace("-", "");
            return cleaned.Length == 14;
        }
    }
}
