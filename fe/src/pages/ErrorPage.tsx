import { useAlert } from "@lib/hooks/useAlert";
import { useRouteError } from "react-router"

const ErrorPage = () => {
    const err = useRouteError();
    console.error(err);

    useAlert("A problem has occured");

    return (
        <div id="error-page">
            <p>The website has encountered an error.</p>
        </div>
    );
}

export {ErrorPage};