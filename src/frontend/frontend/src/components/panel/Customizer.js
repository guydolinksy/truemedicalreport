import React, {useCallback, useState} from 'react';
import { BodyComponent } from 'reactjs-human-body';
import { Modal } from 'antd';


const COMPONENTS = {location: [BodyComponent, 'onChange']}

export const Customizer = ({ isOpen, customizer, onEnd, onCancel }) => {
  const [value, setValue] = useState({});
  const onDone = useCallback(() => onEnd(Object.entries(value).filter(([, {selected}]) => selected).map(([part]) => part).join(', ')), [onEnd, value]);
  if (!customizer) return null;
  const [Component, onChangeKey] = COMPONENTS[customizer.type];
  const props = {[onChangeKey]: (e) => setValue(e)}
  return <Modal open={isOpen} onOk={onDone} onCancel={onCancel}><Component {...props}/></Modal>;
}
