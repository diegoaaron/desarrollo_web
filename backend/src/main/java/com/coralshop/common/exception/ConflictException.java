package com.coralshop.common.exception;

/** La operación entra en conflicto con datos existentes (409). */
public class ConflictException extends RuntimeException {

    public ConflictException(String message) {
        super(message);
    }

    public ConflictException(String message, Throwable cause) {
        super(message, cause);
    }
}
