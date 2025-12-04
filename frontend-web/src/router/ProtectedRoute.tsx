import { Navigate } from "react-router-dom";
import { roleStore } from "../config/role";

interface Props {
  children: JSX.Element;
  allowed: string[]; // roles permitidos
}

export default function ProtectedRoute({ children, allowed }: Props) {
  const role = roleStore.getRole();

  if (!allowed.includes(role)) {
    return <Navigate to="/settings" replace />;
  }

  return children;
}
