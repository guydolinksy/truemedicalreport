import type { FC } from 'react';

interface ICustomizerProps {
  onChange: (value: string) => void;
  customizer?: any;
}

export type CustomizerComponent = FC<ICustomizerProps>;
