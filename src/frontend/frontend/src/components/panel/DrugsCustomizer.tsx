import { Button } from 'antd';
import { useCallback, useState } from 'react';
import type { FC } from 'react';
import type { CustomizerComponent } from './Customizer.types';

const Drug: FC<{
  name: string;
  dosageAmount: number;
  dosageUnit: string;
  maximum: number;
  onChange: (value: string) => void;
}> = ({ name, dosageAmount, dosageUnit, maximum, onChange }) => {
  const [value, setValue] = useState(0);
  const onChanget = useCallback(
    (value: number) => () =>
      setValue((v) => {
        const newValue = Math.max(0, Math.min(maximum, v + value));
        onChange(`${newValue}${dosageUnit}`);
        return newValue;
      }),
    [dosageUnit, maximum, onChange],
  );

  return (
    <div style={{ display: 'flex', flexDirection: 'row', width: '100%', justifyContent: 'space-evenly' }}>
      <span>{name}&nbsp;</span>
      <Button onClick={onChanget(-dosageAmount)} disabled={value === 0}>
        -
      </Button>
      <span>
        {value}
        {value ? dosageUnit : ''}
      </span>
      <Button onClick={onChanget(dosageAmount)} disabled={value === maximum}>
        +
      </Button>
      <span>
        ({maximum}
        {dosageUnit})
      </span>
    </div>
  );
};

export const DrugsCustomizer: CustomizerComponent = ({ onChange, customizer }) => {
  const [, setDrugs] = useState<Record<string, string>>({});
  const onChanget = useCallback(
    (drug: string) => (amount: string) => {
      setDrugs((v) => {
        const newDrugs = { ...v, [drug]: amount };
        const newValue = Object.entries(newDrugs)
          .filter(([, dosage]) => dosage)
          .map(([drug, dosage]) => `${drug} (${dosage})`)
          .join(', ');
        onChange(newValue);
        return newDrugs;
      });
    },
    [onChange],
  );
  return (
    <>
      {customizer.options.map((option: any) => (
        <Drug
          key={option.name}
          name={option.name}
          dosageAmount={option.dosage_amount}
          dosageUnit={option.dosage_unit}
          maximum={option.maximum}
          onChange={onChanget(option.name)}
        />
      ))}
    </>
  );
};
