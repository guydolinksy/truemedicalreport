import { useMemo } from 'react';
import moment from 'moment/moment';

export const useArterySliderProps = () =>
  useMemo(() => {
    const now = moment();
    const start = moment(now).add(-4, 'h');

    const max = moment(now).diff(start, 'm');
    const offset = moment(now).diff(moment(now).startOf('h'), 'm');
    const marks = {
      0: now.format('HH:mm'),
      ...(offset > 30
        ? {
            [max - 240 + offset]: moment(start)
              .add(240 - offset, 'm')
              .format('HH:mm'),
          }
        : {}),
      [max - 180 + offset]: moment(start)
        .add(180 - offset, 'm')
        .format('HH:mm'),
      [max - 120 + offset]: moment(start)
        .add(120 - offset, 'm')
        .format('HH:mm'),
      [max - 60 + offset]: moment(start)
        .add(60 - offset, 'm')
        .format('HH:mm'),
    };
    const formatter = (value?: number) =>
      moment(now)
        .add(-(value ?? 0), 'm')
        .format('HH:mm');

    return { max, marks, formatter };
  }, []);
