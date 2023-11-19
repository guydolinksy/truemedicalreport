import { PatientArrival } from './PatientStatus';
import { PatientAwaiting } from './PatientAwaiting';

export const PatientExtra = ({ mci }) => {
  return mci ? <PatientArrival /> : <PatientAwaiting />;
};
