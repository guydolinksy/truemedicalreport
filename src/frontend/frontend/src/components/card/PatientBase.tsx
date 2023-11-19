import { createDataContext } from '../../contexts/DataContext';

interface IMCIStringValue {
  value: string;
  at: string;
}

export const patientDataContext = createDataContext<{
  info: { name?: string; age?: number; id_?: number; phone?: number };
  mci: {
    gender?: IMCIStringValue;
    age_group?: IMCIStringValue;
    occupation?: IMCIStringValue;
    transport?: IMCIStringValue;
  };
}>();
