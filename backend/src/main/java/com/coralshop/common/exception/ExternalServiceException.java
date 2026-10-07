package com.coralshop.common.exception;

import org.springframework.http.HttpStatus;

/** Falla de un proveedor externo (p. ej. CJ); conserva el código HTTP que se devolverá. */
public class ExternalServiceException extends RuntimeException {

    private final HttpStatus status;

    public ExternalServiceException(HttpStatus status, String message) {
        super(message);
        this.status = status;
    }

    public ExternalServiceException(HttpStatus status, String message, Throwable cause) {
        super(message, cause);
        this.status = status;
    }

    public HttpStatus getStatus() {
        return status;
    }
}
