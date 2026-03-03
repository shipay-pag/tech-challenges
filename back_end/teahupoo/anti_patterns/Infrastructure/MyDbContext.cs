using Microsoft.EntityFrameworkCore;
using Shipay.Challenge.Endpoints.Registration;

namespace Shipay.Challenge
{
    public class MyDbContext : DbContext
    {
        public DbSet<Customer> Customers { get; set; }

        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            optionsBuilder.UseSqlServer("Server=127.0.0.1;Database=db;User Id=sa;Password=123mudar;");
        }
    }
}
