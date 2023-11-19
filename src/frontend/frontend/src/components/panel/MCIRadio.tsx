import type { CSSProperties, ReactElement, FC } from 'react';
import { Radio } from 'antd';

export const MCIRadio: FC<{
  value: string;
  name?: ReactElement | string;
  onClick?: () => void;
  style?: CSSProperties;
}> = ({ value, name, onClick, style }) => (
  <Radio value={value} onClick={onClick} style={style}>
    {name}
  </Radio>
);
