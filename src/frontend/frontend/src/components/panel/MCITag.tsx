import { Tag } from 'antd';
import type { FC } from 'react';

export const MCITag: FC<{ tag: string; checked: boolean; onChange?: (checked: boolean) => void; block?: boolean }> = ({
  tag,
  checked,
  onChange,
  block,
}) => (
  <Tag.CheckableTag
    checked={checked}
    onChange={onChange}
    style={{
      padding: block ? undefined : '10px 20px',
      display: 'flex',
      alignItems: 'center',
      height: block ? '80px' : '40px',
      backgroundColor: checked ? '#E5E4FF' : '#FFFFFF',
      borderColor: checked ? '#A3A1FB' : '#DCDCDF',
      marginTop: '6px',
      font: 'normal normal normal 18px/13px Source Sans Pro',
      color: '#4D565C',
      width: block ? '109px' : undefined,
      justifyContent: 'center',
    }}
  >
    {tag}
  </Tag.CheckableTag>
);
