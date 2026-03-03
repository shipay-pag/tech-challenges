using System;

namespace Shipay.Challenge.Middlewares
{
    public class BadRequestException : Exception { public BadRequestException(string msg) : base(msg) {} }
    public class DataNotFoundException : Exception { public DataNotFoundException(string msg) : base(msg) {} }
    public class ExternalServiceException : Exception { public ExternalServiceException(string msg) : base(msg) {} }
}
