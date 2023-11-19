import { createDataContext } from '../../contexts/DataContext';

export const patientDataContext = createDataContext<{
  info?: { name: string; age?: number; id_?: number; phone?: number };
}>();
