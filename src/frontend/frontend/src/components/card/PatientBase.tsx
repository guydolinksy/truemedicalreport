import { createDataContext } from '../../contexts/DataContext';

interface IMCIStringValue {
  value: string;
  at: string;
}

interface IMCIListItemValue extends IMCIStringValue {
  key: string;
}

export const patientDataContext = createDataContext<{
  info: { name?: string; age?: number; id_?: number; phone?: number };
  mci: {
    gender?: IMCIStringValue;
    age_group?: IMCIStringValue;
    occupation?: IMCIStringValue;
    transport?: IMCIStringValue;
    pre_hospital_diagnosis: Record<string, IMCIListItemValue>; // TODO - this should be a list
    pre_hospital_fluids: Record<string, IMCIListItemValue>; // TODO - this should be a list
    pre_hospital_medications: Record<string, IMCIListItemValue>; // TODO - this should be a list
    pre_hospital_vitals: Record<string, IMCIListItemValue>; // TODO - this should be a list
  };
}>();
