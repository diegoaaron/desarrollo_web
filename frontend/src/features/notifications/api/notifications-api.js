import { http } from "../../../shared/api/http-client";

export function getMyNotifications(options) {
  return http.get("/notifications/me", options);
}

export function markNotificationRead(id) {
  return http.put(`/notifications/${id}/read`);
}

export function markAllNotificationsRead() {
  return http.put("/notifications/me/read");
}
