import { Card } from 'antd';
import React from 'react';

export const InfoPlugin = ({ title, url }) => {
  return (
    <Card title={title}>
      <iframe style={{ border: 'none', width: '100%', height: '250px' }} title={title} src={url} />
    </Card>
  );
};
