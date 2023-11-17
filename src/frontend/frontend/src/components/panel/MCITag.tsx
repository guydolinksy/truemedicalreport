import { Tag } from 'antd';
import type { FC } from 'react';

export const MCITag: FC<{ tag: string; checked: boolean; onChange: (checked: boolean) => void }> = ({
  tag,
  checked,
  onChange,
}) => (
  <Tag.CheckableTag
    checked={checked}
    onChange={onChange}
    style={{
      padding: '10px 20px',
      display: 'flex',
      alignItems: 'center',
      height: '45px',
      background: checked ? 'gray' : 'white',
      marginTop: '6px',
      font: 'normal normal 600 18px/13px Source Sans Pro',
      color: '#4D565C',
    }}
  >
    {tag}
  </Tag.CheckableTag>
);
