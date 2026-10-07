package com.coralshop.common.exception;

/** La solicitud está bien formada pero viola una regla de negocio (422). */
public class BusinessRuleException extends RuntimeException {

    public BusinessRuleException(String message) {
        super(message);
    }

    public BusinessRuleException(String message, Throwable cause) {
        super(message, cause);
    }
}
