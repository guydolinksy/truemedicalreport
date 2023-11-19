import type { FC, ReactNode } from 'react';

export const MCISectionNew: FC<{ title: string; children?: ReactNode }> = ({ title, children }) => (
  <div style={{ width: '100%', display: 'flex', alignItems: 'flex-start', marginTop: '20px', flexDirection: 'column' }}>
    <div style={{ font: 'normal normal normal 20px/13px Source Sans Pro', color: '#A3A0FB' }}>{title}</div>
    {children}
  </div>
);
