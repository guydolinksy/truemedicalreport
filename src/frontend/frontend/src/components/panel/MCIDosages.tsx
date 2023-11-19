import type { FC } from 'react';
import { useCallback, useContext } from 'react';
import { Input, InputNumber } from 'antd';
import { MinusOutlined, PlusOutlined } from '@ant-design/icons';

import { getAt } from '../../utils';
import { patientDataContext } from '../card/PatientBase';
import { MCISectionNew } from './MCISectionNew';

export interface IDosagesProps {
  key: 'pre_hospital_fluids' | 'pre_hospital_medications';
  title: string;
  values: { key: string; value: string; subtitle?: string; step: number; unit: string }[];
  other?: string;
}

const DosageInput: FC<{ value?: number; dosage?: number; onChange: (value: number) => void }> = ({
  value,
  dosage = 1,
  onChange,
  children,
}) => {
  const onClick = useCallback(
    (plus: boolean) => {
      const diff = plus ? dosage : -dosage;
      const newValue = (value ?? 0) + diff;
      return onChange(newValue > 0 ? newValue : 0);
    },
    [dosage, onChange, value],
  );
  return (
    <div
      style={{
        display: 'flex',
        width: '70%',
        justifyContent: 'space-between',
        margin: '6px',
        alignItems: 'center',
      }}
    >
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'start' }}>{children}</div>
      <InputNumber
        addonAfter={<MinusOutlined onClick={() => onClick(false)} />}
        addonBefore={<PlusOutlined onClick={() => onClick(true)} />}
        controls={false}
        value={value ?? 0}
        onChange={(v) => onChange(v ?? 0)}
        style={{ width: '120px' }}
      />
    </div>
  );
};

export const MCIDosages: FC<IDosagesProps & { fieldKey: IDosagesProps['key'] }> = ({
  fieldKey,
  title,
  values,
  other,
}) => {
  const { value: { mci } = { mci: undefined }, update } = useContext(patientDataContext.context);
  // TODO - get additional medications from mci value, and add them to the list
  // const medications = useMemo(() => [...values, ...[value?.mci.pre_hospital_diagnosis]], [value, values]);
  const onChange = useCallback(
    (innerKey: string, v: number) => {
      return update(['mci', fieldKey, innerKey], { key: innerKey, value: `${v}`, at: getAt() }, 'MCIListItemValue');
    },
    [fieldKey, update],
  );

  return (
    <MCISectionNew title={title}>
      <div
        style={{
          width: '100%',
          display: 'inline-flex',
          alignItems: 'start',
          marginTop: '10px',
          flexDirection: 'column',
          justifyContent: 'space-between',
        }}
      >
        {values.map(({ key: innerKey, value, subtitle }) => (
          <DosageInput
            key={innerKey}
            value={parseInt(mci?.[fieldKey][innerKey]?.value ?? '0')}
            onChange={(v) => onChange(innerKey, v)}
          >
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'start' }}>
              <span>{value}</span>
              {subtitle && <span>{subtitle}</span>}
            </div>
          </DosageInput>
        ))}
        {other && (
          <DosageInput value={0} onChange={() => {}}>
            <Input placeholder={'אחר'} />
          </DosageInput>
        )}
      </div>
    </MCISectionNew>
  );
};
