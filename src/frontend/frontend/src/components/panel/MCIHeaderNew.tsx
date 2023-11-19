import { Button } from 'antd';
import type { FC } from 'react';
import Moment from 'react-moment';
import { useContext } from 'react';

import { patientDataContext } from '../card/PatientBase';

export const MCIHeaderNew: FC<{ onClick: () => void; header?: string; buttonText: string }> = ({
  onClick,
  buttonText,
}) => {
  const { value } = useContext(patientDataContext.context);
  const header = `${value?.info?.name}, ת.ז. ${value?.info?.id_}`;
  return (
    <div
      style={{ width: '100%', display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '15px' }}
    >
      <div>
        <span style={{ font: 'normal normal 600 28px/37px Segoe UI', color: '#605F86' }}>{header}</span>
      </div>
      <div style={{ display: 'flex', justifyContent: 'end', alignItems: 'center' }}>
        <span>
          <Moment format={'hh:mm'} style={{ marginRight: '5px' }} />
          <Moment format={'A'} />
        </span>
        <Button
          type={'primary'}
          style={{ marginRight: '10px', backgroundColor: '#2F2E50', borderColor: '#2F2E50' }}
          onClick={onClick}
        >
          {buttonText}
        </Button>
      </div>
    </div>
  );
};
