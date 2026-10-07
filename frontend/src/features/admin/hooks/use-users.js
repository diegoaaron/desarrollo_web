import { useState, useEffect } from "react";
import { usersService } from "../services/users-service";

export function useUsers() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [actionError, setActionError] = useState(null);
  const [updatingId, setUpdatingId] = useState(null);

  useEffect(() => {
    let cancelled = false;

    async function fetchUsers() {
      try {
        const data = await usersService.getAll();
        if (!cancelled) setUsers(data);
      } catch (err) {
        if (!cancelled) setError(err.message);
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    fetchUsers();

    return () => {
      cancelled = true;
    };
  }, []);

  const updateRole = async (id, roleId) => {
    setActionError(null);
    setUpdatingId(id);
    try {
      await usersService.updateRole(id, roleId);
      const data = await usersService.getAll();
      setUsers(data);
      return true;
    } catch (err) {
      setActionError(`No se pudo cambiar el rol del usuario #${id}: ${err.message}`);
      return false;
    } finally {
      setUpdatingId(null);
    }
  };

  const clearActionError = () => setActionError(null);

  return {
    users,
    loading,
    error,
    actionError,
    updatingId,
    updateRole,
    clearActionError,
  };
}
