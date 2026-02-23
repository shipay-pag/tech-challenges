using Microsoft.AspNetCore.Mvc;

namespace Shipay.Challenge.Endpoints.Registration
{
    [ApiController]
    [Route("api")]
    public class RegistrationController : ControllerBase
    {
        private readonly RegistrationManager _manager;

        public RegistrationController(RegistrationManager manager)
        {
            _manager = manager;
        }

        [HttpGet("get-customer")]
        public Customer GetCustomer()
        {
            var idStr = HttpContext.Request.Query["id"];
            return _manager.FindCustomer(idStr);
        }
    }
}
