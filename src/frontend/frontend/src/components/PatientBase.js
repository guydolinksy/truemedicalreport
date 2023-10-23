import {createContext} from "../hooks/DataContext";

export const patientDataContext = createContext({
    data: {},
    update: () => null,
    loading: true,
});