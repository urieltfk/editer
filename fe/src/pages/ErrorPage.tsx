import { useEffect } from "react"
import { useRouteError } from "react-router"
import { useToast } from "@lib/hooks/useToast"
import { Link } from "react-router-dom"

const ErrorPage = () => {
    const err = useRouteError();
    const toast = useToast();
    console.error(err);

    useEffect(() => {
        toast.error("A problem has occurred");
    }, []);

    return (
        <div id="error-page">
            <p>The website has encountered an error.</p>
            <Link to="/">Go back to editor</Link>
        </div>
    );
}

export {ErrorPage};