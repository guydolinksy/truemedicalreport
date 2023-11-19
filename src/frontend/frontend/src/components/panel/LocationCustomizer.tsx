import { useCallback } from 'react';
import { BodyComponent } from 'reactjs-human-body';
import type { PartsInput } from 'reactjs-human-body/dist/components/BodyComponent/BodyComponent';
import type { CustomizerComponent } from './Customizer.types';

const BODY_PARTS: Record<keyof PartsInput, string> = {
  head: 'ראש',
  leftShoulder: 'כתף שמאל',
  rightShoulder: 'כתף ימין',
  leftArm: 'זרוע שמאל',
  rightArm: 'זרוע ימין',
  chest: 'חזה',
  stomach: 'בטן',
  leftLeg: 'רגל שמאל',
  rightLeg: 'רגל ימין',
  leftHand: 'יד שמאל',
  rightHand: 'יד ימין',
  leftFoot: 'כף רגל שמאל',
  rightFoot: 'כף רגל ימין',
};

export const LocationCustomizer: CustomizerComponent = ({ onChange }) => {
  const onChanget = useCallback(
    (value: PartsInput) =>
      onChange(
        Object.entries(value)
          .filter(([, { selected }]) => selected)
          .map(([part]) => BODY_PARTS[part as keyof PartsInput])
          .join(', '),
      ),
    [onChange],
  );
  return (
    <>
      <div style={{ display: 'flex', justifyContent: 'center', width: '100%' }}>סמנ.י את האזורים הרלוונטים</div>
      <BodyComponent onChange={onChanget} />
    </>
  );
};
