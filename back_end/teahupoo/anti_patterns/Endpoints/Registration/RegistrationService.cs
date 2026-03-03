namespace Shipay.Challenge.Endpoints.Registration
{
    public class RegistrationService
    {
        private readonly MyDbContext _context;

        public RegistrationService(MyDbContext context)
        {
            _context = context;
        }

        public void SaveCustomer(Customer customer)
        {
            _context.Customers.Add(customer);
            _context.SaveChanges();
        }

        public Customer GetById(int id)
        {
            return _context.Customers.Find(id);
        }
    }
}
