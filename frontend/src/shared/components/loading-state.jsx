export function LoadingState({ message = "Cargando..." }) {
  return (
    <div className="flex min-h-64 items-center justify-center" role="status">
      <p className="text-gray-600">{message}</p>
    </div>
  );
}
