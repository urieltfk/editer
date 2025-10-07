import { useEffect } from "react";

export const useAlert = (content: string, shouldPopUp?: boolean) => {
    useEffect(() => {
        if (shouldPopUp === undefined || shouldPopUp) {
            alert(content);
        }
    }, []);
}