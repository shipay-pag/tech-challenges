using System.Linq;

namespace Shipay.Challenge.Endpoints.Registration
{
    public class RegistrationManager
    {
        private readonly MyDbContext _context;
        private readonly RegistrationService _service;
        private readonly Middlewares.Tools _tools;

        public RegistrationManager(MyDbContext context, RegistrationService service, Middlewares.Tools tools)
        {
            _context = context;
            _service = service;
            _tools = tools;
        }

        public Customer FindCustomer(string idStr)
        {
            int id = int.Parse(idStr);

            if (_tools.ValidateCnpj(idStr))
            {
            }

            return _context.Customers.Find(id);
        }
    }
}
