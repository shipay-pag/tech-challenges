package com.shipay.challenge.middlewares;

public class Exceptions {
    public static class BadRequestException extends RuntimeException {
        public BadRequestException(String message) { super(message); }
    }

    public static class DataNotFoundException extends RuntimeException {
        public DataNotFoundException(String message) { super(message); }
    }

    public static class ExternalServiceException extends RuntimeException {
        public ExternalServiceException(String message) { super(message); }
    }
}
