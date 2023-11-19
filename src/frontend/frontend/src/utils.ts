import moment from 'moment';

export const getAt = (): string => moment().toISOString().replace('Z', '+00:00');
