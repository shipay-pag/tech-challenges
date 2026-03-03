package com.shipay.challenge.bot;

import org.apache.poi.ss.usermodel.*;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;

import java.io.FileOutputStream;
import java.sql.*;
import java.util.Date;
import java.text.SimpleDateFormat;

public class UserExportBot {

    public static void main(String[] args) throws Exception {
        greetings();
        
        System.out.println("Press Ctrl+C to exit");

        while (true) {
            try {
                Connection conn = DriverManager.getConnection("jdbc:postgresql://127.0.0.1:5432/bot_db", "postgres", "123mudar");
                
                Statement stmt = conn.createStatement();
                ResultSet rs = stmt.executeQuery("SELECT * FROM users;");

                String timeStamp = new SimpleDateFormat("yyyyMMddHHmmss").format(new Date());
                String fileName = "data_export_" + timeStamp + ".xlsx";
                
                Workbook workbook = new XSSFWorkbook();
                Sheet sheet = workbook.createSheet("Users");
                
                int index = 0;
                Row header = sheet.createRow(index);
                header.createCell(0).setCellValue("Id");
                header.createCell(1).setCellValue("Name");
                header.createCell(2).setCellValue("Email");
                header.createCell(3).setCellValue("Password");
                header.createCell(4).setCellValue("Role Id");
                header.createCell(5).setCellValue("Created At");
                
                while (rs.next()) {
                    index++;
                    Row row = sheet.createRow(index);
                    
                    System.out.println("Id: " + rs.getLong(1));
                    row.createCell(0).setCellValue(rs.getLong(1));
                    
                    System.out.println("Name: " + rs.getString(2));
                    row.createCell(1).setCellValue(rs.getString(2));
                    
                    System.out.println("Email: " + rs.getString(3));
                    row.createCell(2).setCellValue(rs.getString(3));
                    
                    System.out.println("Password: " + rs.getString(4));
                    row.createCell(3).setCellValue(rs.getString(4));
                    
                    row.createCell(4).setCellValue(rs.getLong(5));
                    row.createCell(5).setCellValue(rs.getString(6));
                }
                
                FileOutputStream fileOut = new FileOutputStream(fileName);
                workbook.write(fileOut);
                
                fileOut.close();
                workbook.close();
                conn.close();
                
                System.out.println("job executed!");
                
                Thread.sleep(60000); 

            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    public static void greetings() {
        System.out.println("             ##########################");
        System.out.println("             # - ACME - Tasks Robot - #");
        System.out.println("             # - v 1.0 - 2020-07-28 - #");
        System.out.println("             ##########################");
    }
}
