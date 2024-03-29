import React from 'react';
import { dom, library } from '@fortawesome/fontawesome-svg-core';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faArrowDown,
  faArrowUp,
  faBoltLightning,
  faFileMedical,
  faHeart,
  faHeartPulse,
  faHourglass,
  faHouseMedicalCircleCheck,
  faPercentage,
  faStethoscope,
  faTemperatureHalf,
  faUserNurse,
  faVial,
  IconDefinition,
} from '@fortawesome/free-solid-svg-icons';

export const faImaging = {
  prefix: 'fab',
  iconName: 'imaging',
  icon: [
    24,
    24,
    [],
    'e001',
    'M 3.402344 0.132812 C 1.773438 0.523438 0.441406 1.902344 0.101562 3.542969 C -0.0390625 4.238281 -0.0390625 19.761719 0.101562 20.457031 C 0.449219 22.144531 1.855469 23.550781 3.542969 23.898438 C 4.238281 24.039062 19.761719 24.039062 20.457031 23.898438 C 22.144531 23.550781 23.550781 22.144531 23.898438 20.457031 C 24.039062 19.761719 24.039062 4.238281 23.898438 3.542969 C 23.550781 1.855469 22.144531 0.449219 20.457031 0.101562 C 19.707031 -0.0546875 4.058594 -0.0273438 3.402344 0.132812 Z M 12.582031 2.148438 C 12.851562 2.382812 12.882812 2.476562 12.917969 3.039062 L 12.957031 3.65625 L 14.773438 3.65625 C 16.734375 3.65625 17.089844 3.722656 17.382812 4.132812 C 17.625 4.492188 17.570312 4.855469 17.210938 5.210938 L 16.894531 5.53125 L 12.9375 5.53125 L 12.9375 7.40625 L 18.75 7.40625 L 19.050781 7.679688 C 19.453125 8.035156 19.460938 8.503906 19.078125 8.90625 L 18.804688 9.1875 L 12.9375 9.1875 L 12.9375 11.0625 L 16.714844 11.0625 C 20.117188 11.0625 20.511719 11.082031 20.71875 11.222656 C 21.074219 11.464844 21.179688 11.644531 21.179688 12 C 21.179688 12.355469 21.074219 12.535156 20.71875 12.777344 C 20.511719 12.917969 20.117188 12.9375 16.714844 12.9375 L 12.9375 12.9375 L 12.9375 15.65625 L 13.246094 15.601562 C 14.023438 15.460938 14.710938 15.253906 15.167969 15.027344 C 15.601562 14.820312 15.75 14.792969 16.304688 14.832031 C 16.808594 14.867188 17.035156 14.933594 17.351562 15.148438 C 17.851562 15.488281 18.234375 16.03125 18.394531 16.613281 C 18.617188 17.503906 18.179688 18.167969 16.453125 19.460938 C 15.890625 19.894531 15.074219 20.503906 14.652344 20.832031 C 13.632812 21.617188 12.777344 22.050781 12.132812 22.105469 C 11.679688 22.144531 11.53125 22.105469 10.941406 21.816406 C 10.566406 21.628906 9.863281 21.148438 9.375 20.757812 C 8.886719 20.363281 8.0625 19.761719 7.546875 19.40625 C 5.523438 18.039062 5.101562 17.070312 5.980469 15.796875 C 6.402344 15.1875 6.9375 14.886719 7.695312 14.832031 C 8.25 14.792969 8.398438 14.820312 8.832031 15.027344 C 9.289062 15.253906 9.976562 15.460938 10.761719 15.601562 L 11.0625 15.65625 L 11.0625 12.9375 L 7.285156 12.9375 C 3.253906 12.9375 3.300781 12.945312 2.933594 12.46875 C 2.785156 12.289062 2.785156 11.710938 2.933594 11.53125 C 3.300781 11.054688 3.253906 11.0625 7.285156 11.0625 L 11.0625 11.0625 L 11.0625 9.1875 L 5.195312 9.1875 L 4.921875 8.90625 C 4.539062 8.503906 4.546875 8.035156 4.949219 7.679688 L 5.25 7.40625 L 11.0625 7.40625 L 11.0625 5.53125 L 7.105469 5.53125 L 6.789062 5.210938 C 6.429688 4.855469 6.375 4.492188 6.617188 4.132812 C 6.910156 3.722656 7.265625 3.65625 9.226562 3.65625 L 11.042969 3.65625 L 11.082031 3.039062 C 11.117188 2.476562 11.148438 2.382812 11.417969 2.148438 C 11.605469 1.976562 11.820312 1.875 12 1.875 C 12.179688 1.875 12.394531 1.976562 12.582031 2.148438 Z M 12.582031 2.148438 M 7.914062 16.304688 C 7.742188 16.40625 7.546875 16.585938 7.460938 16.695312 C 7.273438 16.976562 7.265625 17.726562 7.453125 18.09375 C 7.949219 19.058594 9.554688 19.238281 10.058594 18.382812 C 10.292969 17.980469 10.265625 17.257812 10.003906 16.867188 C 9.570312 16.21875 8.523438 15.9375 7.914062 16.304688 Z M 7.914062 16.304688 M 14.625 16.332031 C 14.0625 16.621094 13.78125 17.054688 13.78125 17.644531 C 13.78125 18.535156 14.316406 18.992188 15.242188 18.917969 C 16.117188 18.84375 16.6875 18.234375 16.6875 17.363281 C 16.6875 16.332031 15.65625 15.816406 14.625 16.332031 Z M 14.625 16.332031',
  ],
};

library.add(faImaging);
dom.watch();

export const CustomIcon = ({ status, icon, style }) => {
  const className = {
    error: 'status-color status-error',
    processing: 'status-color status-neutral',
    success: 'status-color status-success',
  }[status];
  if (icon === 'pain') return <FontAwesomeIcon style={style} className={className} icon={faBoltLightning} />;
  if (icon === 'pulse') return <FontAwesomeIcon style={style} className={className} icon={faHeartPulse} />;
  if (icon === 'temperature') return <FontAwesomeIcon style={style} className={className} icon={faTemperatureHalf} />;
  if (icon === 'saturation') return <FontAwesomeIcon style={style} className={className} icon={faPercentage} />;
  if (icon === 'bloodPressure') return <FontAwesomeIcon style={style} className={className} icon={faHeart} />;
  if (icon === 'imaging') return <FontAwesomeIcon style={style} className={className} icon={faImaging} />;
  if (icon === 'laboratory') return <FontAwesomeIcon style={style} className={className} icon={faVial} />;
  if (icon === 'treatment')
    return <FontAwesomeIcon style={style} className={className} icon={faHouseMedicalCircleCheck} />;
  if (icon === 'doctor') return <FontAwesomeIcon style={style} className={className} icon={faStethoscope} />;
  if (icon === 'nurse') return <FontAwesomeIcon style={style} className={className} icon={faUserNurse} />;
  if (icon === 'referral') return <FontAwesomeIcon style={style} className={className} icon={faFileMedical} />;
  if (icon === 'awaiting') return <FontAwesomeIcon style={style} className={className} icon={faHourglass} />;
  if (icon === 'raise') return <FontAwesomeIcon style={style} className={className} icon={faArrowUp} />;
  if (icon === 'lower') return <FontAwesomeIcon style={style} className={className} icon={faArrowDown} />;
  return <span style={style}>{icon}</span>;
};
