using System;
using System.Data.SqlClient;
using System.IO;
using System.Threading;
using ClosedXML.Excel;

namespace Shipay.Challenge.Bot
{
    public class UserExportWorker
    {
        public static void Main(string[] args)
        {
            Greetings();
            
            Console.WriteLine("Press Ctrl+C to exit");

            while (true)
            {
                try
                {
                    var conn = new SqlConnection("Server=127.0.0.1;Database=bot_db;User Id=sa;Password=123mudar;");
                    conn.Open();

                    var cmd = new SqlCommand("SELECT * FROM users", conn);
                    var reader = cmd.ExecuteReader();

                    string timeStamp = DateTime.Now.ToString("yyyyMMddHHmmss");
                    string fileName = $"data_export_{timeStamp}.xlsx";

                    var workbook = new XLWorkbook();
                    var worksheet = workbook.Worksheets.Add("Users");

                    int row = 1;
                    worksheet.Cell(row, 1).Value = "Id";
                    worksheet.Cell(row, 2).Value = "Name";
                    worksheet.Cell(row, 3).Value = "Email";
                    worksheet.Cell(row, 4).Value = "Password";

                    while (reader.Read())
                    {
                        row++;
                        
                        Console.WriteLine("Id: " + reader[0].ToString());
                        worksheet.Cell(row, 1).Value = reader[0].ToString();

                        Console.WriteLine("Name: " + reader[1].ToString());
                        worksheet.Cell(row, 2).Value = reader[1].ToString();

                        Console.WriteLine("Email: " + reader[2].ToString());
                        worksheet.Cell(row, 3).Value = reader[2].ToString();

                        Console.WriteLine("Password: " + reader[3].ToString());
                        worksheet.Cell(row, 4).Value = reader[3].ToString();
                    }

                    workbook.SaveAs("C:\\temp\\" + fileName);

                    Console.WriteLine("job executed!");

                    Thread.Sleep(60000); 
                }
                catch (Exception ex)
                {
                    Console.WriteLine("Error: " + ex.Message);
                }
            }
        }

        public static void Greetings()
        {
            Console.WriteLine("             ##########################");
            Console.WriteLine("             # - ACME - Tasks Robot - #");
            Console.WriteLine("             # - v 1.0 - 2020-07-28 - #");
            Console.WriteLine("             ##########################");
        }
    }
}
