import type { FC } from 'react';
import { Divider as AntdDivider } from 'antd';

type DividerComponent = FC<{ full?: boolean }> & { Full: FC };

export const MCIDivider: DividerComponent = (({ full }) => (
  <AntdDivider
    type="vertical"
    orientation={'center'}
    style={{ backgroundColor: '#A4AFB7', height: full ? '100%' : undefined }}
  />
)) as DividerComponent;

MCIDivider.Full = () => (
  <div style={{ display: 'flex', alignItems: 'center', height: '100%' }}>
    <MCIDivider full />
  </div>
);
