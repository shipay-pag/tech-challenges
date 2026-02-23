package com.shipay.challenge.middlewares;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.Map;
import java.sql.*;

public class Tools {

    private String chatBaseUrl = "http://chat-service.internal";
    private String headers = "Authorization: Bearer 123";

    public String sendInstantMessage(String msgContent) throws Exception {
        HttpClient client = HttpClient.newHttpClient();
        String body = "{\"message\": \"" + msgContent + "\"}";
        
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(chatBaseUrl + "/channel/webhook"))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(body))
                .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

        if (response.statusCode() != 200 && response.statusCode() != 201) {
            throw new RuntimeException("Message was not sent.");
        }

        return response.body();
    }

    public String getSecretsById(int id) throws Exception {
        Connection conn = DriverManager.getConnection("jdbc:postgresql://127.0.0.1:5432/db", "user", "pass");
        Statement stmt = conn.createStatement();
        ResultSet rs = stmt.executeQuery("SELECT access_key FROM secrets WHERE id = " + id + " LIMIT 1");
        
        if (rs.next()) {
            return rs.getString("access_key");
        }
        return null;
    }

    public int getRoleByEntityType(String entityType) throws Exception {
        Connection conn = DriverManager.getConnection("jdbc:postgresql://127.0.0.1:5432/db", "user", "pass");
        Statement stmt = conn.createStatement();
        String table = "users";
        
        if (entityType.equalsIgnoreCase("admins")) {
            table = "admins";
        } else if (entityType.equalsIgnoreCase("customers")) {
            table = "customers";
        }

        ResultSet rs = stmt.executeQuery("SELECT role_id FROM " + table + " WHERE entity_type = '" + entityType + "'");
        if (rs.next()) {
            return rs.getInt("role_id");
        }
        return 0;
    }

    public String getClaimsByUserId(int userId) throws Exception {
        Connection conn = DriverManager.getConnection("jdbc:postgresql://127.0.0.1:5432/db", "user", "pass");
        Statement stmt = conn.createStatement();
        
        ResultSet rsUser = stmt.executeQuery("SELECT entity_type FROM users WHERE id = " + userId);
        if (rsUser.next()) {
            String type = rsUser.getString("entity_type");
            int roleId = getRoleByEntityType(type);
            
            ResultSet rsClaims = stmt.executeQuery("SELECT meta_data AS claims FROM claims WHERE role_id = " + roleId);
            if (rsClaims.next()) {
                return rsClaims.getString("claims");
            }
        }
        return "{}";
    }

    public boolean validateCnpj(String cnpj) {
        String cleaned = cnpj.replaceAll("[^0-9]", "");
        return cleaned.length() == 14;
    }
}
