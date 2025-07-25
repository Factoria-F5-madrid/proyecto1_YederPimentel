import { createBrowserRouter } from "react-router-dom";
import Home from "../pages/Home";
import Login from "../pages/Login";
import Layout from "../layout/Layout";
import Register from "../pages/Register";
import Dashboard from "../pages/Dashboard";
import Suggestions from "../pages/Suggestions";

const routes = createBrowserRouter([
  {
    path: "/",
    element: <Layout />,
    children: [
      {
        index: true,
        element: <Home />,
      },
      {
        path: "/login",
        element: <Login />,
      },
      {
        path: "/register",
        element: <Register />,
      },
      {
        path: "/dashboard",
        element: <Dashboard />,
      },
      {
        path: "/suggestions",
        element: <Suggestions />,
      },
    ],
  },
]);

export default routes;
