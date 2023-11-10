import {ComponentProps, useCallback, useState} from 'react';
import type {FC} from 'react';
import {Modal} from 'antd';
import type {CustomizerComponent} from './Customizer.types';
import {DrugsCustomizer} from './DrugsCustomizer';
import {LocationCustomizer} from './LocationCustomizer';

type CustomizerType = 'location' | 'drugs';

const COMPONENTS: Record<CustomizerType, CustomizerComponent> = {location: LocationCustomizer, drugs: DrugsCustomizer}

interface ICustomizerModalProps {
  isOpen: boolean;
  customizer?: { type: CustomizerType };
  onEnd: (value: string) => void;
  onCancel: ComponentProps<typeof Modal>['onCancel'];
}

export const Customizer: FC<ICustomizerModalProps> = ({ isOpen, customizer, onEnd, onCancel }) => {
  const [value, setValue] = useState('');
  const onDone = useCallback(() => onEnd(value), [onEnd, value]);
  if (!customizer) return null;
  const Component = COMPONENTS[customizer.type];
  return <Modal open={isOpen} onOk={onDone} onCancel={onCancel} okText={'אישור'} cancelText={'ביטול'}>
    <Component onChange={setValue} customizer={customizer} />
  </Modal>;
}
