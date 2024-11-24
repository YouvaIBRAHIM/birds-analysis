import { ReactNode } from "react"

import { useAuthStore } from "@stores/auth.store"
import { Navigate, Outlet } from "react-router-dom"


interface PrivateRouteProps {
  children?: ReactNode
}

const PrivateRoute = ({ children }: PrivateRouteProps) => {
  const { user } = useAuthStore()

  if (!user) {
    return <Navigate to="/login" />
  }

  return children ? <>{children}</> : <Outlet />
}

export default PrivateRoute
