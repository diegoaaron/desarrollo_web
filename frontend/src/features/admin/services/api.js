// El panel usa el mismo cliente HTTP que la tienda (sesión por cookie + token CSRF).
export { http as api } from "../../../shared/api/http-client";
