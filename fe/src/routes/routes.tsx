import { createBrowserRouter } from 'react-router-dom'
import App from '@pages/App'
import { About } from '@pages/About'
import {ErrorPage} from '@pages/ErrorPage'

export const Router: ReturnType<typeof createBrowserRouter> = createBrowserRouter([
  {
    path: "/",
    element: <App/>,
    errorElement: <ErrorPage/>
  },
  {
    path: "/about",
    element: <About />,
  }
]);